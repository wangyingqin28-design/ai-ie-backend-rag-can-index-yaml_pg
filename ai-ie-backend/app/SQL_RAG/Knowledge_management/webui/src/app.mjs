import {
  attachKnowledgeFile,
  backToKnowledgeList,
  closeSidePanel,
  completeKnowledgeParsing,
  discardKnowledgeItem,
  includeAllKnowledgeItems,
  includeKnowledgeItem,
  listKnowledgeRecords,
  openAddKnowledge,
  openEditKnowledgePanel,
  openFullTextPanel,
  saveKnowledgeEdit,
  selectAddSourceTab,
  SOURCE_TABS,
  updateAddKnowledgeField,
  updateKnowledgeEditDraft,
} from "./knowledgeStore.mjs";
import { knowledgeService } from "./knowledgeService.mjs";
import {
  buildCalendarMonths,
  isDateInRange,
  isDateSelected,
  selectDateRange,
} from "./uiControls.mjs";

const app = document.getElementById("app");
const fileInput = document.getElementById("hiddenFileInput");

let state = await knowledgeService.loadState();
let uiState = {
  openSelectId: null,
  calendarOpen: false,
  // [2026-07-04 10:18:20] 作用：保存本次真实解析错误文本；理由依据：后端失败必须在页面明确显示而非伪造成功。
  parseError: null,
};

render();

document.addEventListener("click", handleClick);
document.addEventListener("input", handleInput);
document.addEventListener("change", handleChange);
fileInput.addEventListener("change", async (event) => {
  const [file] = Array.from(event.target.files || []);
  if (file) {
    await parseSelectedFile(file);
  }
  event.target.value = "";
});

document.addEventListener("dragover", (event) => {
  if (event.target.closest("[data-drop-zone]")) {
    event.preventDefault();
  }
});

document.addEventListener("drop", async (event) => {
  if (!event.target.closest("[data-drop-zone]")) {
    return;
  }
  event.preventDefault();
  const [file] = Array.from(event.dataTransfer?.files || []);
  if (file) {
    await parseSelectedFile(file);
  }
});

async function handleClick(event) {
  const actionElement = event.target.closest("[data-action]");
  if (!actionElement) {
    if (!event.target.closest(".custom-select") && !event.target.closest(".date-filter")) {
      uiState.openSelectId = null;
      uiState.calendarOpen = false;
      render();
    }
    return;
  }
  const { action, id, tab } = actionElement.dataset;

  if (action === "newKnowledge") {
    await commit(openAddKnowledge(state));
    return;
  }
  if (action === "backList") {
    await commit(backToKnowledgeList(state));
    return;
  }
  if (action === "search") {
    const keyword = document.getElementById("filterKeyword")?.value || "";
    await commit({
      ...state,
      filters: { ...state.filters, keyword },
    });
    return;
  }
  if (action === "clearFilters") {
    await commit({
      ...state,
      filters: {
        keyword: "",
        marker: "",
        startTime: "",
        endTime: "",
        assetType: "全部",
        source: "全部",
        status: "全部",
      },
    });
    return;
  }
  if (action === "toggleCalendar") {
    uiState.calendarOpen = !uiState.calendarOpen;
    uiState.openSelectId = null;
    render();
    return;
  }
  if (action === "pickDate") {
    uiState.openSelectId = null;
    await commit({
      ...state,
      filters: selectDateRange(state.filters, actionElement.dataset.date),
    });
    uiState.calendarOpen = true;
    render();
    return;
  }
  if (action === "toggleSelect") {
    const selectId = actionElement.dataset.selectId;
    uiState.openSelectId = uiState.openSelectId === selectId ? null : selectId;
    uiState.calendarOpen = false;
    render();
    return;
  }
  if (action === "selectOption") {
    const field = actionElement.dataset.field;
    const value = actionElement.dataset.value;
    const scope = actionElement.dataset.scope;
    uiState.openSelectId = null;
    if (scope === "filter") {
      await commit({
        ...state,
        filters: {
          ...state.filters,
          [field]: value,
        },
      });
      return;
    }
    await commit(updateAddKnowledgeField(state, field, value));
    return;
  }
  if (action === "selectSourceTab") {
    await commit(selectAddSourceTab(state, tab));
    return;
  }
  if (action === "pickFile") {
    fileInput.click();
    return;
  }
  if (action === "viewFullText") {
    await commit(openFullTextPanel(state));
    return;
  }
  if (action === "closePanel") {
    await commit(closeSidePanel(state));
    return;
  }
  if (action === "editKnowledge") {
    await commit(openEditKnowledgePanel(state, id));
    return;
  }
  if (action === "saveEdit") {
    const editingId = state.addDraft.editingKnowledgeId;
    state = saveKnowledgeEdit(state);
    if (editingId) {
      state = includeKnowledgeItem(state, editingId);
      await knowledgeService.updateItem(editingId, getKnowledgeItem(editingId));
      await knowledgeService.includeItem(editingId, getKnowledgeItem(editingId));
    }
    await commit(state);
    return;
  }
  if (action === "includeKnowledge") {
    state = includeKnowledgeItem(state, id);
    await knowledgeService.includeItem(id, getKnowledgeItem(id));
    await commit(state);
    return;
  }
  if (action === "includeAll") {
    await commit(includeAllKnowledgeItems(state));
    return;
  }
  if (action === "discardKnowledge") {
    state = discardKnowledgeItem(state, id);
    await knowledgeService.discardItem(id);
    await commit(state);
  }
}

