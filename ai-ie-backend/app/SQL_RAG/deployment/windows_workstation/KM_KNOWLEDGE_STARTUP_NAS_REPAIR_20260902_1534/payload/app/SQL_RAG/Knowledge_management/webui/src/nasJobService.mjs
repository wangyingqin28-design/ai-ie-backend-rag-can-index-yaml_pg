// [2026-08-22 19:02:14] 作用：复用商业任务的部署基址与身份头；理由依据：本地和 NAS 两条入口必须落到同一 18320 实例、租户和浏览器所有者边界。
import { identityHeaders, normalizeCommercialError, resolveCommercialApiBase } from "./commercialJobService.mjs";

// [2026-08-22 19:02:14] 作用：声明 NAS 浏览器并发上传上限；理由依据：大文件正文直接背压流向 NAS，三路并发避免四十人使用时把控制面连接耗尽。
const NAS_UPLOAD_CONCURRENCY = 3;
// [2026-09-01 11:11:11] 作用：限定单个 NAS 文件的瞬态上传总尝试次数；理由依据：并发创建共同父目录时对方 WebDAV 可能短暂返回 502，必须复用当前浏览器 File 自动恢复且禁止无限重试。
const NAS_UPLOAD_MAX_ATTEMPTS = 3;
// [2026-09-01 11:11:11] 作用：声明允许自动重传的 NAS 网关状态；理由依据：只吸收 502、503、504 瞬态故障，路径、权限和清单类永久错误继续立即失败关闭。
const NAS_UPLOAD_RETRYABLE_STATUS_CODES = new Set([502, 503, 504]);
// [2026-09-01 11:11:11] 作用：声明 NAS 文件瞬态重传的基础退避毫秒数；理由依据：让并发目录创建请求先完成并避免立即再次碰撞，同时把用户等待控制在一秒内。
const NAS_UPLOAD_RETRY_DELAY_MS = 250;

// [2026-08-22 19:02:14] 作用：拼接 NAS 第二入口根路径；理由依据：集成页、独立页和固定一键部署只改变已有 API 基址。
function nasPath(suffix = "") {
  // [2026-08-22 19:02:14] 作用：返回稳定 NAS 资源地址；理由依据：不把 172.18.1.95、账号 UUID 或共享目录暴露给浏览器。
  return `${resolveCommercialApiBase()}/knowledge/nas${suffix}`;
}

// [2026-08-22 19:02:14] 作用：解析 NAS 接口错误正文；理由依据：文件验真、代理未部署和三重门禁失败必须显示真实中文原因。
async function nasResponseError(response) {
  // [2026-08-22 19:02:14] 作用：尝试读取 FastAPI detail；理由依据：非 JSON 上游故障仍回落到 HTTP 状态。
  const payload = await response.json().catch(() => null);
  // [2026-09-01 11:11:11] 作用：构造保留服务端诊断的 NAS 错误；理由依据：WebUI 不能把部署缺失或上游故障伪装成文件不支持。
  const error = new Error(String(payload?.detail || `NAS 请求失败：HTTP ${response.status}`));
  // [2026-09-01 11:11:11] 作用：把 HTTP 状态附加到错误对象；理由依据：上传重传必须精确区分瞬态网关错误与永久业务错误。
  error.status = Number(response.status);
  // [2026-09-01 11:11:11] 作用：返回带状态的 NAS 错误；理由依据：现有调用方继续读取 message，上传调用方额外消费 status 而不改变公开接口。
  return error;
}

// [2026-08-22 19:02:14] 作用：执行带统一传输错误语义的请求；理由依据：NAS 第二入口和原商业任务均不得裸露 Failed to fetch。
async function requestJson(url, options = {}) {
  // [2026-08-22 19:02:14] 作用：声明响应变量；理由依据：网络异常与 HTTP 业务异常需要分层处理。
  let response;
  // [2026-08-22 19:02:14] 作用：隔离浏览器传输异常；理由依据：主动中止仍保留 AbortError，网络瞬断复用既有中文诊断。
  try { response = await fetch(url, options); } catch (error) { throw normalizeCommercialError(error); }
  // [2026-08-22 19:02:14] 作用：拒绝非成功状态；理由依据：只有后端确认的快照才可驱动页面。
  if (!response.ok) throw await nasResponseError(response);
  // [2026-08-22 19:02:14] 作用：返回结构化结果；理由依据：创建、逐文件上传、验真和票据共享该合同。
  return response.json();
}

