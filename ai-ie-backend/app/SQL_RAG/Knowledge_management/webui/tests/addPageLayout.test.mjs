// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import test from "node:test";`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import test from "node:test";
// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import assert from "node:assert/strict";`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import assert from "node:assert/strict";
// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import { readFile } from "node:fs/promises";`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import { readFile } from "node:fs/promises";

// [2026-07-04 10:18:20] 作用：为 `const webuiRoot` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
const webuiRoot = new URL("../", import.meta.url);

// [2026-07-04 10:18:20] 作用：为 `test("新增知识字段标题按内容宽度展示且不会被固定列宽裁切", async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
test("新增知识字段标题按内容宽度展示且不会被固定列宽裁切", async () => {
  // [2026-07-04 10:18:20] 作用：为 `const css` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const css = await readFile(new URL("styles.css", webuiRoot), "utf8");

  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.match(`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.match(
    // [2026-07-04 10:18:20] 作用：执行本行代码 `css,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    css,
    // [2026-07-04 10:18:20] 作用：执行本行代码 `/\.control-group\s*\{[^}]*grid-template-columns:\s*max-content\s+152px;/s,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    /\.control-group\s*\{[^}]*grid-template-columns:\s*max-content\s+152px;/s,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  );
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.doesNotMatch(css, /\.asset-control\s*\{[^}]*grid-template-columns:/s);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.doesNotMatch(css, /\.asset-control\s*\{[^}]*grid-template-columns:/s);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.doesNotMatch(css, /\.customer-control\s*\{[^}]*grid-template-columns:/s);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.doesNotMatch(css, /\.customer-control\s*\{[^}]*grid-template-columns:/s);
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：为 `test("上传区直接铺满拖拽上传合成组件且不重复输出文案", async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
test("上传区直接铺满拖拽上传合成组件且不重复输出文案", async () => {
  // [2026-07-04 10:18:20] 作用：为 `const [css, appSource]` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const [css, appSource] = await Promise.all([
    // [2026-07-04 10:18:20] 作用：执行本行代码 `readFile(new URL("styles.css", webuiRoot), "utf8"),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    readFile(new URL("styles.css", webuiRoot), "utf8"),
    // [2026-07-04 10:18:20] 作用：执行本行代码 `readFile(new URL("src/app.mjs", webuiRoot), "utf8"),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    readFile(new URL("src/app.mjs", webuiRoot), "utf8"),
  // [2026-07-04 10:18:20] 作用：执行本行代码 `]);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  ]);

  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.match(css, /\.upload-empty\s*\{[^}]*padding:\s*0;/s);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.match(css, /\.upload-empty\s*\{[^}]*padding:\s*0;/s);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.match(css, /\.upload-empty img\s*\{[^}]*width:\s*100%;[^}]*height:\s*100%;/s);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.match(css, /\.upload-empty img\s*\{[^}]*width:\s*100%;[^}]*height:\s*100%;/s);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.doesNotMatch(`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.doesNotMatch(
    // [2026-07-04 10:18:20] 作用：执行本行代码 `appSource,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    appSource,
    // [2026-07-04 10:18:20] 作用：为 `/<img src` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    /<img src="\$\{icon\("点击拖拽文件上传插件\.png"\)\}" alt="">\s*<strong>/s,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  );
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：为 `test("真实解析失败时页面显示后端错误且不会完成解析状态", async ()` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
test("真实解析失败时页面显示后端错误且不会完成解析状态", async () => {
  // [2026-07-04 10:18:20] 作用：为 `const appSource` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const appSource = await readFile(new URL("src/app.mjs", webuiRoot), "utf8");

  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.match(appSource, /catch\s*\(error\)/);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.match(appSource, /catch\s*\(error\)/);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.match(appSource, /uiState\.parseError/);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.match(appSource, /uiState\.parseError/);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.match(appSource, /parse-error/);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.match(appSource, /parse-error/);
  // [2026-07-04 10:18:20] 作用：执行验收断言 `assert.match(appSource, /parseStatus:\s*"idle"/);`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
  assert.match(appSource, /parseStatus:\s*"idle"/);
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});
