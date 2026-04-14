import { createEvent } from "../../api/events.js";
import { createTask } from "../../api/tasks.js";
import { initializeSidebar, renderSidebar, resetSidebarState } from "../../components/sidebar/app.js";
import { setAuthMode } from "../../utils/auth.js";
import { isMockMode } from "../../utils/config.js";

const root = document.getElementById("create-item-root");
const AGENDA_FLASH_STORAGE_KEY = "agendaFlashMessage";

const state = {
  feedback: null,
  kind: "",
  mockMode: isMockMode(),
  submitting: false,
};

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function setFeedback(type, message) {
  state.feedback = message ? { type, message } : null;
}

function normalizeTextValue(value) {
  const normalizedValue = String(value || "").trim();
  return normalizedValue ? normalizedValue : null;
}

function toApiDateTime(value) {
  if (!value) return null;
  const normalizedDate = new Date(value);
  if (Number.isNaN(normalizedDate.getTime())) return null;
  return normalizedDate.toISOString();
}

function saveAgendaFlashMessage(message) {
  try {
    window.sessionStorage.setItem(AGENDA_FLASH_STORAGE_KEY, JSON.stringify({ type: "success", message }));
  } catch (error) {
    console.warn("Nao foi possivel salvar a mensagem de retorno da agenda.", error);
  }
}

function goToAgenda(forceReload = false) {
  if (typeof window.loadPage === "function") {
    void window.loadPage("agenda", { forceReload });
    return;
  }

  window.location.href = "./index.html#/agenda";
}

function renderFeedback() {
  if (!state.feedback?.message) return "";
  return `<div class="create-item-feedback create-item-feedback-${state.feedback.type}">${escapeHtml(state.feedback.message)}</div>`;
}

function renderSelector() {
  return `
    <section class="dashboard-main">
      <span class="dashboard-kicker">Criacao guiada</span>
      <h2>O que voce quer criar?</h2>
      <p class="create-item-hint">Escolha o tipo de item primeiro. Depois os campos corretos aparecem automaticamente.</p>
      <div class="create-item-choice">
        <article class="create-item-option ${state.kind === "task" ? "create-item-option-active" : ""}">
          <div>
            <h3>Tarefa</h3>
            <p>Ideal para itens de execucao, prazos e acompanhamento de conclusao.</p>
          </div>
          <button type="button" data-kind="task" class="${state.kind === "task" ? "create-item-button-secondary" : ""}">Selecionar tarefa</button>
        </article>
        <article class="create-item-option ${state.kind === "event" ? "create-item-option-active" : ""}">
          <div>
            <h3>Evento</h3>
            <p>Ideal para compromissos com horario, local e planejamento de agenda.</p>
          </div>
          <button type="button" data-kind="event" class="${state.kind === "event" ? "create-item-button-secondary" : ""}">Selecionar evento</button>
        </article>
      </div>
    </section>
  `;
}

function renderTaskForm() {
  return `
    <section class="dashboard-main">
      <span class="agenda-section-label">Nova tarefa</span>
      <h2>Preencha os dados da tarefa</h2>
      <form id="create-item-form" class="create-item-form">
        <input type="hidden" name="kind" value="task">
        <label>
          <span>Titulo</span>
          <input type="text" name="title" placeholder="Ex.: Revisar backlog" required>
        </label>
        <label>
          <span>Descricao</span>
          <textarea name="description" placeholder="Descreva a tarefa"></textarea>
        </label>
        <div class="create-item-form-row">
          <label>
            <span>Prazo</span>
            <input type="datetime-local" name="due_date">
          </label>
          <label class="create-item-checkbox">
            <input type="checkbox" name="completed">
            <span>Ja criar como concluida</span>
          </label>
        </div>
        <div class="create-item-actions">
          <button type="button" class="create-item-button-secondary" data-action="back-to-agenda">Cancelar</button>
          <button type="submit">${state.submitting ? "Salvando..." : "Salvar tarefa"}</button>
        </div>
      </form>
    </section>
  `;
}

function renderEventForm() {
  return `
    <section class="dashboard-main">
      <span class="agenda-section-label">Novo evento</span>
      <h2>Preencha os dados do evento</h2>
      <form id="create-item-form" class="create-item-form">
        <input type="hidden" name="kind" value="event">
        <label>
          <span>Titulo</span>
          <input type="text" name="title" placeholder="Ex.: Reuniao de alinhamento" required>
        </label>
        <label>
          <span>Descricao</span>
          <textarea name="description" placeholder="Descreva o compromisso"></textarea>
        </label>
        <label>
          <span>Local</span>
          <input type="text" name="location" placeholder="Ex.: Sala virtual ou escritorio">
        </label>
        <div class="create-item-form-row">
          <label>
            <span>Inicio</span>
            <input type="datetime-local" name="start_at" required>
          </label>
          <label>
            <span>Fim</span>
            <input type="datetime-local" name="end_at">
          </label>
        </div>
        <div class="create-item-actions">
          <button type="button" class="create-item-button-secondary" data-action="back-to-agenda">Cancelar</button>
          <button type="submit">${state.submitting ? "Salvando..." : "Salvar evento"}</button>
        </div>
      </form>
    </section>
  `;
}