// [2026-09-01 11:11:11] 作用：以有界退避重传单个 NAS 文件请求；理由依据：浏览器 File 可安全重读，而 SQL_RAG 后端的单次流式请求体在 502 后不可回放。
async function requestNasUploadWithRetry(url, options = {}) {
  // [2026-09-01 11:11:11] 作用：遍历固定三次上传机会；理由依据：第一次保留原行为，后两次只用于吸收短暂 WebDAV 目录创建或网关抖动。
  for (let attempt = 1; attempt <= NAS_UPLOAD_MAX_ATTEMPTS; attempt += 1) {
    // [2026-09-01 11:11:11] 作用：执行当前 fileId 的原始上传请求；理由依据：成功快照仍由后端 PostgreSQL 状态驱动而不由前端伪造。
    try { return await requestJson(url, options); } catch (error) {
      // [2026-09-01 11:11:11] 作用：判断当前失败是否允许再次发送同一浏览器 File；理由依据：仅重试网关瞬态状态且尊重用户主动中止和最大次数。
      const shouldRetry = NAS_UPLOAD_RETRYABLE_STATUS_CODES.has(Number(error?.status)) && attempt < NAS_UPLOAD_MAX_ATTEMPTS && options.signal?.aborted !== true;
      // [2026-09-01 11:11:11] 作用：对永久错误、主动中止或最终失败立即保留原异常；理由依据：路径错位、权限和持续故障不能被重试掩盖。
      if (!shouldRetry) throw error;
      // [2026-09-01 11:11:11] 作用：按尝试次数等待短退避；理由依据：共同父目录的成功创建需要先对其他并发请求可见。
      await new Promise((resolve) => setTimeout(resolve, NAS_UPLOAD_RETRY_DELAY_MS * attempt));
    }
  }
  // [2026-09-01 11:11:11] 作用：阻断不可能的重试循环穿透；理由依据：任何未来控制流修改都不能把无快照状态当成上传成功。
  throw new Error("NAS 上传重试流程未返回服务器快照");
}

// [2026-08-22 19:02:14] 作用：读取浏览器提供的稳定相对路径；理由依据：优先使用目录选择器的 webkitRelativePath，并兼容文件选择器或受控浏览器提供的 path 元数据。
export function directoryRelativePath(file) {
  // [2026-08-22 19:02:14] 作用：优先读取目录选择器相对路径；理由依据：真实目录授权时该字段是浏览器唯一可靠的层级证据。
  const relative = String(file?.webkitRelativePath || "").trim();
  // [2026-08-27 09:11:36] 作用：兼容缓存、浏览器和壳层暴露的路径字段；理由依据：普通文件选择器必须先显示文件，若运行环境提供相对或绝对 path 则仍可保留完整层级，绝不把绝对路径发送到后端。
  const exposedPath = String(file?.relativePath || file?.localPath || file?.path || file?.fullPath || "").trim();
  const pathWithoutDrive = exposedPath.replace(/^\/?[A-Za-z]:[\\/]/, "");
  const value = relative || pathWithoutDrive || String(file?.name || "");
  // [2026-08-22 19:02:14] 作用：规范斜杠并移除危险根前缀；理由依据：服务端仍会执行最终路径越界门禁。
  return value.replaceAll("\\", "/").replace(/^\/+/, "");
}

// [2026-08-27 10:06:24] 作用：读取受控浏览器显式提供的源盘符；理由依据：同一批不能混入两块本地盘后再丢失盘符信息并造成 NAS 路径碰撞。
export function directoryDriveRoot(file) {
  // [2026-08-27 10:06:24] 作用：只检查可能携带绝对路径的受控字段；理由依据：webkitRelativePath 本身没有盘符，不能由程序猜测其来源盘。
  const exposedPath = String(file?.relativePath || file?.localPath || file?.path || file?.fullPath || "").trim();
  // [2026-08-27 10:06:24] 作用：返回规范大写盘符或空值；理由依据：盘符仅在当前浏览器内用于防串盘门禁，不写入 NAS 清单。
  return exposedPath.match(/^\/?([A-Za-z]):[\\/]/)?.[1]?.toUpperCase() || "";
}

