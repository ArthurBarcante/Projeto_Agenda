import { formatDateTimeInput } from "../../../utils/dateTime.js";
import { escapeHtml } from "../../../utils/escapeHtml.js";
import { renderEventCard } from "./eventCard.js";
import { renderTaskCard } from "./taskCard.js";

function renderFeedback(feedback) {
  if (!feedback?.message) return "";
  return `<div class="agenda-feedback agenda-feedback-${feedback.type}"><span>${escapeHtml(feedback.message)}</span></div>`;
}

function renderAgendaItems(items, renderer, formatDateTimeLabel, emptyMessage) {
  if (!items.length) {
    return `<div class="agenda-empty-state">${emptyMessage}</div>`;
  }

  return items.map((item) => renderer(item, { escapeHtml, formatDateTimeLabel })).join("");
}

function renderTaskItems(viewModel, formatDateTimeLabel) {
  return renderAgendaItems(
    viewModel.tasks,
    renderTaskCard,
    formatDateTimeLabel,
    "Nenhuma tarefa cadastrada ate o momento.",
  );
}

function renderEventItems(viewModel, formatDateTimeLabel) {
  return renderAgendaItems(
    viewModel.events,
    renderEventCard,
    formatDateTimeLabel,
    "Nenhum evento cadastrado ate o momento.",
  );
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

function renderAgendaFilters(state) {
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

function renderAgendaTabs(activeView) {
  return `
    <section class="agenda-tabs-wrap">
      <div class="agenda-tabs" role="tablist" aria-label="Visualizacoes da agenda">
        <span class="agenda-tabs-indicator agenda-tabs-indicator-${activeView}" aria-hidden="true"></span>
        <button
          type="button"
          role="tab"
          aria-selected="${activeView === "calendar"}"
          class="agenda-tab ${activeView === "calendar" ? "agenda-tab-active" : ""}"
          data-view="calendar"
        >
          Calendario
        </button>
        <button
          type="button"
          role="tab"
          aria-selected="${activeView === "commitments"}"
          class="agenda-tab ${activeView === "commitments" ? "agenda-tab-active" : ""}"
          data-view="commitments"
        >
          Compromissos
        </button>
      </div>
    </section>
  `;
}

function renderCommitmentsPanel(state, formatDateTimeLabel) {
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
        <div class="agenda-list">${renderSectionState(state.tasksError, renderTaskItems(state.viewModel, formatDateTimeLabel))}</div>
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
        <div class="agenda-list">${renderSectionState(state.eventsError, renderEventItems(state.viewModel, formatDateTimeLabel))}</div>
      </section>
    </div>
  `;
}

function renderCalendarPanel(calendar) {
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

function renderAgendaContent(state, formatDateTimeLabel) {
  return `
    <section class="agenda-view-shell">
      <div class="agenda-view-track agenda-view-track-${state.activeView}">
        <div class="agenda-view-panel agenda-view-panel-calendar">
          ${renderCalendarPanel(state.viewModel.calendar)}
        </div>
        <div class="agenda-view-panel agenda-view-panel-commitments">
          ${renderCommitmentsPanel(state, formatDateTimeLabel)}
        </div>
      </div>
    </section>
  `;
}

export function renderAgendaPage({ state, formatDateTimeLabel, sidebarMarkup }) {
  return `
    <div class="dashboard-page fade-in agenda-page">
      <button type="button" class="dashboard-menu-toggle" id="dashboard-menu-toggle" aria-label="Abrir menu">☰</button>
      ${renderFeedback(state.feedback)}
      ${state.mockMode ? renderMockModeState() : `
        ${renderAgendaFilters(state)}
        ${renderAgendaTabs(state.activeView)}
        ${state.loading ? `
          <section class="dashboard-state"><div class="dashboard-state-card"><div class="dashboard-spinner"></div><h2>Carregando sua agenda</h2><p>Buscando tarefas e eventos autenticados no backend.</p></div></section>
        ` : renderAgendaContent(state, formatDateTimeLabel)}
      `}
      ${sidebarMarkup}
    </div>
  `;
}
