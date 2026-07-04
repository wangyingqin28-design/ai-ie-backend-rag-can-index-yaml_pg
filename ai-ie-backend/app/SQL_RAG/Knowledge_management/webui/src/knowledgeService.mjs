// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import {`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import {
  // [2026-07-04 10:18:20] 作用：执行本行代码 `createInitialKnowledgeState,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  createInitialKnowledgeState,
// [2026-07-04 10:18:20] 作用：执行本行代码 `} from "./knowledgeStore.mjs";`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
} from "./knowledgeStore.mjs";

// [2026-07-04 10:18:20] 作用：为 `export const STORAGE_KEY` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
export const STORAGE_KEY = "knowledge_management_webui_state_v1";

// [2026-07-04 10:18:20] 作用：为 `export const RESERVED_ENDPOINTS` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
export const RESERVED_ENDPOINTS = {
  // [2026-07-04 10:18:20] 作用：执行本行代码 `loadState: "GET /api/knowledge/state",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  loadState: "GET /api/knowledge/state",
  // [2026-07-04 10:18:20] 作用：执行本行代码 `persistState: "PUT /api/knowledge/state",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  persistState: "PUT /api/knowledge/state",
  // [2026-07-04 10:18:20] 作用：执行本行代码 `parseUpload: "POST /api/knowledge/parse",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  parseUpload: "POST /api/knowledge/parse",
  // [2026-07-04 10:18:20] 作用：执行本行代码 `includeItem: "POST /api/knowledge/items/{id}/include",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  includeItem: "POST /api/knowledge/items/{id}/include",
  // [2026-07-04 10:18:20] 作用：执行本行代码 `updateItem: "PUT /api/knowledge/items/{id}",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  updateItem: "PUT /api/knowledge/items/{id}",
  // [2026-07-04 10:18:20] 作用：执行本行代码 `discardItem: "DELETE /api/knowledge/items/{id}",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  discardItem: "DELETE /api/knowledge/items/{id}",
// [2026-07-04 10:18:20] 作用：执行本行代码 `};`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
};

// [2026-07-04 10:18:20] 作用：为 `const REQUEST_TIMEOUT_MS` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
const REQUEST_TIMEOUT_MS = 1200;
// [2026-07-04 10:18:20] 作用：为 `const PARSE_TIMEOUT_MS` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
const PARSE_TIMEOUT_MS = 600000;

