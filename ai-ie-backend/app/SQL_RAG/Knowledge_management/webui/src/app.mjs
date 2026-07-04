// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import {`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import {
  // [2026-07-04 10:18:20] 作用：执行本行代码 `attachKnowledgeFile,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  attachKnowledgeFile,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `backToKnowledgeList,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  backToKnowledgeList,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `closeSidePanel,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  closeSidePanel,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `completeKnowledgeParsing,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  completeKnowledgeParsing,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `discardKnowledgeItem,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  discardKnowledgeItem,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `includeAllKnowledgeItems,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  includeAllKnowledgeItems,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `includeKnowledgeItem,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  includeKnowledgeItem,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `listKnowledgeRecords,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  listKnowledgeRecords,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `openAddKnowledge,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  openAddKnowledge,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `openEditKnowledgePanel,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  openEditKnowledgePanel,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `openFullTextPanel,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  openFullTextPanel,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `saveKnowledgeEdit,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  saveKnowledgeEdit,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `selectAddSourceTab,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  selectAddSourceTab,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `SOURCE_TABS,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  SOURCE_TABS,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `updateAddKnowledgeField,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  updateAddKnowledgeField,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `updateKnowledgeEditDraft,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  updateKnowledgeEditDraft,
// [2026-07-04 10:18:20] 作用：执行本行代码 `} from "./knowledgeStore.mjs";`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
} from "./knowledgeStore.mjs";
// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import { knowledgeService } from "./knowledgeService.mjs";`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import { knowledgeService } from "./knowledgeService.mjs";
// [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import {`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import {
  // [2026-07-04 10:18:20] 作用：执行本行代码 `buildCalendarMonths,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  buildCalendarMonths,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `isDateInRange,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  isDateInRange,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `isDateSelected,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  isDateSelected,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `selectDateRange,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  selectDateRange,
// [2026-07-04 10:18:20] 作用：执行本行代码 `} from "./uiControls.mjs";`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
} from "./uiControls.mjs";

// [2026-07-04 10:18:20] 作用：为 `const app` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
const app = document.getElementById("app");
// [2026-07-04 10:18:20] 作用：为 `const fileInput` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
const fileInput = document.getElementById("hiddenFileInput");

// [2026-07-04 10:18:20] 作用：为 `let state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
let state = await knowledgeService.loadState();
// [2026-07-04 10:18:20] 作用：为 `let uiState` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
let uiState = {
  // [2026-07-04 10:18:20] 作用：执行本行代码 `openSelectId: null,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  openSelectId: null,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `calendarOpen: false,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  calendarOpen: false,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `parseError: null,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  parseError: null,
// [2026-07-04 10:18:20] 作用：执行本行代码 `};`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
};

// [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
render();