async function handleInput(event) {
  if (event.target.matches("[data-edit-field]")) {
    state = updateKnowledgeEditDraft(state, event.target.dataset.editField, event.target.value);
  }
}

async function handleChange(event) {
  if (event.target.matches("[data-add-field]")) {
    await commit(updateAddKnowledgeField(state, event.target.dataset.addField, event.target.value));
  }
  if (event.target.matches("[data-filter-field]")) {
    await commit({
      ...state,
      filters: {
        ...state.filters,
        [event.target.dataset.filterField]: event.target.value,
      },
    });
  }
}

async function parseSelectedFile(file) {
  // [2026-07-04 10:18:20] 作用：清除上一轮解析错误；理由依据：新文件上传应拥有独立状态。
  uiState.parseError = null;
  state = attachKnowledgeFile(state, file);
  render();
  await knowledgeService.persistState(state);
  await wait(650);
  // [2026-07-04 10:18:20] 作用：开始真实上传并捕获全链路错误；理由依据：页面不得把网络、模型或数据库失败当作解析完成。
  try {
    // [2026-07-04 10:18:20] 作用：上传真实 File 对象；理由依据：knowledgeService 使用 FormData 传递文件字节。
    const parsed = await knowledgeService.parseUpload(file);
    // [2026-07-04 10:18:20] 作用：仅在后端成功后进入完成状态；理由依据：知识卡片必须来自真实解析和提取结果。
    await commit(completeKnowledgeParsing(state, parsed));
  // [2026-07-04 10:18:20] 作用：捕获真实解析失败；理由依据：保留错误信息并允许用户重新选择文件。
  } catch (error) {
    // [2026-07-04 10:18:20] 作用：提取可显示的错误消息；理由依据：优先展示后端 detail，兼容非 Error 抛出值。
    uiState.parseError = error instanceof Error ? error.message : String(error);
    // [2026-07-04 10:18:20] 作用：把上传草稿恢复到可重试状态；理由依据：失败时不能继续显示“正在解析”或生成 parsed 结果。
    state = { ...state, addDraft: { ...state.addDraft, parseStatus: "idle", parsed: null } };
    // [2026-07-04 10:18:20] 作用：立即重绘错误与上传入口；理由依据：用户无需刷新即可看到失败原因并重试。
    render();
    // [2026-07-04 10:18:20] 作用：持久化失败后的非完成状态；理由依据：刷新页面后也不能出现伪解析成功。
    await knowledgeService.persistState(state);
  }
}

async function commit(nextState) {
  state = nextState;
  render();
  state = await knowledgeService.persistState(state);
  render();
}

function render() {
  app.innerHTML = `${renderTopTabs()}${state.route === "add" ? renderAddPage() : renderListPage()}`;
}

function renderTopTabs() {
  return `
    <nav class="top-tabs">
      <div class="top-tab">门户<span class="close-mark">×</span></div>
      <div class="top-tab">个人门户<span class="close-mark">×</span></div>
      <div class="top-tab active">知识管理<span class="close-mark">×</span></div>
    </nav>
  `;
}

function renderListPage() {
  const page = listKnowledgeRecords(state, {
    query: state.filters.keyword,
    assetType: state.filters.assetType,
    source: state.filters.source,
    status: state.filters.status,
    page: 1,
    pageSize: 20,
  });
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
}

function renderRecordRow(record) {
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
}

function renderAddPage() {
  const draft = state.addDraft;
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
}

