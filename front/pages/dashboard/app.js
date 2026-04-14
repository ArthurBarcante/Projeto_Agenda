import { getProgress, updateDailyGoal } from "../../api/progress.js";
import { initializeSidebar, renderSidebar, resetSidebarState } from "../../components/sidebar/app.js";
import { isMockMode } from "../../utils/config.js";

const root = document.getElementById("dashboard-root");

const state = {
  feedback: null,
  loading: false,
  mockMode: isMockMode(),
  progress: null,
};

const runtime = (typeof window !== "undefined")
  ? (window.__AIGENDA_DASHBOARD_RUNTIME__ ||= {
    bootTriggered: false,
    inFlightProgressRequest: null,
    lastProgressPayload: null,
    hasAutoLoadedProgress: false,
  })
  : {
    bootTriggered: false,
    inFlightProgressRequest: null,
    lastProgressPayload: null,
    hasAutoLoadedProgress: false,
  };

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function clampPercentage(value) {
  return Math.max(0, Math.min(100, Number(value || 0)));
}

function renderFeedback(feedback) {
  if (!feedback?.message) {
    return "";
  }

  return `<div class="dashboard-feedback dashboard-feedback-${feedback.type}">${escapeHtml(feedback.message)}</div>`;
}

function renderMockState() {
  return `
    <section class="dashboard-main dashboard-product-card">
      <span class="dashboard-kicker">Progresso</span>
      <h2>Modo mock ativo</h2>
      <p>O painel de progresso usa o endpoint real <strong>/progress</strong>. Troque para modo real para ver as metricas.</p>
    </section>
  `;
}

function renderMetrics(progress) {
  const completionRate = clampPercentage(progress.completion_rate);
  const goalRate = progress.daily_goal > 0
    ? clampPercentage((progress.daily_completed_tasks / progress.daily_goal) * 100)
    : 0;

  return `
    <div class="dashboard-progress-grid">
      <article class="dashboard-main dashboard-product-card dashboard-hero-card">
        <div class="dashboard-hero-copy">
          <span class="dashboard-kicker">Produto real</span>
          <h1>Sistema de progresso</h1>
          <p>Camada funcional para medir consistencia, ritmo de execucao e aderencia a metas diarias.</p>
        </div>
        <div class="dashboard-level-badge dashboard-level-${escapeHtml(progress.level)}">
          <span>Nivel atual</span>
          <strong>${escapeHtml(progress.level)}</strong>
          <small>${progress.next_level ? `Proximo: ${escapeHtml(progress.next_level)}` : "Nivel maximo atual"}</small>
        </div>
      </article>
      <div class="dashboard-metric-row">
        <article class="dashboard-main dashboard-metric-card">
          <span>Conclusao</span>
          <strong>${completionRate}%</strong>
          <p>${progress.completed_tasks} de ${progress.total_tasks} tarefas concluidas</p>
        </article>
        <article class="dashboard-main dashboard-metric-card">
          <span>Streak</span>
          <strong>${progress.streak_days} dias</strong>
          <p>Melhor sequencia: ${progress.best_streak} dias</p>
        </article>
        <article class="dashboard-main dashboard-metric-card">
          <span>Meta diaria</span>
          <strong>${progress.daily_completed_tasks}/${progress.daily_goal}</strong>
          <p>${progress.goal_completed ? "Meta concluida hoje" : "Meta ainda em andamento"}</p>
        </article>
      </div>
      <div class="dashboard-chart-row">
        <section class="dashboard-main dashboard-chart-card">
          <div class="dashboard-section-header"><div><span class="dashboard-kicker">Grafico simples</span><h2>Progresso acumulado</h2></div></div>
          <div class="dashboard-progress-bar-group">
            <div>
              <div class="dashboard-bar-header"><span>Tarefas concluidas</span><strong>${completionRate}%</strong></div>
              <div class="dashboard-progress-bar-track"><div class="dashboard-progress-bar-fill" style="width: ${completionRate}%"></div></div>
            </div>
            <div>
              <div class="dashboard-bar-header"><span>Meta do dia</span><strong>${goalRate}%</strong></div>
              <div class="dashboard-progress-bar-track dashboard-progress-bar-track-accent"><div class="dashboard-progress-bar-fill dashboard-progress-bar-fill-accent" style="width: ${goalRate}%"></div></div>
            </div>
          </div>
        </section>
        <section class="dashboard-main dashboard-chart-card">
          <div class="dashboard-section-header"><div><span class="dashboard-kicker">Ajuste</span><h2>Meta diaria</h2></div></div>
          <form id="dashboard-goal-form" class="dashboard-goal-form">
            <label>
              <span>Quantas tarefas voce quer concluir por dia?</span>
              <input type="number" min="1" max="50" name="daily_goal" value="${progress.daily_goal}" required>
            </label>
            <div class="agenda-actions-inline">
              <button type="submit">Salvar meta</button>
              <button type="button" data-action="refresh-progress">Atualizar painel</button>
            </div>
          </form>
        </section>
      </div>
    </div>
  `;
}

