import { createEvent, deleteEvent, listEvents, updateEvent } from "../../api/events.js";
import { createTask, deleteTask, listTasks, updateTask } from "../../api/tasks.js";
import { initializeSidebar, renderSidebar, resetSidebarState } from "../../components/sidebar/app.js";
import { setAuthMode } from "../../utils/auth.js";
import { isMockMode } from "../../utils/config.js";
import { buildAgendaViewModel, createAgendaStateSnapshot } from "./modules/agenda.js";
import { buildCalendarModel, mapAgendaItemsToCalendar } from "./modules/calendar.js";
import { renderEventCard } from "./modules/eventCard.js";
import { createDefaultFilters, filterEvents, filterTasks, sortAgendaItems } from "./modules/filters.js";
import { renderTaskCard } from "./modules/taskCard.js";

const root = document.getElementById("agenda-root");
const AGENDA_FLASH_STORAGE_KEY = "agendaFlashMessage";

const state = {
  activeView: "calendar",
  data: {
    events: [],
    tasks: [],
  },
  editingEventId: null,
  editingTaskId: null,
  eventsError: "",
  eventForm: createEmptyEventForm(),
  feedback: null,
  filters: createDefaultFilters(),
  loading: true,
  mockMode: isMockMode(),
  sort: { by: "recent" },
  tasksError: "",
  taskForm: createEmptyTaskForm(),
  viewModel: {
    calendar: null,
    events: [],
    tasks: [],
  },
};

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function formatDateTimeLabel(value, fallback = "Sem data definida") {
  if (!value) return fallback;
  const parsedValue = new Date(value);
  if (Number.isNaN(parsedValue.getTime())) return fallback;
  return new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(parsedValue);
}

function formatDateTimeInput(value) {
  if (!value) return "";
  const parsedValue = new Date(value);
  if (Number.isNaN(parsedValue.getTime())) return "";
  const timezoneOffset = parsedValue.getTimezoneOffset() * 60000;
  return new Date(parsedValue.getTime() - timezoneOffset).toISOString().slice(0, 16);
}

function consumeAgendaFlashMessage() {
  try {
    const rawMessage = window.sessionStorage.getItem(AGENDA_FLASH_STORAGE_KEY);
    if (!rawMessage) return null;
    window.sessionStorage.removeItem(AGENDA_FLASH_STORAGE_KEY);
    return JSON.parse(rawMessage);
  } catch (error) {
    window.sessionStorage.removeItem(AGENDA_FLASH_STORAGE_KEY);
    return null;
  }
}

function renderFeedback() {
  if (!state.feedback?.message) return "";
  return `<div class="agenda-feedback agenda-feedback-${state.feedback.type}"><span>${escapeHtml(state.feedback.message)}</span></div>`;
}

function renderTaskItems() {
  const tasks = state.viewModel.tasks;
  if (!tasks.length) return '<div class="agenda-empty-state">Nenhuma tarefa cadastrada ate o momento.</div>';
  return tasks.map((task) => renderTaskCard(task, { escapeHtml, formatDateTimeLabel })).join("");
}

function renderEventItems() {
  const events = state.viewModel.events;
  if (!events.length) return '<div class="agenda-empty-state">Nenhum evento cadastrado ate o momento.</div>';
  return events.map((calendarEvent) => renderEventCard(calendarEvent, { escapeHtml, formatDateTimeLabel })).join("");
}

function renderSectionState(errorMessage, itemsMarkup) {
  if (errorMessage) return `<div class="agenda-section-error">${escapeHtml(errorMessage)}</div>`;
  return itemsMarkup;
}

function renderMockModeState() {
  return `
    <section class="dashboard-main agenda-mode-card">
      <div class="agenda-section-header"><div><h2>Modo mock ativo</h2><p>A agenda com tarefas e eventos utiliza as rotas reais do backend.</p></div></div>
      <div class="agenda-empty-state">Ative o modo real para consumir <strong>/tasks</strong> e <strong>/events</strong> com JWT.</div>
      <div class="agenda-actions-inline"><button type="button" data-action="use-real-mode">Usar backend real</button></div>
    </section>
  `;
}

function createEmptyTaskForm() {
  return { completed: false, description: "", dueDate: "", title: "" };
}

function createEmptyEventForm() {
  return { description: "", endAt: "", location: "", startAt: "", title: "" };
}