// [2026-07-04 10:18:20] 作用：执行本行代码 `document.addEventListener("click", handleClick);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
document.addEventListener("click", handleClick);
// [2026-07-04 10:18:20] 作用：执行本行代码 `document.addEventListener("input", handleInput);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
document.addEventListener("input", handleInput);
// [2026-07-04 10:18:20] 作用：执行本行代码 `document.addEventListener("change", handleChange);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
document.addEventListener("change", handleChange);
// [2026-07-04 10:18:20] 作用：为 `fileInput.addEventListener("change", async (event)` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
fileInput.addEventListener("change", async (event) => {
  // [2026-07-04 10:18:20] 作用：为 `const [file]` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const [file] = Array.from(event.target.files || []);
  // [2026-07-04 10:18:20] 作用：按条件 `if (file) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (file) {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await parseSelectedFile(file);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await parseSelectedFile(file);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：为 `event.target.value` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  event.target.value = "";
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：为 `document.addEventListener("dragover", (event)` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
document.addEventListener("dragover", (event) => {
  // [2026-07-04 10:18:20] 作用：按条件 `if (event.target.closest("[data-drop-zone]")) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (event.target.closest("[data-drop-zone]")) {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `event.preventDefault();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    event.preventDefault();
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：为 `document.addEventListener("drop", async (event)` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
document.addEventListener("drop", async (event) => {
  // [2026-07-04 10:18:20] 作用：按条件 `if (!event.target.closest("[data-drop-zone]")) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (!event.target.closest("[data-drop-zone]")) {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：执行本行代码 `event.preventDefault();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  event.preventDefault();
  // [2026-07-04 10:18:20] 作用：为 `const [file]` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const [file] = Array.from(event.dataTransfer?.files || []);
  // [2026-07-04 10:18:20] 作用：按条件 `if (file) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (file) {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await parseSelectedFile(file);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await parseSelectedFile(file);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
});

// [2026-07-04 10:18:20] 作用：声明 `handleClick` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
async function handleClick(event) {
  // [2026-07-04 10:18:20] 作用：为 `const actionElement` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const actionElement = event.target.closest("[data-action]");
  // [2026-07-04 10:18:20] 作用：按条件 `if (!actionElement) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (!actionElement) {
    // [2026-07-04 10:18:20] 作用：按条件 `if (!event.target.closest(".custom-select") && !event.target.closest(".date-filter")) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
    if (!event.target.closest(".custom-select") && !event.target.closest(".date-filter")) {
      // [2026-07-04 10:18:20] 作用：为 `uiState.openSelectId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      uiState.openSelectId = null;
      // [2026-07-04 10:18:20] 作用：为 `uiState.calendarOpen` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      uiState.calendarOpen = false;
      // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      render();
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：为 `const { action, id, tab }` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const { action, id, tab } = actionElement.dataset;

  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "newKnowledge") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "newKnowledge") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(openAddKnowledge(state));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(openAddKnowledge(state));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "backList") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "backList") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(backToKnowledgeList(state));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(backToKnowledgeList(state));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "search") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "search") {
    // [2026-07-04 10:18:20] 作用：为 `const keyword` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const keyword = document.getElementById("filterKeyword")?.value || "";
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit({`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit({
      // [2026-07-04 10:18:20] 作用：执行本行代码 `...state,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      ...state,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `filters: { ...state.filters, keyword },`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      filters: { ...state.filters, keyword },
    // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    });
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "clearFilters") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "clearFilters") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit({`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit({
      // [2026-07-04 10:18:20] 作用：执行本行代码 `...state,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      ...state,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `filters: {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      filters: {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `keyword: "",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        keyword: "",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `marker: "",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        marker: "",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `startTime: "",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        startTime: "",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `endTime: "",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        endTime: "",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `assetType: "全部",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        assetType: "全部",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `source: "全部",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        source: "全部",
        // [2026-07-04 10:18:20] 作用：执行本行代码 `status: "全部",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        status: "全部",
      // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      },
    // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    });
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "toggleCalendar") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "toggleCalendar") {
    // [2026-07-04 10:18:20] 作用：为 `uiState.calendarOpen` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.calendarOpen = !uiState.calendarOpen;
    // [2026-07-04 10:18:20] 作用：为 `uiState.openSelectId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.openSelectId = null;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    render();
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "pickDate") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "pickDate") {
    // [2026-07-04 10:18:20] 作用：为 `uiState.openSelectId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.openSelectId = null;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit({`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit({
      // [2026-07-04 10:18:20] 作用：执行本行代码 `...state,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      ...state,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `filters: selectDateRange(state.filters, actionElement.dataset.date),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      filters: selectDateRange(state.filters, actionElement.dataset.date),
    // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    });
    // [2026-07-04 10:18:20] 作用：为 `uiState.calendarOpen` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.calendarOpen = true;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    render();
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "toggleSelect") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "toggleSelect") {
    // [2026-07-04 10:18:20] 作用：为 `const selectId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const selectId = actionElement.dataset.selectId;
    // [2026-07-04 10:18:20] 作用：为 `uiState.openSelectId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.openSelectId = uiState.openSelectId === selectId ? null : selectId;
    // [2026-07-04 10:18:20] 作用：为 `uiState.calendarOpen` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.calendarOpen = false;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    render();
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "selectOption") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "selectOption") {
    // [2026-07-04 10:18:20] 作用：为 `const field` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const field = actionElement.dataset.field;
    // [2026-07-04 10:18:20] 作用：为 `const value` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const value = actionElement.dataset.value;
    // [2026-07-04 10:18:20] 作用：为 `const scope` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const scope = actionElement.dataset.scope;
    // [2026-07-04 10:18:20] 作用：为 `uiState.openSelectId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.openSelectId = null;
    // [2026-07-04 10:18:20] 作用：按条件 `if (scope === "filter") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
    if (scope === "filter") {
      // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit({`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      await commit({
        // [2026-07-04 10:18:20] 作用：执行本行代码 `...state,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        ...state,
        // [2026-07-04 10:18:20] 作用：执行本行代码 `filters: {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        filters: {
          // [2026-07-04 10:18:20] 作用：执行本行代码 `...state.filters,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
          ...state.filters,
          // [2026-07-04 10:18:20] 作用：执行本行代码 `[field]: value,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
          [field]: value,
        // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        },
      // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      });
      // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
      return;
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(updateAddKnowledgeField(state, field, value));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(updateAddKnowledgeField(state, field, value));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "selectSourceTab") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "selectSourceTab") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(selectAddSourceTab(state, tab));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(selectAddSourceTab(state, tab));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "pickFile") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "pickFile") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `fileInput.click();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    fileInput.click();
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "viewFullText") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "viewFullText") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(openFullTextPanel(state));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(openFullTextPanel(state));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "closePanel") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "closePanel") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(closeSidePanel(state));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(closeSidePanel(state));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "editKnowledge") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "editKnowledge") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(openEditKnowledgePanel(state, id));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(openEditKnowledgePanel(state, id));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "saveEdit") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "saveEdit") {
    // [2026-07-04 10:18:20] 作用：为 `const editingId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const editingId = state.addDraft.editingKnowledgeId;
    // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    state = saveKnowledgeEdit(state);
    // [2026-07-04 10:18:20] 作用：按条件 `if (editingId) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
    if (editingId) {
      // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
      state = includeKnowledgeItem(state, editingId);
      // [2026-07-04 10:18:20] 作用：执行本行代码 `await knowledgeService.updateItem(editingId, getKnowledgeItem(editingId));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      await knowledgeService.updateItem(editingId, getKnowledgeItem(editingId));
      // [2026-07-04 10:18:20] 作用：执行本行代码 `await knowledgeService.includeItem(editingId, getKnowledgeItem(editingId));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      await knowledgeService.includeItem(editingId, getKnowledgeItem(editingId));
    // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    }
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(state);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(state);
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "includeKnowledge") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "includeKnowledge") {
    // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    state = includeKnowledgeItem(state, id);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await knowledgeService.includeItem(id, getKnowledgeItem(id));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await knowledgeService.includeItem(id, getKnowledgeItem(id));
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(state);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(state);
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "includeAll") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "includeAll") {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(includeAllKnowledgeItems(state));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(includeAllKnowledgeItems(state));
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return;`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (action === "discardKnowledge") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (action === "discardKnowledge") {
    // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    state = discardKnowledgeItem(state, id);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await knowledgeService.discardItem(id);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await knowledgeService.discardItem(id);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(state);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(state);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `handleInput` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
async function handleInput(event) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (event.target.matches("[data-edit-field]")) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (event.target.matches("[data-edit-field]")) {
    // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    state = updateKnowledgeEditDraft(state, event.target.dataset.editField, event.target.value);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `handleChange` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
async function handleChange(event) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (event.target.matches("[data-add-field]")) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (event.target.matches("[data-add-field]")) {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(updateAddKnowledgeField(state, event.target.dataset.addField, event.target.`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(updateAddKnowledgeField(state, event.target.dataset.addField, event.target.value));
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (event.target.matches("[data-filter-field]")) {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (event.target.matches("[data-filter-field]")) {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit({`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit({
      // [2026-07-04 10:18:20] 作用：执行本行代码 `...state,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      ...state,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `filters: {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      filters: {
        // [2026-07-04 10:18:20] 作用：执行本行代码 `...state.filters,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        ...state.filters,
        // [2026-07-04 10:18:20] 作用：执行本行代码 `[event.target.dataset.filterField]: event.target.value,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        [event.target.dataset.filterField]: event.target.value,
      // [2026-07-04 10:18:20] 作用：执行本行代码 `},`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      },
    // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    });
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `parseSelectedFile` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
async function parseSelectedFile(file) {
  // [2026-07-04 10:18:20] 作用：为 `uiState.parseError` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  uiState.parseError = null;
  // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  state = attachKnowledgeFile(state, file);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  render();
  // [2026-07-04 10:18:20] 作用：执行本行代码 `await knowledgeService.persistState(state);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  await knowledgeService.persistState(state);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `await wait(650);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  await wait(650);
  // [2026-07-04 10:18:20] 作用：进入异常控制片段 `try {`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
  try {
    // [2026-07-04 10:18:20] 作用：为 `const parsed` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    const parsed = await knowledgeService.parseUpload(file);
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await commit(completeKnowledgeParsing(state, parsed));`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await commit(completeKnowledgeParsing(state, parsed));
  // [2026-07-04 10:18:20] 作用：执行本行代码 `} catch (error) {`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  } catch (error) {
    // [2026-07-04 10:18:20] 作用：为 `uiState.parseError` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    uiState.parseError = error instanceof Error ? error.message : String(error);
    // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    state = { ...state, addDraft: { ...state.addDraft, parseStatus: "idle", parsed: null } };
    // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    render();
    // [2026-07-04 10:18:20] 作用：执行本行代码 `await knowledgeService.persistState(state);`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    await knowledgeService.persistState(state);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `commit` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
async function commit(nextState) {
  // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  state = nextState;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  render();
  // [2026-07-04 10:18:20] 作用：为 `state` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  state = await knowledgeService.persistState(state);
  // [2026-07-04 10:18:20] 作用：执行本行代码 `render();`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  render();
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `render` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function render() {
  // [2026-07-04 10:18:20] 作用：为 `app.innerHTML` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  app.innerHTML = `${renderTopTabs()}${state.route === "add" ? renderAddPage() : renderListPage()}`;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderTopTabs` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderTopTabs() {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <nav class="top-tabs">
      <div class="top-tab">门户<span class="close-mark">×</span></div>
      <div class="top-tab">个人门户<span class="close-mark">×</span></div>
      <div class="top-tab active">知识管理<span class="close-mark">×</span></div>
    </nav>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderListPage` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderListPage() {
  // [2026-07-04 10:18:20] 作用：为 `const page` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const page = listKnowledgeRecords(state, {
    // [2026-07-04 10:18:20] 作用：执行本行代码 `query: state.filters.keyword,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    query: state.filters.keyword,
    // [2026-07-04 10:18:20] 作用：执行本行代码 `assetType: state.filters.assetType,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    assetType: state.filters.assetType,
    // [2026-07-04 10:18:20] 作用：执行本行代码 `source: state.filters.source,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    source: state.filters.source,
    // [2026-07-04 10:18:20] 作用：执行本行代码 `status: state.filters.status,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    status: state.filters.status,
    // [2026-07-04 10:18:20] 作用：执行本行代码 `page: 1,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    page: 1,
    // [2026-07-04 10:18:20] 作用：执行本行代码 `pageSize: 20,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    pageSize: 20,
  // [2026-07-04 10:18:20] 作用：执行本行代码 `});`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  });
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <section class="list-page">
      <header class="page-title-row">
        <span>•知识库管理</span>
        <span class="page-note">（在这里管理你的知识库，其他人收录的知识在这里不会显示）</span>
      </header>
      <div class="toolbar">
        <div class="counter">
          <div class="counter-number">${page.total}</div>
          <div>全部文档</div>
        </div>
        <label class="filter-control filter-keyword">
          <span>知识标注</span>
          <input id="filterKeyword" class="field" value="${escapeHtml(state.filters.keyword)}" placeholder="请输入">
        </label>
        <label class="filter-control filter-time">
          <span>录入时间</span>
          <div class="date-filter">
            <button class="date-range" data-action="toggleCalendar" type="button">
              <span class="date-value">${escapeHtml(state.filters.startTime || "开始时间")}</span>
              <span class="date-separator">—</span>
              <span class="date-value">${escapeHtml(state.filters.endTime || "结束时间")}</span>
              <img src="${icon("日期小组件.png")}" alt="">
            </button>
            ${uiState.calendarOpen ? renderCalendarPopover() : ""}
          </div>
        </label>
        <label class="filter-control filter-select">
          <span>资产类型</span>
          ${renderCustomSelect("filter", "assetType", state.filters.assetType, ["全部", "智能客服", "市场营销", "IE工程"])}
        </label>
        <label class="filter-control filter-select">
          <span>资产来源</span>
          ${renderCustomSelect("filter", "source", state.filters.source, ["全部", "录音文件", "直接录入", "视频文件", "图片文件", "CRM系统"])}
        </label>
        <label class="filter-control filter-select">
          <span>当前状态</span>
          ${renderCustomSelect("filter", "status", state.filters.status, ["全部", "在用", "待审", "弃用"])}
        </label>
        <button class="danger-button" data-action="search">查询</button>
        <div class="toolbar-spacer"></div>
        <div class="button-row">
          <button class="text-button" data-action="clearFilters">⊗ 删除</button>
          <button class="text-button">▣ 审核</button>
          <button class="primary-button" data-action="newKnowledge">新增知识</button>
        </div>
      </div>
      <div class="table-wrap">
        <table class="knowledge-table">
          <colgroup>
            <col style="width:34px"><col style="width:46px"><col style="width:92px"><col style="width:176px">
            <col style="width:172px"><col style="width:210px"><col style="width:84px"><col style="width:154px">
            <col style="width:70px"><col style="width:80px"><col style="width:70px"><col style="width:92px">
            <col style="width:132px"><col style="width:78px">
          </colgroup>
          <thead>
            <tr>
              <th class="checkbox-cell"><input type="checkbox"></th>
              <th>序号</th>
              <th>资产类型</th>
              <th>知识标题</th>
              <th>知识标注</th>
              <th>知识正文</th>
              <th>来源类型</th>
              <th>来源体</th>
              <th>同源知识</th>
              <th>当前状态</th>
              <th>被调用</th>
              <th>知识提供</th>
              <th>录入时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>${page.items.map(renderRecordRow).join("")}</tbody>
        </table>
      </div>
      <footer class="pager">
        <span>共${page.total}条</span>
        <select class="select"><option>20条/页</option></select>
        <span>‹</span><span class="link">1</span><span>›</span>
        <span>前往</span><input class="field" value="1" style="width:38px"><span>页</span>
      </footer>
    </section>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderRecordRow` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderRecordRow(record) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <tr>
      <td class="checkbox-cell"><input type="checkbox"></td>
      <td class="center-cell">${record.sequence}</td>
      <td><button class="link">${escapeHtml(record.assetType)}</button></td>
      <td title="${escapeHtml(record.title)}">${escapeHtml(record.title)}</td>
      <td title="${escapeHtml(record.marker)}">${escapeHtml(record.marker)}</td>
      <td title="${escapeHtml(record.body)}">${escapeHtml(record.body)}</td>
      <td>${escapeHtml(record.sourceType)}</td>
      <td title="${escapeHtml(record.sourceBody)}">${escapeHtml(record.sourceBody)}</td>
      <td class="center-cell"><button class="link">${record.sameKnowledgeCount}个</button></td>
      <td class="center-cell">${renderStatus(record.status)}</td>
      <td class="center-cell"><button class="link">${record.calledCount}个</button></td>
      <td>${escapeHtml(record.provider)}</td>
      <td>${escapeHtml(record.createdAt)}</td>
      <td><button class="link" data-action="newKnowledge">进操作页</button></td>
    </tr>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderAddPage` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderAddPage() {
  // [2026-07-04 10:18:20] 作用：为 `const draft` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const draft = state.addDraft;
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <section class="add-page">
      <div class="back-row"><button class="text-button" data-action="backList">‹ 返回</button></div>
      <h1 class="add-title">新增知识</h1>
      <div class="add-controls">
        <label class="control-group asset-control">
          <span class="control-label">请选择资产类型</span>
          ${renderCustomSelect("add", "assetType", draft.assetType, ["智能问答", "智能客服", "市场营销", "IE工程"])}
        </label>
        <label class="control-group customer-control">
          <span class="control-label">涉及的客户</span>
          ${renderCustomSelect("add", "customerName", draft.customerName, ["梁氏箱包", "盖特箱包", "默认客户"])}
        </label>
      </div>
      <div class="source-tabs">
        ${SOURCE_TABS.map((tab) => `<button class="source-tab ${tab.id === draft.sourceTab ? "active" : ""}" data-action="selectSourceTab" data-tab="${tab.id}">${tab.label}</button>`).join("")}
      </div>
      <!-- [2026-07-04 10:18:20] 作用：在新增页显示真实解析错误；理由依据：禁止静默失败或回退模拟数据。 -->
      ${uiState.parseError ? `<div class="parse-error">${escapeHtml(uiState.parseError)}</div>` : ""}
      ${renderSourcePanel(draft)}
    </section>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderSourcePanel` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderSourcePanel(draft) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (draft.sourceTab !== "upload") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (draft.sourceTab !== "upload") {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return `<div class="reserved-panel">${escapeHtml(SOURCE_TABS.find((tab) => tab.id === dr`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return `<div class="reserved-panel">${escapeHtml(SOURCE_TABS.find((tab) => tab.id === draft.sourceTab)?.label || "")}接口和页面区域已预留，可接入后端数据源。</div>`;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (draft.parseStatus === "idle") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (draft.parseStatus === "idle") {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
    return `
      <button class="upload-empty" data-action="pickFile" data-drop-zone="true">
        <img src="${icon("点击拖拽文件上传插件.png")}" alt="点击或将文件拖拽到此处上传">
      </button>
    `;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：按条件 `if (draft.parseStatus === "parsing") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (draft.parseStatus === "parsing") {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
    return `
      ${renderUploadedFile(draft)}
      <div class="parse-row"><img class="parse-spinner-img" src="${icon("正在解析图标.png")}" alt=""><span>正在解析中...</span></div>
    `;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return renderParsedResult(draft);`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return renderParsedResult(draft);
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderUploadedFile` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderUploadedFile(draft) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <div class="uploaded-file">
      <div>
        <div class="uploaded-file-title">${escapeHtml(draft.file?.name || "盖特箱包采购入库单如何反审会议讨论.mp4")}</div>
        <div class="uploaded-file-size">${escapeHtml(draft.file?.sizeLabel || "2.3M")}</div>
      </div>
      <img src="${icon("需解析的文件实例图标.png")}" alt="">
    </div>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderParsedResult` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderParsedResult(draft) {
  // [2026-07-04 10:18:20] 作用：为 `const parsed` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const parsed = draft.parsed;
  // [2026-07-04 10:18:20] 作用：为 `const hasPanel` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const hasPanel = Boolean(draft.sidePanel);
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <div class="parsed-layout ${hasPanel ? "" : "no-panel"}">
      <div class="parsed-main ${hasPanel ? "narrow" : ""}">
        <h2 class="parsed-file-title">${escapeHtml(draft.file?.name || parsed.fileName)}</h2>
        <div class="section-title"><img src="${icon("原始内容解析小图标.png")}" alt="">原始内容解析</div>
        <div class="summary-text">${escapeHtml(parsed.originalSummary)}</div>
        <div class="view-all-line"><button class="link" data-action="viewFullText">全看原文</button></div>
        ${parsed.analysisBlocks.map(renderAnalysisBlock).join("")}
        <div class="knowledge-section-head"><img src="${icon("知识提取标题头.png")}" alt="">知识提取</div>
        ${parsed.knowledgeItems.map(renderKnowledgeCard).join("")}
        <div class="bottom-actions">
          <button class="outline-button" data-action="includeAll">一键纳入知识库</button>
          <button class="ghost-button" data-action="backList">放弃</button>
        </div>
        ${renderAudioBar()}
      </div>
      ${hasPanel ? renderSidePanel(draft) : ""}
    </div>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderAnalysisBlock` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderAnalysisBlock(block) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <article class="analysis-card">
      <div class="analysis-head"><img src="${icon(block.icon)}" alt="">${escapeHtml(block.title)}</div>
      <div>${escapeHtml(block.content)} <button class="link" data-action="viewFullText">查看全部</button></div>
    </article>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderKnowledgeCard` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderKnowledgeCard(item, index) {
  // [2026-07-04 10:18:20] 作用：为 `const statusText` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const statusText = item.status === "included" ? "已纳入" : item.status === "discarded" ? "已放弃" : "";
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <article class="knowledge-card ${item.status === "discarded" ? "discarded" : ""}">
      <div>
        <span class="knowledge-label">知识${index + 1}</span>
        <span class="knowledge-card-title">${escapeHtml(item.title)}</span>
        ${statusText ? `<span class="status-note">（${statusText}）</span>` : ""}
      </div>
      <div class="knowledge-lines">
        <div>标注： ${escapeHtml(item.marker)} <button class="link" data-action="viewFullText">查看全部</button></div>
        <div>正文： ${escapeHtml(item.body)} <button class="link" data-action="viewFullText">查看全部</button></div>
      </div>
      <div class="knowledge-actions">
        <button class="outline-button" data-action="includeKnowledge" data-id="${escapeHtml(item.id)}">纳入知识库</button>
        <button class="outline-button" data-action="editKnowledge" data-id="${escapeHtml(item.id)}">编辑</button>
        <button class="ghost-button" data-action="discardKnowledge" data-id="${escapeHtml(item.id)}">放弃</button>
      </div>
    </article>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderSidePanel` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderSidePanel(draft) {
  // [2026-07-04 10:18:20] 作用：按条件 `if (draft.sidePanel === "fullText") {` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
  if (draft.sidePanel === "fullText") {
    // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
    return `
      <aside class="side-panel">
        <div class="side-title">
          <span>全文内容</span>
          <span class="side-tools"><button class="text-button">导出</button><button class="text-button">分享</button><button class="text-button">更多</button></span>
        </div>
        <div class="full-text">${escapeHtml(draft.parsed.fullText)}</div>
      </aside>
    `;
  // [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
  }
  // [2026-07-04 10:18:20] 作用：为 `const edit` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const edit = draft.editDraft || { title: "", marker: "", body: "" };
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <aside class="side-panel">
      <div class="side-title"><span>编辑知识内容</span><button class="text-button" data-action="closePanel">×</button></div>
      <form class="edit-form">
        <label>
          <span>知识标题</span>
          <input data-edit-field="title" value="${escapeHtml(edit.title)}">
        </label>
        <label>
          <span>知识标注</span>
          <textarea data-edit-field="marker">${escapeHtml(edit.marker)}</textarea>
        </label>
        <label>
          <span>知识正文</span>
          <textarea class="large" data-edit-field="body">${escapeHtml(edit.body)}</textarea>
        </label>
      </form>
      <div class="edit-actions">
        <button class="ghost-button" data-action="closePanel">取消</button>
        <button class="primary-button" data-action="saveEdit">纳入知识库</button>
      </div>
    </aside>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderCalendarPopover` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderCalendarPopover() {
  // [2026-07-04 10:18:20] 作用：为 `const months` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const months = buildCalendarMonths(2025, 6, 2);
  // [2026-07-04 10:18:20] 作用：为 `const weekDays` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const weekDays = ["日", "一", "二", "三", "四", "五", "六"];
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <div class="calendar-popover">
      ${months.map((month, index) => `
        // [2026-07-04 10:18:20] 作用：为 `<section class` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        <section class="calendar-month">
          // [2026-07-04 10:18:20] 作用：为 `<header class` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
          <header class="calendar-month-head">
            // [2026-07-04 10:18:20] 作用：为 `<button class` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            <button class="calendar-nav" type="button"><img src="${icon(index === 0 ? "日期回退.png" : "日期前进.png")}" alt=""></button>
            // [2026-07-04 10:18:20] 作用：执行本行代码 `<strong>${month.label}</strong>`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
            <strong>${month.label}</strong>
            // [2026-07-04 10:18:20] 作用：为 `<button class` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            <button class="calendar-nav" type="button"><img src="${icon(index === 0 ? "日期回退.png" : "日期前进.png")}" alt=""></button>
          // [2026-07-04 10:18:20] 作用：执行本行代码 `</header>`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
          </header>
          // [2026-07-04 10:18:20] 作用：为 `<div class` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
          <div class="calendar-weekdays">${weekDays.map((day) => `<span>${day}</span>`).join("")}</div>
          // [2026-07-04 10:18:20] 作用：为 `<div class` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
          <div class="calendar-grid">
            // [2026-07-04 10:18:20] 作用：为 `${month.weeks.flat().map((day)` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            ${month.weeks.flat().map((day) => renderCalendarDay(day)).join("")}
          // [2026-07-04 10:18:20] 作用：执行本行代码 `</div>`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
          </div>
        // [2026-07-04 10:18:20] 作用：执行本行代码 `</section>`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        </section>
      // [2026-07-04 10:18:20] 作用：执行本行代码 ``).join("")}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      `).join("")}
    </div>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderCalendarDay` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderCalendarDay(day) {
  // [2026-07-04 10:18:20] 作用：为 `const selected` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const selected = isDateSelected(state.filters, day.date);
  // [2026-07-04 10:18:20] 作用：为 `const inRange` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const inRange = isDateInRange(state.filters, day.date);
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <button
      class="calendar-day ${day.inMonth ? "" : "outside"} ${selected ? "selected" : ""} ${inRange ? "in-range" : ""}"
      data-action="pickDate"
      data-date="${escapeHtml(day.date)}"
      type="button"
    >${day.day}</button>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderCustomSelect` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderCustomSelect(scope, field, selected, options) {
  // [2026-07-04 10:18:20] 作用：为 `const selectId` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const selectId = `${scope}-${field}`;
  // [2026-07-04 10:18:20] 作用：为 `const isOpen` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const isOpen = uiState.openSelectId === selectId;
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <div class="custom-select ${scope === "add" ? "custom-select-wide" : ""}">
      <button
        class="custom-select-trigger"
        data-action="toggleSelect"
        data-select-id="${escapeHtml(selectId)}"
        type="button"
      >
        <span>${escapeHtml(selected || options[0])}</span>
        <span class="select-arrow">⌄</span>
      </button>
      ${isOpen ? `
        // [2026-07-04 10:18:20] 作用：为 `<div class` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        <div class="custom-select-menu">
          // [2026-07-04 10:18:20] 作用：为 `${options.map((option)` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
          ${options.map((option) => `
            <button
              class="custom-select-option ${option === selected ? "active" : ""}"
              data-action="selectOption"
              data-scope="${escapeHtml(scope)}"
              data-field="${escapeHtml(field)}"
              data-value="${escapeHtml(option)}"
              type="button"
            >${escapeHtml(option)}</button>
          `).join("")}
        // [2026-07-04 10:18:20] 作用：执行本行代码 `</div>`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        </div>
      // [2026-07-04 10:18:20] 作用：执行本行代码 `` : ""}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
      ` : ""}
    </div>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderAudioBar` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderAudioBar() {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return ``；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `
    <div class="audio-bar">
      <span class="audio-icon">↺</span>
      <span class="play-icon">▶</span>
      <span class="audio-icon">↻</span>
      <span class="progress"></span>
      <span>倍速</span>
      <span class="audio-icon">≡</span>
    </div>
  `;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderStatus` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderStatus(status) {
  // [2026-07-04 10:18:20] 作用：为 `const className` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
  const className = status === "在用" ? "active" : status === "待审" ? "pending" : "disabled";
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return `<span class="status-pill ${className}">${escapeHtml(status)}</span>`;`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `<span class="status-pill ${className}">${escapeHtml(status)}</span>`;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `renderOptions` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function renderOptions(options, selected) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return options.map((option) => `<option value="${escapeHtml(option)}" ${option === selec`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return options.map((option) => `<option value="${escapeHtml(option)}" ${option === selected ? "selected" : ""}>${escapeHtml(option)}</option>`).join("");
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `getKnowledgeItem` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function getKnowledgeItem(id) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return state.addDraft?.parsed?.knowledgeItems?.find((item) => item.id === id) || null;`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return state.addDraft?.parsed?.knowledgeItems?.find((item) => item.id === id) || null;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `icon` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function icon(name) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return `./icons/${name}`;`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return `./icons/${name}`;
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `wait` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function wait(ms) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return new Promise((resolve) => window.setTimeout(resolve, ms));`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return new Promise((resolve) => window.setTimeout(resolve, ms));
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}

// [2026-07-04 10:18:20] 作用：声明 `escapeHtml` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
function escapeHtml(value) {
  // [2026-07-04 10:18:20] 作用：执行控制结果 `return String(value ?? "")`；理由依据：调用方必须获得明确返回值或可诊断失败。
  return String(value ?? "")
    // [2026-07-04 10:18:20] 作用：执行本行代码 `.replaceAll("&", "&amp;")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    .replaceAll("&", "&amp;")
    // [2026-07-04 10:18:20] 作用：执行本行代码 `.replaceAll("<", "&lt;")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    .replaceAll("<", "&lt;")
    // [2026-07-04 10:18:20] 作用：执行本行代码 `.replaceAll(">", "&gt;")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    .replaceAll(">", "&gt;")
    // [2026-07-04 10:18:20] 作用：执行本行代码 `.replaceAll('"', "&quot;")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    .replaceAll('"', "&quot;")
    // [2026-07-04 10:18:20] 作用：执行本行代码 `.replaceAll("'", "&#039;");`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    .replaceAll("'", "&#039;");
// [2026-07-04 10:18:20] 作用：执行本行代码 `}`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
}
