// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import test from "node:test";`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import test from "node:test";
// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import assert from "node:assert/strict";`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import assert from "node:assert/strict";

// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import {`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import {
  // [2026-07-04 10:18:20] 作用：执行本行代码 `RESERVED_ENDPOINTS,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  RESERVED_ENDPOINTS,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `createKnowledgeService,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  createKnowledgeService,
// [2026-07-04 10:18:20] 作用：执行本行代码 `} from "../src/knowledgeService.mjs";`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
} from "../src/knowledgeService.mjs";

// [2026-07-04 10:18:20] 作用：为 `test("service 层声明知识管理预留接口路径", ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
test("service 层声明知识管理预留接口路径", () => {
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(RESERVED_ENDPOINTS.loadState, "GET /api/knowledge/state");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(RESERVED_ENDPOINTS.loadState, "GET /api/knowledge/state");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(RESERVED_ENDPOINTS.persistState, "PUT /api/knowledge/state");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(RESERVED_ENDPOINTS.persistState, "PUT /api/knowledge/state");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(RESERVED_ENDPOINTS.parseUpload, "POST /api/knowledge/parse");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(RESERVED_ENDPOINTS.parseUpload, "POST /api/knowledge/parse");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(RESERVED_ENDPOINTS.includeItem, "POST /api/knowledge/items/{id}/include");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(RESERVED_ENDPOINTS.includeItem, "POST /api/knowledge/items/{id}/include");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(RESERVED_ENDPOINTS.updateItem, "PUT /api/knowledge/items/{id}");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(RESERVED_ENDPOINTS.updateItem, "PUT /api/knowledge/items/{id}");
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：为 `test("后端不可用时 service 使用本地存储兜底", async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
test("后端不可用时 service 使用本地存储兜底", async () => {
  // [2026-07-04 10:18:20] 作用：为 `const memory` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const memory = createMemoryStorage();
  // [2026-07-04 10:18:20] 作用：为 `const service` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const service = createKnowledgeService({
    // [2026-07-04 10:18:20] 作用：执行本行代码 `storage: memory,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    storage: memory,
    // [2026-07-04 10:18:20] 作用：为 `fetchImpl: async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    fetchImpl: async () => {
      // [2026-07-04 10:18:20] 作用：执行控制结果 `throw new Error("backend offline");`；理由依据：调用方必须获得明确返回值或可诊断失败。
      throw new Error("backend offline");
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },
  // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  });

  // [2026-07-04 10:18:20] 作用：为 `const state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const state = await service.loadState();
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(state.records.length, 34);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(state.records.length, 34);

  // [2026-07-04 10:18:20] 作用：为 `const saved` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const saved = await service.persistState({ ...state, route: "add" });
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(saved.route, "add");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(saved.route, "add");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(JSON.parse(memory.getItem("knowledge_management_webui_state_v1")).route, "a`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(JSON.parse(memory.getItem("knowledge_management_webui_state_v1")).route, "add");
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：为 `test("解析上传使用真实 FormData 并传递资产和客户元数据", async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
test("解析上传使用真实 FormData 并传递资产和客户元数据", async () => {
  // [2026-07-04 10:18:20] 作用：为 `let capturedUrl` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  let capturedUrl = "";
  // [2026-07-04 10:18:20] 作用：为 `let capturedOptions` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  let capturedOptions = null;
  // [2026-07-04 10:18:20] 作用：为 `const service` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const service = createKnowledgeService({
    // [2026-07-04 10:18:20] 作用：执行本行代码 `storage: createMemoryStorage(),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    storage: createMemoryStorage(),
    // [2026-07-04 10:18:20] 作用：为 `fetchImpl: async (url, options)` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    fetchImpl: async (url, options) => {
      // [2026-07-04 10:18:20] 作用：为 `capturedUrl` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      capturedUrl = url;
      // [2026-07-04 10:18:20] 作用：为 `capturedOptions` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      capturedOptions = options;
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return {`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `ok: true,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        ok: true,
        // [2026-07-04 10:18:20] 作用：执行本行代码 `async json() {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        async json() {
          // [2026-07-04 10:18:20] 作用：执行控制结果 `return { fileName: "会议录音.m4a", fullText: "真实转录", knowledgeItems: [] };`；理由依据：调用方必须获得明确返回值或可诊断失败。
          return { fileName: "会议录音.m4a", fullText: "真实转录", knowledgeItems: [] };
        // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        },
      // [2026-07-04 10:18:20] 作用：执行本行代码 `};`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      };
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },
  // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  });
  // [2026-07-04 10:18:20] 作用：为 `const file` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const file = new Blob(["audio-bytes"], { type: "audio/mp4" });
  // [2026-07-04 10:18:20] 作用：执行本行代码 `Object.defineProperty(file, "name", { value: "会议录音.m4a" });`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  Object.defineProperty(file, "name", { value: "会议录音.m4a" });

  // [2026-07-04 10:18:20] 作用：为 `const parsed` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const parsed = await service.parseUpload(file, { assetTypeId: "asset-1", customerId: 9 });

  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(capturedUrl, "/api/knowledge/parse");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(capturedUrl, "/api/knowledge/parse");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(capturedOptions.method, "POST");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(capturedOptions.method, "POST");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.ok(capturedOptions.body instanceof FormData);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.ok(capturedOptions.body instanceof FormData);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(capturedOptions.body.get("file").name, "会议录音.m4a");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(capturedOptions.body.get("file").name, "会议录音.m4a");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(capturedOptions.body.get("asset_type_id"), "asset-1");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(capturedOptions.body.get("asset_type_id"), "asset-1");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(capturedOptions.body.get("customer_id"), "9");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(capturedOptions.body.get("customer_id"), "9");
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(capturedOptions.headers, undefined);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(capturedOptions.headers, undefined);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.equal(parsed.fullText, "真实转录");`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.equal(parsed.fullText, "真实转录");
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：为 `test("解析接口失败时抛出真实错误且不返回模拟成功", async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
test("解析接口失败时抛出真实错误且不返回模拟成功", async () => {
  // [2026-07-04 10:18:20] 作用：为 `const service` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const service = createKnowledgeService({
    // [2026-07-04 10:18:20] 作用：执行本行代码 `storage: createMemoryStorage(),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    storage: createMemoryStorage(),
    // [2026-07-04 10:18:20] 作用：为 `fetchImpl: async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    fetchImpl: async () => ({
      // [2026-07-04 10:18:20] 作用：执行本行代码 `ok: false,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      ok: false,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `status: 503,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      status: 503,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `async json() {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      async json() {
        // [2026-07-04 10:18:20] 作用：执行控制结果 `return { detail: "DeepSeek service unavailable" };`；理由依据：调用方必须获得明确返回值或可诊断失败。
        return { detail: "DeepSeek service unavailable" };
      // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      },
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }),
  // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  });
  // [2026-07-04 10:18:20] 作用：为 `const file` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const file = new Blob(["audio-bytes"], { type: "audio/mp4" });
  // [2026-07-04 10:18:20] 作用：执行本行代码 `Object.defineProperty(file, "name", { value: "会议录音.m4a" });`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  Object.defineProperty(file, "name", { value: "会议录音.m4a" });

  // [2026-07-04 10:18:20] 作用：执行本行代码 `await assert.rejects(`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  await assert.rejects(
    // [2026-07-04 10:18:20] 作用：执行本行代码 `service.parseUpload(file),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    service.parseUpload(file),
    // [2026-07-04 10:18:20] 作用：执行本行代码 `/DeepSeek service unavailable/,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    /DeepSeek service unavailable/,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  );
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：声明 `createMemoryStorage` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function createMemoryStorage() {
  // [2026-07-04 10:18:20] 作用：为 `const store` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const store = new Map();
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return {`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `getItem(key) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    getItem(key) {
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return store.has(key) ? store.get(key) : null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return store.has(key) ? store.get(key) : null;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },
    // [2026-07-04 10:18:20] 作用：执行本行代码 `setItem(key, value) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    setItem(key, value) {
      // [2026-07-04 10:18:20] 作用：执行本行代码 `store.set(key, String(value));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      store.set(key, String(value));
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },
    // [2026-07-04 10:18:20] 作用：执行本行代码 `removeItem(key) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    removeItem(key) {
      // [2026-07-04 10:18:20] 作用：执行本行代码 `store.delete(key);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      store.delete(key);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    },
  // [2026-07-04 10:18:20] 作用：执行本行代码 `};`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  };
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}