function renderAgendaFilters() {
  return `
    <section class="dashboard-main agenda-filters-panel">
      <form id="agenda-filters-form" class="agenda-filters-form" autocomplete="off">
        <label>
          <span>Buscar</span>
          <input
            type="search"
            name="text"
            placeholder="Busque por titulo, descricao ou local e pressione Enter"
            value="${escapeHtml(state.filters.text || "")}" />
        </label>
        <label>
          <span>Status das tarefas</span>
          <select name="status">
            <option value="all" ${state.filters.status === "all" ? "selected" : ""}>Todas</option>
            <option value="completed" ${state.filters.status === "completed" ? "selected" : ""}>Concluidas</option>
            <option value="pending" ${state.filters.status === "pending" ? "selected" : ""}>Pendentes</option>
          </select>
        </label>
        <label>
          <span>Ordenar por</span>
          <select name="sort_by">
            <option value="recent" ${state.sort.by === "recent" ? "selected" : ""}>Mais recente</option>
            <option value="priority" ${state.sort.by === "priority" ? "selected" : ""}>Prioridade</option>
          </select>
        </label>
        <div class="agenda-filters-actions">
          <button type="submit" class="agenda-filter-submit" aria-label="Aplicar busca e filtros">
            <i class="fas fa-search" aria-hidden="true"></i>
            <span>Buscar</span>
          </button>
        </div>
      </form>
    </section>
  `;
}

function renderAgendaTabs() {
  return `
    <section class="agenda-tabs-wrap">
      <div class="agenda-tabs" role="tablist" aria-label="Visualizacoes da agenda">
        <span class="agenda-tabs-indicator agenda-tabs-indicator-${state.activeView}" aria-hidden="true"></span>
        <button
          type="button"
          role="tab"
          aria-selected="${state.activeView === "calendar"}"
          class="agenda-tab ${state.activeView === "calendar" ? "agenda-tab-active" : ""}"
          data-view="calendar"
        >
          Calendario
        </button>
        <button
          type="button"
          role="tab"
          aria-selected="${state.activeView === "commitments"}"
          class="agenda-tab ${state.activeView === "commitments" ? "agenda-tab-active" : ""}"
          data-view="commitments"
        >
          Compromissos
        </button>
      </div>
    </section>
  `;
}

function renderCommitmentsPanel() {
  return `
    <div class="agenda-layout">
      <section class="dashboard-main agenda-panel">
        <div class="agenda-section-header"><div><span class="agenda-section-label">Tarefas</span><h2>Itens cadastrados</h2></div><span class="agenda-count">${state.viewModel.tasks.length} itens</span></div>
        ${state.editingTaskId ? `
          <form id="agenda-task-form" class="agenda-form">
            <label><span>Titulo</span><input type="text" name="title" value="${escapeHtml(state.taskForm.title)}" required></label>
            <label><span>Descricao</span><textarea name="description">${escapeHtml(state.taskForm.description)}</textarea></label>
            <div class="agenda-form-row">
              <label><span>Prazo</span><input type="datetime-local" name="due_date" value="${escapeHtml(formatDateTimeInput(state.taskForm.dueDate))}"></label>
              <label class="agenda-checkbox-field"><input type="checkbox" name="completed" ${state.taskForm.completed ? "checked" : ""}><span>Marcar como concluida</span></label>
            </div>
            <div class="agenda-actions-inline"><button type="submit">Salvar edicao</button><button type="button" class="agenda-button-secondary" data-action="cancel-task-edit">Cancelar edicao</button></div>
          </form>
        ` : ""}
        <div class="agenda-list">${renderSectionState(state.tasksError, renderTaskItems())}</div>
      </section>
      <section class="dashboard-main agenda-panel">
        <div class="agenda-section-header"><div><span class="agenda-section-label">Eventos</span><h2>Compromissos cadastrados</h2></div><span class="agenda-count">${state.viewModel.events.length} itens</span></div>
        ${state.editingEventId ? `
          <form id="agenda-event-form" class="agenda-form">
            <label><span>Titulo</span><input type="text" name="title" value="${escapeHtml(state.eventForm.title)}" required></label>
            <label><span>Descricao</span><textarea name="description">${escapeHtml(state.eventForm.description)}</textarea></label>
            <label><span>Local</span><input type="text" name="location" value="${escapeHtml(state.eventForm.location)}"></label>
            <div class="agenda-form-row">
              <label><span>Inicio</span><input type="datetime-local" name="start_at" value="${escapeHtml(formatDateTimeInput(state.eventForm.startAt))}" required></label>
              <label><span>Fim</span><input type="datetime-local" name="end_at" value="${escapeHtml(formatDateTimeInput(state.eventForm.endAt))}"></label>
            </div>
            <div class="agenda-actions-inline"><button type="submit">Salvar edicao</button><button type="button" class="agenda-button-secondary" data-action="cancel-event-edit">Cancelar edicao</button></div>
          </form>
        ` : ""}
        <div class="agenda-list">${renderSectionState(state.eventsError, renderEventItems())}</div>
      </section>
    </div>
  `;
}

