import test from "node:test";
import assert from "node:assert/strict";

import {
  RESERVED_ENDPOINTS,
  createKnowledgeService,
} from "../src/knowledgeService.mjs";

test("service 层声明知识管理预留接口路径", () => {
  assert.equal(RESERVED_ENDPOINTS.loadState, "GET /api/knowledge/state");
  assert.equal(RESERVED_ENDPOINTS.persistState, "PUT /api/knowledge/state");
  assert.equal(RESERVED_ENDPOINTS.parseUpload, "POST /api/knowledge/parse");
  assert.equal(RESERVED_ENDPOINTS.includeItem, "POST /api/knowledge/items/{id}/include");
  assert.equal(RESERVED_ENDPOINTS.updateItem, "PUT /api/knowledge/items/{id}");
});

test("后端不可用时 service 使用本地存储兜底", async () => {
  const memory = createMemoryStorage();
  const service = createKnowledgeService({
    storage: memory,
    fetchImpl: async () => {
      throw new Error("backend offline");
    },
  });

  const state = await service.loadState();
  assert.equal(state.records.length, 34);

  const saved = await service.persistState({ ...state, route: "add" });
  assert.equal(saved.route, "add");
  assert.equal(JSON.parse(memory.getItem("knowledge_management_webui_state_v1")).route, "add");
});

test("解析上传使用真实 FormData 并传递资产和客户元数据", async () => {
  let capturedUrl = "";
  let capturedOptions = null;
  const service = createKnowledgeService({
    storage: createMemoryStorage(),
    fetchImpl: async (url, options) => {
      capturedUrl = url;
      capturedOptions = options;
      return {
        ok: true,
        async json() {
          return { fileName: "会议录音.m4a", fullText: "真实转录", knowledgeItems: [] };
        },
      };
    },
  });
  const file = new Blob(["audio-bytes"], { type: "audio/mp4" });
  Object.defineProperty(file, "name", { value: "会议录音.m4a" });

  const parsed = await service.parseUpload(file, { assetTypeId: "asset-1", customerId: 9 });

  assert.equal(capturedUrl, "/api/knowledge/parse");
  assert.equal(capturedOptions.method, "POST");
  assert.ok(capturedOptions.body instanceof FormData);
  assert.equal(capturedOptions.body.get("file").name, "会议录音.m4a");
  assert.equal(capturedOptions.body.get("asset_type_id"), "asset-1");
  assert.equal(capturedOptions.body.get("customer_id"), "9");
  assert.equal(capturedOptions.headers, undefined);
  assert.equal(parsed.fullText, "真实转录");
});

test("解析接口失败时抛出真实错误且不返回模拟成功", async () => {
  const service = createKnowledgeService({
    storage: createMemoryStorage(),
    fetchImpl: async () => ({
      ok: false,
      status: 503,
      async json() {
        return { detail: "DeepSeek service unavailable" };
      },
    }),
  });
  const file = new Blob(["audio-bytes"], { type: "audio/mp4" });
  Object.defineProperty(file, "name", { value: "会议录音.m4a" });

  await assert.rejects(
    service.parseUpload(file),
    /DeepSeek service unavailable/,
  );
});

function createMemoryStorage() {
  const store = new Map();
  return {
    getItem(key) {
      return store.has(key) ? store.get(key) : null;
    },
    setItem(key, value) {
      store.set(key, String(value));
    },
    removeItem(key) {
      store.delete(key);
    },
  };
}