// [2026-08-22 19:02:14] 作用：读取目录根名；理由依据：同一企业、用户和根名映射到稳定隔离工作区，重新选择才能动态对账修改。
export function directoryRootName(files) {
  // [2026-08-24 10:00:39] 作用：读取首条文件和目录相对路径；理由依据：目录选择保留真实根名，普通多文件选择不能把首文件名误当成工作区。
  const firstPath = directoryRelativePath(Array.from(files || [])[0]);
  // [2026-08-26 18:48:00] 作用：只从浏览器实际目录证据返回盘符后的第一段；理由依据：普通文件框只有文件名，生成固定兜底根会破坏用户要求的一比一路径映射。
  return firstPath.includes("/") ? firstPath.split("/")[0] : "";
}

// [2026-08-24 12:01:47] 作用：从本次目录选择自动解析 NAS 目标根；理由依据：用户不输入目标文字，所选根名必须成为动态同步的唯一目录身份。
export function resolveNasFolderName(files, explicitFolderName = "") {
  // [2026-08-24 12:01:47] 作用：读取目录选择器的真实根名；理由依据：webkitRelativePath 提供根名和内部相对路径，普通文件选择不具备该目录真相。
  const derived = directoryRootName(files);
  // [2026-08-27 09:11:36] 作用：在创建任务前拒绝缺少父目录层级的浏览器文件；理由依据：没有真实路径证据就无法只替换盘符根，失败关闭可防止文件落入错误 NAS 路径。
  if (!derived) throw new Error("浏览器未提供本地父路径层级；请在当前访问者浏览器提供路径信息后再提交 NAS 文件");
  // [2026-08-27 10:06:24] 作用：统计受控浏览器明确暴露的源盘符；理由依据：盘符删除前先证明本批只来自同一块本地盘，避免 D 盘和 E 盘同名路径互相覆盖。
  const driveRoots = new Set(Array.from(files || []).map(directoryDriveRoot).filter(Boolean));
  // [2026-08-27 10:06:24] 作用：拒绝跨盘批次；理由依据：每位同事只能提交自己当前浏览器明确选择的单一源盘文件树，不能把多个盘压成一个 NAS 根。
  if (driveRoots.size > 1) throw new Error("本批 NAS 文件来自多个本地盘符；请按单一盘符分批选择，禁止串盘映射");
  // [2026-08-27 09:11:36] 作用：检查本批所有文件是否来自同一真实顶层根；理由依据：跨盘符或跨根选择不能被压进一个 NAS 工作区并造成路径错位。
  const roots = new Set(Array.from(files || []).map((file) => directoryRelativePath(file).split("/").filter(Boolean)[0]).filter(Boolean));
  // [2026-08-27 09:11:36] 作用：拒绝多个真实根混合提交；理由依据：NAS 目标根只能有一个，不能由程序擅自选择或拼接。
  if (roots.size > 1) throw new Error("本批 NAS 文件来自多个顶层路径；请按同一真实顶层路径分批选择");
  // [2026-08-25 16:50:00] 作用：校验调用方携带的根名只能等于浏览器目录证据；理由依据：禁止时间戳、人员姓名或任何页面生成值替代真实第一层目录。
  const explicit = String(explicitFolderName || "").trim();
  // [2026-08-25 16:50:00] 作用：拒绝根名和 File 元数据不一致；理由依据：选中批次和完整目录清单必须指向同一个动态 NAS 根。
  if (explicit && explicit !== derived) throw new Error("NAS 目标根与本次选择的真实顶层目录不一致");
  // [2026-08-25 16:50:00] 作用：返回盘符后的真实第一段目录；理由依据：服务端直接把该根接到“魔方数据存储文档”且不再插入固定层级。
  return derived;
}