function renderCalendarPanel() {
  const calendar = state.viewModel.calendar;

  if (!calendar) {
    return "";
  }

  const monthLabel = new Intl.DateTimeFormat("pt-BR", { month: "long", year: "numeric" }).format(new Date(calendar.year, calendar.month, 1));

  return `
    <section class="dashboard-main agenda-calendar-panel">
      <div class="agenda-section-header agenda-calendar-toolbar">
        <div>
          <span class="agenda-section-label">Calendario</span>
          <h2>Visao mensal (30 dias)</h2>
        </div>
        <div class="agenda-calendar-toolbar-actions">
          <span class="agenda-count agenda-calendar-month-label">${escapeHtml(monthLabel)}</span>
          <button type="button" class="agenda-calendar-add-button" data-action="go-to-create-item">
            <span aria-hidden="true">＋</span>
            <span>Adicionar item</span>
          </button>
        </div>
      </div>

      <div class="agenda-calendar-grid">
        ${calendar.days.map((day) => `
          <article class="agenda-calendar-day ${day.entryCount ? "agenda-calendar-day-active" : ""}">
            <header>
              <strong>Dia ${day.dayNumber}</strong>
              <small>${day.entryCount} item(ns)</small>
            </header>
            <div class="agenda-calendar-items">
              ${day.entries.length
      ? day.entries.map((entry) => `<span class="agenda-calendar-item agenda-calendar-item-${entry.kind}">${entry.kind === "task" ? "Tarefa" : "Evento"}: ${escapeHtml(entry.title || "Sem titulo")}</span>`).join("")
      : '<span class="agenda-calendar-empty">Sem itens</span>'}
            </div>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

function renderAgendaContent() {
  return `
    <section class="agenda-view-shell">
      <div class="agenda-view-track agenda-view-track-${state.activeView}">
        <div class="agenda-view-panel agenda-view-panel-calendar">
          ${renderCalendarPanel()}
        </div>
        <div class="agenda-view-panel agenda-view-panel-commitments">
          ${renderCommitmentsPanel()}
        </div>
      </div>
    </section>
  `;
}

function renderAgendaPage() {
  return `
    <div class="dashboard-page fade-in agenda-page">
      <button type="button" class="dashboard-menu-toggle" id="dashboard-menu-toggle" aria-label="Abrir menu">☰</button>
      ${renderFeedback()}
      ${state.mockMode ? renderMockModeState() : `
        ${renderAgendaFilters()}
        ${renderAgendaTabs()}
        ${state.loading ? `
          <section class="dashboard-state"><div class="dashboard-state-card"><div class="dashboard-spinner"></div><h2>Carregando sua agenda</h2><p>Buscando tarefas e eventos autenticados no backend.</p></div></section>
        ` : renderAgendaContent()}
      `}
      ${renderSidebar()}
    </div>
  `;
}

function setFeedback(type, message) {
  state.feedback = message ? { message, type } : null;
}

function normalizeTextValue(value) {
  const normalizedValue = value.trim();
  return normalizedValue ? normalizedValue : null;
}

function toApiDateTime(value) {
  if (!value) return null;
  const normalizedDate = new Date(value);
  if (Number.isNaN(normalizedDate.getTime())) return null;
  return normalizedDate.toISOString();
}

function resetTaskForm() {
  state.editingTaskId = null;
  state.taskForm = createEmptyTaskForm();
}

function resetEventForm() {
  state.editingEventId = null;
  state.eventForm = createEmptyEventForm();
}

function refreshAgendaViewModel() {
  const snapshot = createAgendaStateSnapshot({
    events: state.data.events,
    filters: state.filters,
    referenceDate: new Date(),
    sort: state.sort,
    tasks: state.data.tasks,
  });

  state.viewModel = buildAgendaViewModel({
    buildCalendarModel,
    filterEvents,
    filterTasks,
    mapItemsToCalendar: mapAgendaItemsToCalendar,
    snapshot,
    sortItems: sortAgendaItems,
  });
}

function renderAgenda() {
  if (!root) return;
  resetSidebarState();
  root.innerHTML = renderAgendaPage();
  initializeSidebar();
  bindAgendaEvents();
}

function syncAgendaView() {
  root?.querySelectorAll(".agenda-tab").forEach((button) => {
    const isActive = button.dataset.view === state.activeView;
    button.classList.toggle("agenda-tab-active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });

  const indicator = root?.querySelector(".agenda-tabs-indicator");
  if (indicator) {
    indicator.className = `agenda-tabs-indicator agenda-tabs-indicator-${state.activeView}`;
  }

  const track = root?.querySelector(".agenda-view-track");
  if (track) {
    track.classList.toggle("agenda-view-track-calendar", state.activeView === "calendar");
    track.classList.toggle("agenda-view-track-commitments", state.activeView === "commitments");
  }
}

async function loadAgendaData(feedback = null) {
  const nextFeedback = feedback || consumeAgendaFlashMessage();
  if (nextFeedback) setFeedback(nextFeedback.type, nextFeedback.message);
  state.mockMode = isMockMode();

  if (state.mockMode) {
    state.loading = false;
    state.data.tasks = [];
    state.data.events = [];
    state.tasksError = "";
    state.eventsError = "";
    refreshAgendaViewModel();
    renderAgenda();
    return;
  }

  state.loading = true;
  state.tasksError = "";
  state.eventsError = "";
  renderAgenda();

  try {
    const [tasks, events] = await Promise.all([listTasks(), listEvents()]);

    state.data.tasks = Array.isArray(tasks) ? tasks : [];
    state.data.events = Array.isArray(events) ? events : [];
    state.tasksError = "";
    state.eventsError = "";
  } catch (error) {
    const fallbackMessage = "Nao foi possivel carregar tarefas e eventos. Verifique API/CORS.";
    const message = error?.message || fallbackMessage;
    state.data.tasks = [];
    state.data.events = [];
    state.tasksError = message;
    state.eventsError = message;
  }

  state.loading = false;
  refreshAgendaViewModel();
  renderAgenda();
}

function bindAgendaEvents() {
  const taskForm = root?.querySelector("#agenda-task-form");
  const eventForm = root?.querySelector("#agenda-event-form");
  const filtersForm = root?.querySelector("#agenda-filters-form");

  const syncFiltersState = (event = null) => {
    event?.preventDefault?.();
    if (!filtersForm) return;

    const formData = new FormData(filtersForm);
    state.filters.text = String(formData.get("text") || "").trim();
    state.filters.status = String(formData.get("status") || "all");
    state.sort.by = String(formData.get("sort_by") || "recent");
    refreshAgendaViewModel();
    renderAgenda();
  };

  root?.querySelectorAll(".agenda-tab").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeView = button.dataset.view === "commitments" ? "commitments" : "calendar";
      syncAgendaView();
    });
  });

  root?.querySelector('[data-action="refresh-agenda"]')?.addEventListener("click", () => void loadAgendaData());
  root?.querySelectorAll('[data-action="go-to-create-item"]').forEach((button) => {
    button.addEventListener("click", () => {
      window.loadPage?.("create-item");
    });
  });
  root?.querySelector('[data-action="use-real-mode"]')?.addEventListener("click", () => {
    setAuthMode("real");
    state.mockMode = false;
    void loadAgendaData({ type: "success", message: "Modo real ativado para consultar tarefas e eventos." });
  });
  root?.querySelector('[data-action="cancel-task-edit"]')?.addEventListener("click", () => {
    resetTaskForm();
    renderAgenda();
  });
  root?.querySelector('[data-action="cancel-event-edit"]')?.addEventListener("click", () => {
    resetEventForm();
    renderAgenda();
  });

  taskForm?.addEventListener("submit", handleTaskSubmit);
  eventForm?.addEventListener("submit", handleEventSubmit);
  filtersForm?.addEventListener("submit", syncFiltersState);

  root?.querySelectorAll("[data-task-action]").forEach((button) => {
    button.addEventListener("click", () => void handleTaskAction(button.dataset.taskAction, Number(button.dataset.taskId)));
  });
  root?.querySelectorAll("[data-event-action]").forEach((button) => {
    button.addEventListener("click", () => void handleEventAction(button.dataset.eventAction, Number(button.dataset.eventId)));
  });

  syncAgendaView();
}