function renderSourcePanel(draft) {
  if (draft.sourceTab !== "upload") {
    return `<div class="reserved-panel">${escapeHtml(SOURCE_TABS.find((tab) => tab.id === draft.sourceTab)?.label || "")}接口和页面区域已预留，可接入后端数据源。</div>`;
  }
  if (draft.parseStatus === "idle") {
    return `
      <button class="upload-empty" data-action="pickFile" data-drop-zone="true">
        <img src="${icon("点击拖拽文件上传插件.png")}" alt="点击或将文件拖拽到此处上传">
      </button>
    `;
  }
  if (draft.parseStatus === "parsing") {
    return `
      ${renderUploadedFile(draft)}
      <div class="parse-row"><img class="parse-spinner-img" src="${icon("正在解析图标.png")}" alt=""><span>正在解析中...</span></div>
    `;
  }
  return renderParsedResult(draft);
}

function renderUploadedFile(draft) {
  return `
    <div class="uploaded-file">
      <div>
        <div class="uploaded-file-title">${escapeHtml(draft.file?.name || "盖特箱包采购入库单如何反审会议讨论.mp4")}</div>
        <div class="uploaded-file-size">${escapeHtml(draft.file?.sizeLabel || "2.3M")}</div>
      </div>
      <img src="${icon("需解析的文件实例图标.png")}" alt="">
    </div>
  `;
}

function renderParsedResult(draft) {
  const parsed = draft.parsed;
  const hasPanel = Boolean(draft.sidePanel);
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
}

function renderAnalysisBlock(block) {
  return `
    <article class="analysis-card">
      <div class="analysis-head"><img src="${icon(block.icon)}" alt="">${escapeHtml(block.title)}</div>
      <div>${escapeHtml(block.content)} <button class="link" data-action="viewFullText">查看全部</button></div>
    </article>
  `;
}

function renderKnowledgeCard(item, index) {
  const statusText = item.status === "included" ? "已纳入" : item.status === "discarded" ? "已放弃" : "";
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
}

function renderSidePanel(draft) {
  if (draft.sidePanel === "fullText") {
    return `
      <aside class="side-panel">
        <div class="side-title">
          <span>全文内容</span>
          <span class="side-tools"><button class="text-button">导出</button><button class="text-button">分享</button><button class="text-button">更多</button></span>
        </div>
        <div class="full-text">${escapeHtml(draft.parsed.fullText)}</div>
      </aside>
    `;
  }
  const edit = draft.editDraft || { title: "", marker: "", body: "" };
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
}

function renderCalendarPopover() {
  const months = buildCalendarMonths(2025, 6, 2);
  const weekDays = ["日", "一", "二", "三", "四", "五", "六"];
  return `
    <div class="calendar-popover">
      ${months.map((month, index) => `
        <section class="calendar-month">
          <header class="calendar-month-head">
            <button class="calendar-nav" type="button"><img src="${icon(index === 0 ? "日期回退.png" : "日期前进.png")}" alt=""></button>
            <strong>${month.label}</strong>
            <button class="calendar-nav" type="button"><img src="${icon(index === 0 ? "日期回退.png" : "日期前进.png")}" alt=""></button>
          </header>
          <div class="calendar-weekdays">${weekDays.map((day) => `<span>${day}</span>`).join("")}</div>
          <div class="calendar-grid">
            ${month.weeks.flat().map((day) => renderCalendarDay(day)).join("")}
          </div>
        </section>
      `).join("")}
    </div>
  `;
}

function renderCalendarDay(day) {
  const selected = isDateSelected(state.filters, day.date);
  const inRange = isDateInRange(state.filters, day.date);
  return `
    <button
      class="calendar-day ${day.inMonth ? "" : "outside"} ${selected ? "selected" : ""} ${inRange ? "in-range" : ""}"
      data-action="pickDate"
      data-date="${escapeHtml(day.date)}"
      type="button"
    >${day.day}</button>
  `;
}

function renderCustomSelect(scope, field, selected, options) {
  const selectId = `${scope}-${field}`;
  const isOpen = uiState.openSelectId === selectId;
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
        <div class="custom-select-menu">
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
        </div>
      ` : ""}
    </div>
  `;
}

function renderAudioBar() {
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
}

function renderStatus(status) {
  const className = status === "在用" ? "active" : status === "待审" ? "pending" : "disabled";
  return `<span class="status-pill ${className}">${escapeHtml(status)}</span>`;
}

function renderOptions(options, selected) {
  return options.map((option) => `<option value="${escapeHtml(option)}" ${option === selected ? "selected" : ""}>${escapeHtml(option)}</option>`).join("");
}

function getKnowledgeItem(id) {
  return state.addDraft?.parsed?.knowledgeItems?.find((item) => item.id === id) || null;
}

function icon(name) {
  return `./icons/${name}`;
}

function wait(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