function renderCreateItemPage() {
  if (!root) return;

  resetSidebarState();
  root.innerHTML = `
    <div class="dashboard-page fade-in create-item-page">
      <button type="button" class="dashboard-menu-toggle" id="dashboard-menu-toggle" aria-label="Abrir menu">☰</button>
      <section class="dashboard-main create-item-hero">
        <div>
          <span class="dashboard-kicker">Novo item</span>
          <h1>Criar tarefa ou evento</h1>
          <p>Escolha o tipo, preencha os dados e o sistema retorna voce automaticamente para a agenda.</p>
        </div>
        <div class="create-item-actions">
          <button type="button" class="create-item-button-secondary" data-action="back-to-agenda">Voltar para agenda</button>
        </div>
      </section>
      ${renderFeedback()}
      ${state.mockMode ? `
        <section class="dashboard-main">
          <h2>Modo mock ativo</h2>
          <p>Para cadastrar tarefas e eventos reais, ative o modo real primeiro.</p>
          <div class="create-item-actions">
            <button type="button" data-action="use-real-mode">Usar backend real</button>
          </div>
        </section>
      ` : `${renderSelector()}${state.kind === "task" ? renderTaskForm() : state.kind === "event" ? renderEventForm() : ""}`}
      ${renderSidebar()}
    </div>
  `;

  initializeSidebar();
  bindEvents();
}

function bindEvents() {
  root?.querySelectorAll("[data-kind]").forEach((button) => {
    button.addEventListener("click", () => {
      state.kind = button.dataset.kind || "";
      setFeedback(null, "");
      renderCreateItemPage();
    });
  });

  root?.querySelectorAll('[data-action="back-to-agenda"]').forEach((button) => {
    button.addEventListener("click", () => {
      goToAgenda();
    });
  });

  root?.querySelector('[data-action="use-real-mode"]')?.addEventListener("click", () => {
    setAuthMode("real");
    state.mockMode = false;
    setFeedback("success", "Modo real ativado. Agora voce ja pode criar itens.");
    renderCreateItemPage();
  });

  root?.querySelector("#create-item-form")?.addEventListener("submit", (event) => {
    void handleSubmit(event);
  });
}

async function handleSubmit(event) {
  event.preventDefault();

  if (state.submitting) {
    return;
  }

  const formData = new FormData(event.currentTarget);
  const kind = String(formData.get("kind") || "");

  try {
    state.submitting = true;
    setFeedback(null, "");

    let successMessage = "Item criado com sucesso. Redirecionando para a agenda...";

    if (kind === "task") {
      const payload = {
        completed: formData.get("completed") === "on",
        description: normalizeTextValue(formData.get("description")),
        due_date: toApiDateTime(String(formData.get("due_date") || "")),
        title: String(formData.get("title") || "").trim(),
      };

      if (!payload.title) {
        throw new Error("Informe um titulo para a tarefa.");
      }

      await createTask(payload);
      successMessage = "Tarefa criada com sucesso. Redirecionando para a agenda...";
    }

    if (kind === "event") {
      const payload = {
        description: normalizeTextValue(formData.get("description")),
        end_at: toApiDateTime(String(formData.get("end_at") || "")),
        location: normalizeTextValue(formData.get("location")),
        start_at: toApiDateTime(String(formData.get("start_at") || "")),
        title: String(formData.get("title") || "").trim(),
      };

      if (!payload.title || !payload.start_at) {
        throw new Error("Preencha titulo e inicio do evento.");
      }

      if (payload.end_at && payload.end_at < payload.start_at) {
        throw new Error("O fim do evento nao pode ser anterior ao inicio.");
      }

      await createEvent(payload);
      successMessage = "Evento criado com sucesso. Redirecionando para a agenda...";
    }

    if (kind !== "task" && kind !== "event") {
      throw new Error("Selecione primeiro se deseja criar uma tarefa ou um evento.");
    }

    saveAgendaFlashMessage(successMessage.replace(". Redirecionando para a agenda...", "."));
    state.submitting = false;
    state.kind = "";
    goToAgenda(true);
  } catch (error) {
    state.submitting = false;
    setFeedback("error", error?.message || "Nao foi possivel salvar o item.");
    renderCreateItemPage();
  }
}

renderCreateItemPage();