async function handleTaskSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);
  const payload = {
    completed: formData.get("completed") === "on",
    description: normalizeTextValue(String(formData.get("description") || "")),
    due_date: toApiDateTime(String(formData.get("due_date") || "")),
    title: String(formData.get("title") || "").trim(),
  };

  if (!payload.title) {
    setFeedback("error", "Informe um titulo para a tarefa.");
    renderAgenda();
    return;
  }

  const wasEditing = Boolean(state.editingTaskId);

  try {
    if (state.editingTaskId) await updateTask(state.editingTaskId, payload);
    else await createTask(payload);

    resetTaskForm();
    await loadAgendaData({ type: "success", message: wasEditing ? "Tarefa atualizada com sucesso." : "Tarefa criada com sucesso." });
  } catch (error) {
    setFeedback("error", error.message || "Nao foi possivel salvar a tarefa.");
    renderAgenda();
  }
}

async function handleEventSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);
  const payload = {
    description: normalizeTextValue(String(formData.get("description") || "")),
    end_at: toApiDateTime(String(formData.get("end_at") || "")),
    location: normalizeTextValue(String(formData.get("location") || "")),
    start_at: toApiDateTime(String(formData.get("start_at") || "")),
    title: String(formData.get("title") || "").trim(),
  };

  if (!payload.title || !payload.start_at) {
    setFeedback("error", "Preencha titulo e inicio do evento.");
    renderAgenda();
    return;
  }

  if (payload.end_at && payload.end_at < payload.start_at) {
    setFeedback("error", "O fim do evento nao pode ser anterior ao inicio.");
    renderAgenda();
    return;
  }

  const wasEditing = Boolean(state.editingEventId);

  try {
    if (state.editingEventId) await updateEvent(state.editingEventId, payload);
    else await createEvent(payload);

    resetEventForm();
    await loadAgendaData({ type: "success", message: wasEditing ? "Evento atualizado com sucesso." : "Evento criado com sucesso." });
  } catch (error) {
    setFeedback("error", error.message || "Nao foi possivel salvar o evento.");
    renderAgenda();
  }
}