// [2026-08-24 11:01:24] 作用：验证文件同步阶段的独立健康门禁；理由依据：nas-admin 已就绪时必须允许建目录和上传，解析代理未上线只影响后续派发。
export function assertNasUploadHealth(health) {
  // [2026-08-24 11:01:24] 作用：仅在文件管理服务不可用时阻断；理由依据：不能回落本机，但也不能把两个分层服务错误耦合。
  if (health?.nasAdminReady !== true) throw new Error(String(health?.error || "NAS 文件管理服务当前不可用"));
  // [2026-08-24 11:01:24] 作用：返回分层健康快照；理由依据：调用方仍可展示解析代理状态而不伪造完整就绪。
  return health;
}

// [2026-08-22 20:06:18] 作用：生成所选根目录内部的相对路径；理由依据：远端工作区已包含 folderName，不能再次拼出“文件夹/文件夹/文件”的重复层级。
export function directoryManifestRelativePath(file) {
  // [2026-08-22 20:06:18] 作用：拆分浏览器完整相对路径；理由依据：第一段是原生目录选择器固定附带的根名。
  const parts = directoryRelativePath(file).split("/").filter(Boolean);
  // [2026-08-22 20:06:18] 作用：返回根内路径并兼容测试 File；理由依据：真实目录至少两段，普通 File 仍以文件名作为安全兜底。
  return parts.length > 1 ? parts.slice(1).join("/") : String(file?.name || parts[0] || "");
}

// [2026-08-22 19:02:14] 作用：构造 NAS 文件声明；理由依据：任何原始字节发送前先取得 PostgreSQL jobId/fileId 和远端目标路径。
export function directoryManifest(files) {
  // [2026-08-22 19:02:14] 作用：投影浏览器安全元数据；理由依据：不记录本地绝对地址、修改时间或文件正文。
  return Array.from(files || []).map((file) => ({ name: file.name, relativePath: directoryManifestRelativePath(file), size: Number(file.size || 0), contentType: file.type || "application/octet-stream" }));
}

// [2026-08-22 19:02:14] 作用：按相对路径和大小关联浏览器 File 与服务器 fileId；理由依据：子目录可出现同名文件且不能错传、错播。
function findBrowserFile(serverFile, files) {
  // [2026-08-22 19:02:14] 作用：精确匹配目录路径和大小；理由依据：任一不一致都必须停止上传等待重新选择。
  return Array.from(files || []).find((file) => directoryManifestRelativePath(file) === String(serverFile.relativePath || "") && Number(file.size || 0) === Number(serverFile.size || 0));
}

// [2026-08-22 19:02:14] 作用：执行有界并发浏览器到 NAS 流式上传；理由依据：每个请求只保留网络块，SQL_RAG 本机不形成原文件副本。
async function uploadDirectory(job, files, tenantId, onSnapshot, signal) {
  // [2026-08-22 19:02:14] 作用：筛出尚未被 NAS 接收的来源；理由依据：同页重试不重复覆盖已上传且已验真的文件。
  const pending = Array.from(job?.files || []).filter((item) => !item.nasVerified && !["uploaded_unverified", "verified_waiting_remote_parse", "verified_waiting_parse_agent", "parse_dispatched", "remote_parse_dispatched", "parsing", "remote_parse_completed", "business_sync_verifying", "completed"].includes(String(item.nasStatus || "")));
  // [2026-08-22 19:02:14] 作用：创建共享任务游标；理由依据：三个工作协程只领取一次每个 fileId。
  let cursor = 0;
  // [2026-08-22 19:02:14] 作用：声明单个上传工作协程；理由依据：任一文件失败会中止本轮验真且保留已完成远端文件供重选恢复。
  const worker = async () => {
    // [2026-08-24 17:32:00] 作用：持续领取当前一至二十文件批次中的待上传文件；理由依据：完整目录另作发现清单，三路协程继续保证网络和控制面资源有界。
    while (cursor < pending.length) {
      // [2026-08-22 19:02:14] 作用：原子领取当前数组索引；理由依据：JavaScript 单线程同步递增不会重复领取。
      const serverFile = pending[cursor++];
      // [2026-08-22 19:02:14] 作用：查找精确浏览器文件；理由依据：关闭重开后没有 File 权限时禁止发送错误正文。
      const file = findBrowserFile(serverFile, files);
      // [2026-08-22 19:02:14] 作用：拒绝目录清单不一致；理由依据：用户必须重新选择同一目录后才能继续。
      if (!file) throw new Error(`请重新选择包含原文件的同一目录：${serverFile.relativePath || serverFile.name}`);
      // [2026-09-01 11:11:11] 作用：对当前 File 使用有界瞬态重传入口；理由依据：保持三路并发吞吐，同时在共同父目录并发创建或 NAS 网关抖动后自动从同一 fileId 恢复。
      const snapshot = await requestNasUploadWithRetry(nasPath(`/jobs/${encodeURIComponent(job.jobId)}/files/${encodeURIComponent(serverFile.fileId)}/content`), { method: "PUT", headers: identityHeaders(tenantId, { "Content-Type": file.type || "application/octet-stream" }), body: file, signal });
      // [2026-08-22 19:02:14] 作用：发布后端确认快照；理由依据：页面不按已发送字节伪造远端上传成功。
      onSnapshot?.(snapshot);
    }
  };
  // [2026-08-22 19:02:14] 作用：启动不超过文件数的工作协程；理由依据：空恢复批次不创建无意义 Promise。
  await Promise.all(Array.from({ length: Math.min(NAS_UPLOAD_CONCURRENCY, pending.length) }, () => worker()));
}

