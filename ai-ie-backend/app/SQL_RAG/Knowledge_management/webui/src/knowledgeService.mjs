import {
  createInitialKnowledgeState,
} from "./knowledgeStore.mjs";

export const STORAGE_KEY = "knowledge_management_webui_state_v1";

export const RESERVED_ENDPOINTS = {
  loadState: "GET /api/knowledge/state",
  persistState: "PUT /api/knowledge/state",
  parseUpload: "POST /api/knowledge/parse",
  includeItem: "POST /api/knowledge/items/{id}/include",
  updateItem: "PUT /api/knowledge/items/{id}",
  discardItem: "DELETE /api/knowledge/items/{id}",
};

const REQUEST_TIMEOUT_MS = 1200;
// [2026-07-04 10:18:20] 作用：为真实音频解析设置十分钟超时；理由依据：FFmpeg、语音转录和三轮 DeepSeek 明显超过普通状态接口时限。
const PARSE_TIMEOUT_MS = 600000;

export function createKnowledgeService(options = {}) {
  const storage = options.storage || globalThis.localStorage;
  const fetchImpl = options.fetchImpl || globalThis.fetch?.bind(globalThis);
  const apiBase = normalizeApiBase(options.apiBase ?? readConfiguredApiBase());

  return {
    async loadState() {
      const remoteState = await tryFetchJson(fetchImpl, `${apiBase}/knowledge/state`, { method: "GET" });
      if (remoteState) {
        saveLocal(storage, remoteState);
        return remoteState;
      }
      const localState = readLocal(storage);
      return localState || createInitialKnowledgeState();
    },

    async persistState(state) {
      const remoteState = await tryFetchJson(fetchImpl, `${apiBase}/knowledge/state`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(state),
      });
      const nextState = remoteState || state;
      saveLocal(storage, nextState);
      return nextState;
    },

    async parseUpload(file, metadata = {}) {
      // [2026-07-04 10:18:20] 作用：拒绝没有真实文件对象的解析请求；理由依据：禁止仅凭文件名伪造成功结果。
      if (!file || typeof file.name !== "string") {
        // [2026-07-04 10:18:20] 作用：抛出明确的文件缺失错误；理由依据：调用方必须显示真实失败而非生成模拟卡片。
        throw new Error("请选择需要解析的真实文件");
      }
      // [2026-07-04 10:18:20] 作用：创建浏览器 multipart 表单；理由依据：后端 FastAPI UploadFile 必须接收文件字节。
      const form = new FormData();
      // [2026-07-04 10:18:20] 作用：写入文件内容与原文件名；理由依据：保留 `新录音 4.m4a` 名称并传递真实二进制。
      form.append("file", file, file.name);
      // [2026-07-04 10:18:20] 作用：仅在存在真实资产 ID 时写入表单；理由依据：避免把界面显示名称误写为 ZcLeiXin。
      if (metadata.assetTypeId) {
        // [2026-07-04 10:18:20] 作用：传递资产类型 ID；理由依据：原始数据表按该值关联资产类型。
        form.append("asset_type_id", String(metadata.assetTypeId));
      }
      // [2026-07-04 10:18:20] 作用：传递客户 ID 或默认 0；理由依据：GuanLianKeHu 是原始表复合主键必填列。
      form.append("customer_id", String(metadata.customerId ?? 0));
      // [2026-07-04 10:18:20] 作用：发起必须成功的真实解析请求；理由依据：解析失败不得回退到模拟知识结果。
      return fetchJsonOrThrow(fetchImpl, `${apiBase}/knowledge/parse`, {
        method: "POST",
        body: form,
      }, PARSE_TIMEOUT_MS);
    },

    async includeItem(itemId, item) {
      return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}/include`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(item || {}),
      });
    },

    async updateItem(itemId, item) {
      return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(item || {}),
      });
    },

    async discardItem(itemId) {
      return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}`, {
        method: "DELETE",
      });
    },
  };
}

export const knowledgeService = createKnowledgeService();

function readLocal(storage) {
  if (!storage) {
    return null;
  }
  try {
    const saved = storage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : null;
  } catch (error) {
    storage.removeItem?.(STORAGE_KEY);
    return null;
  }
}

function saveLocal(storage, state) {
  if (!storage) {
    return;
  }
  storage.setItem(STORAGE_KEY, JSON.stringify(state));
}

async function tryFetchJson(fetchImpl, url, options) {
  if (!fetchImpl || !url) {
    return null;
  }
  const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS) : null;
  try {
    const response = await fetchImpl(url, {
      ...options,
      signal: options?.signal || controller?.signal,
    });
    if (!response?.ok) {
      return null;
    }
    return response.json();
  } catch (error) {
    return null;
  } finally {
    if (timer) {
      clearTimeout(timer);
    }
  }
}

// [2026-07-04 10:18:20] 作用：声明必须返回成功 JSON 的请求函数；理由依据：真实解析链不能吞掉 API、数据库或模型错误。
async function fetchJsonOrThrow(fetchImpl, url, options, timeoutMs) {
  // [2026-07-04 10:18:20] 作用：检查浏览器 fetch 能力；理由依据：缺少网络实现时应立即报告而非返回模拟数据。
  if (!fetchImpl) {
    // [2026-07-04 10:18:20] 作用：抛出网络能力缺失错误；理由依据：调用页面需显示失败原因。
    throw new Error("当前环境不支持文件上传请求");
  }
  // [2026-07-04 10:18:20] 作用：创建请求中止控制器；理由依据：防止外部 API 永久挂起页面。
  const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
  // [2026-07-04 10:18:20] 作用：设置解析专用超时计时器；理由依据：十分钟后仍未完成应明确终止。
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;
  // [2026-07-04 10:18:20] 作用：开始真实解析请求及错误处理；理由依据：无论成功失败都需清理计时器。
  try {
    // [2026-07-04 10:18:20] 作用：调用 fetch 并附加中止信号；理由依据：保留 FormData 自动生成的 multipart boundary。
    const response = await fetchImpl(url, { ...options, signal: options?.signal || controller?.signal });
    // [2026-07-04 10:18:20] 作用：检测非 2xx 响应；理由依据：DeepSeek 或后端失败不能进入成功页面。
    if (!response?.ok) {
      // [2026-07-04 10:18:20] 作用：尝试读取后端 JSON 错误体；理由依据：优先展示 FastAPI detail。
      const payload = await response?.json?.().catch(() => null);
      // [2026-07-04 10:18:20] 作用：构造包含真实 detail 或状态码的错误；理由依据：用户需要可排查信息。
      throw new Error(payload?.detail || `文件解析请求失败（HTTP ${response?.status || "unknown"}）`);
    }
    // [2026-07-04 10:18:20] 作用：返回成功 JSON；理由依据：页面只接受真实后端解析结果。
    return response.json();
  // [2026-07-04 10:18:20] 作用：确保请求结束后执行资源清理；理由依据：避免计时器泄漏影响后续上传。
  } finally {
    // [2026-07-04 10:18:20] 作用：检测是否创建了计时器；理由依据：无 AbortController 的环境没有可清理对象。
    if (timer) {
      // [2026-07-04 10:18:20] 作用：清除解析超时计时器；理由依据：成功或快速失败后不应再触发 abort。
      clearTimeout(timer);
    }
  }
}

function readConfiguredApiBase() {
  if (globalThis.KNOWLEDGE_API_BASE === "local") {
    return "";
  }
  return globalThis.KNOWLEDGE_API_BASE || "/api";
}

function normalizeApiBase(value) {
  return String(value || "").replace(/\/$/, "");
}