async function handleTaskAction(action, taskId) {
  const task = state.data.tasks.find((item) => item.id === taskId);
  if (!task) return;

  if (action === "edit") {
    state.activeView = "commitments";
    state.editingTaskId = task.id;
    state.taskForm = {
      completed: !!task.completed,
      description: task.description || "",
      dueDate: task.due_date || "",
      title: task.title || "",
    };
    setFeedback(null, "");
    renderAgenda();
    return;
  }

  if (action === "toggle") {
    try {
      await updateTask(task.id, { completed: !task.completed });
      await loadAgendaData({ type: "success", message: task.completed ? "Tarefa reaberta com sucesso." : "Tarefa concluida com sucesso." });
    } catch (error) {
      setFeedback("error", error.message || "Nao foi possivel atualizar a tarefa.");
      renderAgenda();
    }
    return;
  }

  if (action === "delete") {
    if (!window.confirm(`Excluir a tarefa "${task.title}"?`)) return;
    try {
      await deleteTask(task.id);
      if (state.editingTaskId === task.id) resetTaskForm();
      await loadAgendaData({ type: "success", message: "Tarefa excluida com sucesso." });
    } catch (error) {
      setFeedback("error", error.message || "Nao foi possivel excluir a tarefa.");
      renderAgenda();
    }
  }
}

async function handleEventAction(action, eventId) {
  const calendarEvent = state.data.events.find((item) => item.id === eventId);
  if (!calendarEvent) return;

  if (action === "edit") {
    state.activeView = "commitments";
    state.editingEventId = calendarEvent.id;
    state.eventForm = {
      description: calendarEvent.description || "",
      endAt: calendarEvent.end_at || "",
      location: calendarEvent.location || "",
      startAt: calendarEvent.start_at || "",
      title: calendarEvent.title || "",
    };
    setFeedback(null, "");
    renderAgenda();
    return;
  }

  if (action === "delete") {
    if (!window.confirm(`Excluir o evento "${calendarEvent.title}"?`)) return;
    try {
      await deleteEvent(calendarEvent.id);
      if (state.editingEventId === calendarEvent.id) resetEventForm();
      await loadAgendaData({ type: "success", message: "Evento excluido com sucesso." });
    } catch (error) {
      setFeedback("error", error.message || "Nao foi possivel excluir o evento.");
      renderAgenda();
    }
  }
}

void loadAgendaData();
