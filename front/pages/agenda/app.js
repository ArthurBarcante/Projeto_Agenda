import { createEvent, deleteEvent, listEvents, updateEvent } from "../../api/events.js";
import { createTask, deleteTask, listTasks, updateTask } from "../../api/tasks.js";
import { initializeSidebar, renderSidebar, resetSidebarState } from "../../components/sidebar/app.js";
import { consumeAgendaFlashMessage } from "../../utils/agendaFlash.js";
import { setAuthMode } from "../../utils/auth.js";
import { isMockMode } from "../../utils/config.js";
import { formatDateTimeLabel, toApiDateTime } from "../../utils/dateTime.js";
import { buildAgendaViewModel, createAgendaStateSnapshot } from "./modules/agenda.js";
import { buildCalendarModel, mapAgendaItemsToCalendar } from "./modules/calendar.js";
import { filterEvents, filterTasks, sortAgendaItems } from "./modules/filters.js";
import { renderAgendaPage } from "./modules/render.js";
import { createAgendaState, createEmptyEventForm, createEmptyTaskForm } from "./modules/state.js";

const root = document.getElementById("agenda-root");

const state = createAgendaState({ mockMode: isMockMode() });

function setFeedback(type, message) {
  state.feedback = message ? { message, type } : null;
}

function handleErrorAndRender(feedback, renderFn) {
  setFeedback(feedback.type, feedback.message);
  renderFn();
}

function normalizeTextValue(value) {
  const normalizedValue = value.trim();
  return normalizedValue ? normalizedValue : null;
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
  root.innerHTML = renderAgendaPage({
    state,
    formatDateTimeLabel,
    sidebarMarkup: renderSidebar(),
  });
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
    handleErrorAndRender({ type: "error", message: "Informe um titulo para a tarefa." }, renderAgenda);
    return;
  }

  const wasEditing = Boolean(state.editingTaskId);

  try {
    if (state.editingTaskId) await updateTask(state.editingTaskId, payload);
    else await createTask(payload);

    resetTaskForm();
    await loadAgendaData({ type: "success", message: wasEditing ? "Tarefa atualizada com sucesso." : "Tarefa criada com sucesso." });
  } catch (error) {
    handleErrorAndRender({ type: "error", message: error.message || "Nao foi possivel salvar a tarefa." }, renderAgenda);
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
    handleErrorAndRender({ type: "error", message: "Preencha titulo e inicio do evento." }, renderAgenda);
    return;
  }

  if (payload.end_at && payload.end_at < payload.start_at) {
    handleErrorAndRender({ type: "error", message: "O fim do evento nao pode ser anterior ao inicio." }, renderAgenda);
    return;
  }

  const wasEditing = Boolean(state.editingEventId);

  try {
    if (state.editingEventId) await updateEvent(state.editingEventId, payload);
    else await createEvent(payload);

    resetEventForm();
    await loadAgendaData({ type: "success", message: wasEditing ? "Evento atualizado com sucesso." : "Evento criado com sucesso." });
  } catch (error) {
    handleErrorAndRender({ type: "error", message: error.message || "Nao foi possivel salvar o evento." }, renderAgenda);
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
      handleErrorAndRender({ type: "error", message: error.message || "Nao foi possivel atualizar a tarefa." }, renderAgenda);
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
      handleErrorAndRender({ type: "error", message: error.message || "Nao foi possivel excluir a tarefa." }, renderAgenda);
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
      handleErrorAndRender({ type: "error", message: error.message || "Nao foi possivel excluir o evento." }, renderAgenda);
    }
  }
}

void loadAgendaData();
