import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const webuiRoot = new URL("../", import.meta.url);

test("新增知识字段标题按内容宽度展示且不会被固定列宽裁切", async () => {
  const css = await readFile(new URL("styles.css", webuiRoot), "utf8");

  assert.match(
    css,
    /\.control-group\s*\{[^}]*grid-template-columns:\s*max-content\s+152px;/s,
  );
  assert.doesNotMatch(css, /\.asset-control\s*\{[^}]*grid-template-columns:/s);
  assert.doesNotMatch(css, /\.customer-control\s*\{[^}]*grid-template-columns:/s);
});

test("上传区直接铺满拖拽上传合成组件且不重复输出文案", async () => {
  const [css, appSource] = await Promise.all([
    readFile(new URL("styles.css", webuiRoot), "utf8"),
    readFile(new URL("src/app.mjs", webuiRoot), "utf8"),
  ]);

  assert.match(css, /\.upload-empty\s*\{[^}]*padding:\s*0;/s);
  assert.match(css, /\.upload-empty img\s*\{[^}]*width:\s*100%;[^}]*height:\s*100%;/s);
  assert.doesNotMatch(
    appSource,
    /<img src="\$\{icon\("点击拖拽文件上传插件\.png"\)\}" alt="">\s*<strong>/s,
  );
});

test("真实解析失败时页面显示后端错误且不会完成解析状态", async () => {
  const appSource = await readFile(new URL("src/app.mjs", webuiRoot), "utf8");

  assert.match(appSource, /catch\s*\(error\)/);
  assert.match(appSource, /uiState\.parseError/);
  assert.match(appSource, /parse-error/);
  assert.match(appSource, /parseStatus:\s*"idle"/);
});