function renderDashboardPage() {
  return `
    <div class="dashboard-page fade-in">
      <button type="button" class="dashboard-menu-toggle" id="dashboard-menu-toggle" aria-label="Abrir menu">☰</button>
      ${renderFeedback(state.feedback)}
      ${state.mockMode ? renderMockState() : state.loading ? `
        <section class="dashboard-state"><div class="dashboard-state-card"><div class="dashboard-spinner"></div><h2>Carregando progresso</h2><p>Buscando metricas consolidadas da sua produtividade.</p></div></section>
      ` : state.progress ? renderMetrics(state.progress) : `
        <section class="dashboard-main dashboard-product-card dashboard-main-standalone">
          <span class="dashboard-kicker">Progresso</span>
          <h1>Painel pronto para carregar</h1>
          <p>Clique em atualizar para buscar os dados de progresso no backend real.</p>
          <div class="agenda-actions-inline"><button type="button" data-action="refresh-progress">Tentar novamente</button></div>
        </section>
      `}
      ${renderSidebar()}
    </div>
  `;
}

function setFeedback(type, message) {
  state.feedback = message ? { type, message } : null;
}

function renderDashboard() {
  if (!root) return;
  resetSidebarState();
  root.innerHTML = renderDashboardPage();
  initializeSidebar();
  bindDashboardEvents();
}

async function loadDashboard(feedback = null) {
  const forceRefresh = feedback?.force === true;
  state.mockMode = isMockMode();

  if (feedback) {
    setFeedback(feedback.type, feedback.message);
  }

  if (state.mockMode) {
    state.loading = false;
    state.progress = null;
    renderDashboard();
    return;
  }

  if (!forceRefresh && runtime.lastProgressPayload) {
    state.loading = false;
    state.progress = runtime.lastProgressPayload;
    renderDashboard();
    return;
  }

  state.loading = true;
  renderDashboard();

  try {
    if (runtime.inFlightProgressRequest) {
      state.progress = await runtime.inFlightProgressRequest;
      state.loading = false;
      renderDashboard();
      return;
    }

    runtime.inFlightProgressRequest = getProgress();
    state.progress = await runtime.inFlightProgressRequest;
    runtime.lastProgressPayload = state.progress;
    runtime.hasAutoLoadedProgress = true;
    state.loading = false;
  } catch (error) {
    state.loading = false;
    state.progress = null;
    setFeedback("error", error.message || "Nao foi possivel carregar o progresso.");
  } finally {
    runtime.inFlightProgressRequest = null;
  }

  renderDashboard();
}

function bindDashboardEvents() {
  const form = root?.querySelector("#dashboard-goal-form");
  const refreshButton = root?.querySelector('[data-action="refresh-progress"]');

  refreshButton?.addEventListener("click", () => {
    void loadDashboard({ force: true });
  });

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const dailyGoal = Number(formData.get("daily_goal"));

    if (!Number.isFinite(dailyGoal) || dailyGoal < 1) {
      setFeedback("error", "Informe uma meta diaria valida.");
      renderDashboard();
      return;
    }

    try {
      state.progress = await updateDailyGoal(dailyGoal);
      runtime.lastProgressPayload = state.progress;
      setFeedback("success", "Meta diaria atualizada com sucesso.");
      renderDashboard();
    } catch (error) {
      setFeedback("error", error.message || "Nao foi possivel atualizar a meta diaria.");
      renderDashboard();
    }
  });
}

renderDashboard();

if (!runtime.bootTriggered) {
  runtime.bootTriggered = true;

  if (!runtime.hasAutoLoadedProgress) {
    void loadDashboard();
  }
} else if (runtime.lastProgressPayload) {
  state.progress = runtime.lastProgressPayload;
  renderDashboard();
}