// [2026-07-04 10:18:20] 作用：声明 `createKnowledgeService` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
export function createKnowledgeService(options = {}) {
  // [2026-07-04 10:18:20] 作用：为 `const storage` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const storage = options.storage || globalThis.localStorage;
  // [2026-07-04 10:18:20] 作用：为 `const fetchImpl` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const fetchImpl = options.fetchImpl || globalThis.fetch?.bind(globalThis);
  // [2026-07-04 10:18:20] 作用：为 `const apiBase` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const apiBase = normalizeApiBase(options.apiBase ?? readConfiguredApiBase());

  // [2026-07-04 10:18:20] 作用：执行控制结果 `return {`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `async loadState() {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    async loadState() {
      // [2026-07-04 10:18:20] 作用：为 `const remoteState` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      const remoteState = await tryFetchJson(fetchImpl, `${apiBase}/knowledge/state`, { method: "GET" });
      // [2026-07-04 10:18:20] 作用：按条件 `if (remoteState) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
      if (remoteState) {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `saveLocal(storage, remoteState);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        saveLocal(storage, remoteState);
        // [2026-07-04 10:18:20] 作用：执行控制结果 `return remoteState;`；理由依据：调用方必须获得明确返回值或可诊断失败。
        return remoteState;
      // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      }
      // [2026-07-04 10:18:20] 作用：为 `const localState` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      const localState = readLocal(storage);
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return localState || createInitialKnowledgeState();`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return localState || createInitialKnowledgeState();
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },

    // [2026-07-04 10:18:20] 作用：执行本行代码 `async persistState(state) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    async persistState(state) {
      // [2026-07-04 10:18:20] 作用：为 `const remoteState` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      const remoteState = await tryFetchJson(fetchImpl, `${apiBase}/knowledge/state`, {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `method: "PUT",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        method: "PUT",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `headers: { "Content-Type": "application/json" },`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        headers: { "Content-Type": "application/json" },
        // [2026-07-04 10:18:20] 作用：执行本行代码 `body: JSON.stringify(state),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        body: JSON.stringify(state),
      // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      });
      // [2026-07-04 10:18:20] 作用：为 `const nextState` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      const nextState = remoteState || state;
      // [2026-07-04 10:18:20] 作用：执行本行代码 `saveLocal(storage, nextState);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      saveLocal(storage, nextState);
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return nextState;`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return nextState;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },

    // [2026-07-04 10:18:20] 作用：为 `async parseUpload(file, metadata` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    async parseUpload(file, metadata = {}) {
      // [2026-07-04 10:18:20] 作用：按条件 `if (!file || typeof file.name !== "string") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
      if (!file || typeof file.name !== "string") {
        // [2026-07-04 10:18:20] 作用：执行控制结果 `throw new Error("请选择需要解析的真实文件");`；理由依据：调用方必须获得明确返回值或可诊断失败。
        throw new Error("请选择需要解析的真实文件");
      // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      }
      // [2026-07-04 10:18:20] 作用：为 `const form` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      const form = new FormData();
      // [2026-07-04 10:18:20] 作用：执行本行代码 `form.append("file", file, file.name);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      form.append("file", file, file.name);
      // [2026-07-04 10:18:20] 作用：按条件 `if (metadata.assetTypeId) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
      if (metadata.assetTypeId) {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `form.append("asset_type_id", String(metadata.assetTypeId));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        form.append("asset_type_id", String(metadata.assetTypeId));
      // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      }
      // [2026-07-04 10:18:20] 作用：执行本行代码 `form.append("customer_id", String(metadata.customerId ?? 0));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      form.append("customer_id", String(metadata.customerId ?? 0));
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return fetchJsonOrThrow(fetchImpl, `${apiBase}/knowledge/parse`, {`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return fetchJsonOrThrow(fetchImpl, `${apiBase}/knowledge/parse`, {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `method: "POST",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        method: "POST",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `body: form,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        body: form,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `}, PARSE_TIMEOUT_MS);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      }, PARSE_TIMEOUT_MS);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },

    // [2026-07-04 10:18:20] 作用：执行本行代码 `async includeItem(itemId, item) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    async includeItem(itemId, item) {
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}/include`, {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `method: "POST",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        method: "POST",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `headers: { "Content-Type": "application/json" },`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        headers: { "Content-Type": "application/json" },
        // [2026-07-04 10:18:20] 作用：执行本行代码 `body: JSON.stringify(item || {}),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        body: JSON.stringify(item || {}),
      // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      });
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },

    // [2026-07-04 10:18:20] 作用：执行本行代码 `async updateItem(itemId, item) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    async updateItem(itemId, item) {
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}`, {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `method: "PUT",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        method: "PUT",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `headers: { "Content-Type": "application/json" },`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        headers: { "Content-Type": "application/json" },
        // [2026-07-04 10:18:20] 作用：执行本行代码 `body: JSON.stringify(item || {}),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        body: JSON.stringify(item || {}),
      // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      });
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },

    // [2026-07-04 10:18:20] 作用：执行本行代码 `async discardItem(itemId) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    async discardItem(itemId) {
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return tryFetchJson(fetchImpl, `${apiBase}/knowledge/items/${encodeURIComponent(itemId)}`, {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `method: "DELETE",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        method: "DELETE",
      // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      });
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },
  // [2026-07-04 10:18:20] 作用：执行本行代码 `};`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  };
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：为 `export const knowledgeService` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
export const knowledgeService = createKnowledgeService();

// [2026-07-04 10:18:20] 作用：声明 `readLocal` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function readLocal(storage) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (!storage) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (!storage) {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return null;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：进入异常控制片段 `try {`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
  try {
    // [2026-07-04 10:18:20] 作用：为 `const saved` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const saved = storage.getItem(STORAGE_KEY);
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return saved ? JSON.parse(saved) : null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return saved ? JSON.parse(saved) : null;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `} catch (error) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  } catch (error) {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `storage.removeItem?.(STORAGE_KEY);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    storage.removeItem?.(STORAGE_KEY);
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return null;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `saveLocal` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function saveLocal(storage, state) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (!storage) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (!storage) {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：执行本行代码 `storage.setItem(STORAGE_KEY, JSON.stringify(state));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  storage.setItem(STORAGE_KEY, JSON.stringify(state));
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `tryFetchJson` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
async function tryFetchJson(fetchImpl, url, options) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (!fetchImpl || !url) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (!fetchImpl || !url) {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return null;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：为 `const controller` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
  // [2026-07-04 10:18:20] 作用：为 `const timer` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const timer = controller ? setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS) : null;
  // [2026-07-04 10:18:20] 作用：进入异常控制片段 `try {`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
  try {
    // [2026-07-04 10:18:20] 作用：为 `const response` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const response = await fetchImpl(url, {
      // [2026-07-04 10:18:20] 作用：执行本行代码 `...options,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      ...options,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `signal: options?.signal || controller?.signal,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      signal: options?.signal || controller?.signal,
    // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    });
    // [2026-07-04 10:18:20] 作用：按条件 `if (!response?.ok) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
    if (!response?.ok) {
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return null;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return response.json();`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return response.json();
  // [2026-07-04 10:18:20] 作用：执行本行代码 `} catch (error) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  } catch (error) {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return null;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `} finally {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  } finally {
    // [2026-07-04 10:18:20] 作用：按条件 `if (timer) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
    if (timer) {
      // [2026-07-04 10:18:20] 作用：执行本行代码 `clearTimeout(timer);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      clearTimeout(timer);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `fetchJsonOrThrow` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
async function fetchJsonOrThrow(fetchImpl, url, options, timeoutMs) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (!fetchImpl) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (!fetchImpl) {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `throw new Error("当前环境不支持文件上传请求");`；理由依据：调用方必须获得明确返回值或可诊断失败。
    throw new Error("当前环境不支持文件上传请求");
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：为 `const controller` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
  // [2026-07-04 10:18:20] 作用：为 `const timer` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;
  // [2026-07-04 10:18:20] 作用：进入异常控制片段 `try {`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
  try {
    // [2026-07-04 10:18:20] 作用：为 `const response` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const response = await fetchImpl(url, { ...options, signal: options?.signal || controller?.signal });
    // [2026-07-04 10:18:20] 作用：按条件 `if (!response?.ok) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
    if (!response?.ok) {
      // [2026-07-04 10:18:20] 作用：为 `const payload` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      const payload = await response?.json?.().catch(() => null);
      // [2026-07-04 10:18:20] 作用：执行控制结果 `throw new Error(payload?.detail || `文件解析请求失败（HTTP ${response?.status || "unknown"}）`);`；理由依据：调用方必须获得明确返回值或可诊断失败。
      throw new Error(payload?.detail || `文件解析请求失败（HTTP ${response?.status || "unknown"}）`);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return response.json();`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return response.json();
  // [2026-07-04 10:18:20] 作用：执行本行代码 `} finally {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  } finally {
    // [2026-07-04 10:18:20] 作用：按条件 `if (timer) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
    if (timer) {
      // [2026-07-04 10:18:20] 作用：执行本行代码 `clearTimeout(timer);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      clearTimeout(timer);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `readConfiguredApiBase` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function readConfiguredApiBase() {
  // [2026-07-04 10:18:20] 作用：按条件 `if (globalThis.KNOWLEDGE_API_BASE === "local") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (globalThis.KNOWLEDGE_API_BASE === "local") {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return "";`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return "";
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return globalThis.KNOWLEDGE_API_BASE || "/api";`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return globalThis.KNOWLEDGE_API_BASE || "/api";
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `normalizeApiBase` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function normalizeApiBase(value) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return String(value || "").replace(/\/$/, "");`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return String(value || "").replace(/\/$/, "");
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}