// [2026-08-22 19:02:14] 作用：导出 NAS 第二入口客户端；理由依据：页面只编排目录选择和可见状态，不接触 NAS 凭据或物理路径。
export const nasJobService = {
  // [2026-08-22 19:02:14] 作用：读取两层健康状态；理由依据：区分 nas-admin 可用和 NAS 侧解析代理已部署。
  health() { return requestJson(nasPath("/health")); },
  // [2026-08-22 19:02:14] 作用：创建 NAS 持久任务；理由依据：文件字节上传前完成清单、业务上下文和三重门禁登记。
  create(files, metadata) { return requestJson(nasPath("/jobs"), { method: "POST", headers: identityHeaders(metadata.gsId, { "Content-Type": "application/json" }), body: JSON.stringify({ assetTypeId: metadata.assetTypeId, customerId: metadata.customerId, gsId: metadata.gsId, folderName: resolveNasFolderName(files, metadata.folderName), files: directoryManifest(files) }) }); },
  // [2026-08-22 19:02:14] 作用：上传目录内尚未验真的文件；理由依据：保留 File 当前生命周期且不写 localStorage。
  upload(job, files, tenantId, onSnapshot, signal) { return uploadDirectory(job, files, tenantId, onSnapshot, signal); },
  // [2026-08-22 19:02:14] 作用：触发远端一比一对账、删除多余文件并派发 NAS 侧解析；理由依据：第一标志只有重新列目录精确一致后才能为真。
  verify(jobId, tenantId, signal, inventoryFiles = [], inventoryComplete = true) { return requestJson(nasPath(`/jobs/${encodeURIComponent(jobId)}/verify`), { method: "POST", headers: identityHeaders(tenantId, { "Content-Type": "application/json" }), body: JSON.stringify({ inventory: directoryManifest(inventoryFiles), inventoryComplete: Boolean(inventoryComplete) }), signal }); },
  // [2026-08-24 16:10:00] 作用：恢复代理晚启动或单文件超时的未完成 NAS 解析；理由依据：服务端重新核对物理清单后只按原 fileId 幂等重派，不重置已完成业务阶段。
  dispatch(jobId, tenantId, signal) { return requestJson(nasPath(`/jobs/${encodeURIComponent(jobId)}/dispatch`), { method: "POST", headers: identityHeaders(tenantId), signal }); },
  // [2026-08-22 19:02:14] 作用：恢复 NAS 增强快照；理由依据：刷新后仍显示三个门禁而不是只看通用任务阶段。
  get(jobId, tenantId, signal) { return requestJson(nasPath(`/jobs/${encodeURIComponent(jobId)}`), { headers: identityHeaders(tenantId), signal }); },
  // [2026-08-22 19:02:14] 作用：为强绑定 rawDataId 签发短时媒体地址；理由依据：audio 标签无需获取 X-NAS-ID 或任意下载路径。
  ticket(rawDataId, tenantId) { return requestJson(nasPath(`/media/tickets/${encodeURIComponent(rawDataId)}`), { method: "POST", headers: identityHeaders(tenantId) }); },
};
