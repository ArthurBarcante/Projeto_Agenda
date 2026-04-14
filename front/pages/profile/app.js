import { getProgressByUserId } from "../../api/progress.js";
import { getCurrentUserProfile, updateCurrentUserProfile } from "../../api/users.js";
import { initializeSidebar, renderSidebar, resetSidebarState } from "../../components/sidebar/app.js";
import { isMockMode } from "../../utils/config.js";
import { getStoredUser, saveSession } from "../../utils/session.js";
import {
  formatBirthdateInput,
  formatBirthdateLabel,
  validateProfilePayload,
} from "./validation.mjs";

const root = document.getElementById("profile-root");

const state = {
  activeTab: "dados",
  editMode: false,
  feedback: null,
  formErrors: {},
  lastSyncedAt: null,
  loading: true,
  mockMode: isMockMode(),
  progressDetail: null,
  saving: false,
  user: getStoredUser(),
};

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function buildInitials(name, email) {
  const source = name || email || "AI";
  return source
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() || "")
    .join("") || "AI";
}

function getBadgeEmoji(badgeName = "") {
  const name = badgeName.toLowerCase();
  if (name.includes("consistente") || name.includes("streak")) return "🔥";
  if (name.includes("veterano") || name.includes("50")) return "🏆";
  if (name.includes("iniciante") || name.includes("primeira")) return "🌱";
  return "⭐";
}

function formatLastSyncLabel() {
  if (!state.lastSyncedAt) {
    return state.mockMode ? "Modo mock" : "Aguardando sincronizacao";
  }

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(state.lastSyncedAt);
}

function renderFeedback() {
  if (!state.feedback?.message) {
    return "";
  }

  return `
    <div class="profile-feedback profile-feedback-${state.feedback.type}" role="status" aria-live="polite">
      <strong>${escapeHtml(state.feedback.title || "Atualizacao")}</strong>
      <span>${escapeHtml(state.feedback.message)}</span>
    </div>
  `;
}

function renderFieldError(fieldName) {
  const errorMessage = state.formErrors[fieldName];
  return `
    <small class="profile-field-error ${errorMessage ? "profile-field-error-visible" : ""}" data-field-error="${fieldName}">
      ${escapeHtml(errorMessage || "")}
    </small>
  `;
}

function renderReadonlyHighlights(user) {
  return `
    <div class="profile-highlight-grid">
      <article class="profile-highlight-card">
        <span>Status da conta</span>
        <strong>${state.mockMode ? "Modo mock" : "Conta autenticada"}</strong>
        <p>${state.mockMode ? "Alteracoes reais exigem o backend ativo." : "Os dados abaixo sao carregados a partir do seu JWT."}</p>
      </article>
      <article class="profile-highlight-card">
        <span>Ultima sincronizacao</span>
        <strong>${escapeHtml(formatLastSyncLabel())}</strong>
        <p>${state.loading ? "Atualizando dados agora." : "Perfil sincronizado com o backend."}</p>
      </article>
      <article class="profile-highlight-card">
        <span>Identidade</span>
        <strong>${escapeHtml(user.role || "Usuario")}</strong>
        <p>${escapeHtml(user.email || "Sem email cadastrado")}</p>
      </article>
    </div>
  `;
}

function renderDadosTab() {
  const user = state.user || {};

  if (state.editMode) {
    return `
      <section class="dashboard-main profile-panel">
        <div class="profile-section-header">
          <div>
            <span class="profile-section-label">Perfil</span>
            <h2>Editar Dados</h2>
            <p class="profile-section-copy">Atualize seus dados principais. As alteracoes sao aplicadas na sua conta autenticada.</p>
          </div>
          <button type="button" data-action="refresh-profile" class="profile-edit-btn profile-edit-btn-secondary" ${state.loading || state.saving ? "disabled" : ""}>Atualizar</button>
        </div>

        <div class="profile-readonly-meta">
          <span><strong>CPF:</strong> ${escapeHtml(user.cpf || "Nao informado")}</span>
          <span><strong>Perfil:</strong> ${escapeHtml(user.role || "Nao informado")}</span>
        </div>

        <form id="profile-account-form" class="profile-account-form" novalidate>
          <label>
            <span>Nome</span>
            <input type="text" name="name" value="${escapeHtml(user.name || "")}" autocomplete="name" aria-invalid="${state.formErrors.name ? "true" : "false"}" required>
            <small class="profile-field-hint">Nome exibido nas areas autenticadas do sistema.</small>
            ${renderFieldError("name")}
          </label>
          <label>
            <span>Email</span>
            <input type="email" name="email" value="${escapeHtml(user.email || "")}" autocomplete="email" aria-invalid="${state.formErrors.email ? "true" : "false"}" required>
            <small class="profile-field-hint">Usado como identificador de login da sua conta.</small>
            ${renderFieldError("email")}
          </label>
          <label>
            <span>Telefone</span>
            <input type="tel" name="phone" value="${escapeHtml(user.phone || "")}" autocomplete="tel" aria-invalid="${state.formErrors.phone ? "true" : "false"}" required>
            <small class="profile-field-hint">Informe DDD e numero para manter seu cadastro consistente.</small>
            ${renderFieldError("phone")}
          </label>
          <label>
            <span>Data de nascimento</span>
            <input type="date" name="birthdate" value="${escapeHtml(formatBirthdateInput(user.birthdate))}" autocomplete="bday" aria-invalid="${state.formErrors.birthdate ? "true" : "false"}" required>
            <small class="profile-field-hint">A data e mantida no backend e refletida no seu perfil.</small>
            ${renderFieldError("birthdate")}
          </label>
          <div class="profile-actions-inline">
            <button type="submit" ${state.saving || state.loading ? "disabled" : ""}>${state.saving ? "Salvando alteracoes..." : "Salvar alteracoes"}</button>
            <button type="button" data-action="cancel-edit" ${state.saving ? "disabled" : ""}>Cancelar</button>
          </div>
        </form>
      </section>
    `;
  }

  return `
    <section class="dashboard-main profile-panel">
      <div class="profile-section-header">
        <div>
          <span class="profile-section-label">Perfil</span>
          <h2>Dados da conta</h2>
          <p class="profile-section-copy">Visualize seus dados atuais e entre no modo de edicao quando precisar corrigir algo.</p>
        </div>
        <div class="profile-header-actions">
          <button type="button" data-action="refresh-profile" class="profile-edit-btn profile-edit-btn-secondary" ${state.loading ? "disabled" : ""}>${state.loading ? "Atualizando..." : "Atualizar"}</button>
          <button type="button" data-action="edit-mode" class="profile-edit-btn" ${state.loading ? "disabled" : ""}>Editar</button>
        </div>
      </div>

      ${renderReadonlyHighlights(user)}

      <div class="profile-readonly-grid">
        <article>
          <span>Nome</span>
          <strong>${escapeHtml(user.name || "Nao informado")}</strong>
        </article>
        <article>
          <span>Email</span>
          <strong>${escapeHtml(user.email || "Nao informado")}</strong>
        </article>
        <article>
          <span>Telefone</span>
          <strong>${escapeHtml(user.phone || "Nao informado")}</strong>
        </article>
        <article>
          <span>Data de nascimento</span>
          <strong>${escapeHtml(formatBirthdateLabel(user.birthdate))}</strong>
        </article>
        <article>
          <span>CPF</span>
          <strong>${escapeHtml(user.cpf || "Nao informado")}</strong>
        </article>
        <article>
          <span>Perfil</span>
          <strong>${escapeHtml(user.role || "Nao informado")}</strong>
        </article>
      </div>
    </section>
  `;
}

function renderProgressTab() {
  const detail = state.progressDetail;

  if (!detail) {
    return `
      <section class="dashboard-main profile-panel">
        <div class="profile-loading"><div class="dashboard-spinner"></div><p>Carregando progresso...</p></div>
      </section>
    `;
  }

  const completionRate = Number(detail.progress || 0);
  const completedTasks = Number(detail.completed_tasks || 0);
  const streak = Number(detail.streak || 0);
  const bestStreak = Number(detail.best_streak || 0);
  const accountLevel = Number(detail.account_level || 1);
  const currentXp = Number(detail.current_xp || 0);
  const xpToNextLevel = Math.max(1, Number(detail.xp_to_next_level || 100));
  const levelProgressPercent = Math.max(0, Math.min(100, (currentXp / xpToNextLevel) * 100));

  return `
    <section class="dashboard-main profile-panel">
      <div class="profile-section-header">
        <div>
          <span class="profile-section-label">Desempenho</span>
          <h2>Progresso</h2>
        </div>
      </div>

      <div class="profile-level-block">
        <div class="profile-level-header">
          <span>Nivel</span>
          <strong>Nivel ${accountLevel}</strong>
        </div>

        <div class="profile-progress-track">
          <div class="profile-progress-bar" style="--progress:${levelProgressPercent}%"></div>
        </div>

        <p class="profile-level-xp">(${currentXp}/${xpToNextLevel} XP)</p>
      </div>

      <div class="profile-progress-metrics profile-progress-metrics-four">
        <article>
          <span>% de tarefas feitas</span>
          <strong>${completionRate.toFixed(2)}%</strong>
        </article>
        <article>
          <span>Tarefas feitas desde o inicio</span>
          <strong>${completedTasks}</strong>
        </article>
        <article>
          <span>Streak atual</span>
          <strong>${streak} dias</strong>
        </article>
        <article>
          <span>Streak maximo</span>
          <strong>${bestStreak} dias</strong>
        </article>
      </div>
    </section>
  `;
}

function renderBadgesTab() {
  const detail = state.progressDetail;

  if (!detail) {
    return `
      <section class="dashboard-main profile-panel">
        <div class="profile-loading"><div class="dashboard-spinner"></div><p>Carregando conquistas...</p></div>
      </section>
    `;
  }

  const badges = Array.isArray(detail.badges) ? detail.badges : [];

  return `
    <section class="dashboard-main profile-panel">
      <div class="profile-section-header">
        <div>
          <span class="profile-section-label">Conquistas</span>
          <h2>Conquistas</h2>
        </div>
      </div>

      ${badges.length ? `
        <div class="profile-badges-grid">
          ${badges.map((badge) => `
            <article class="profile-badge-card" title="${escapeHtml(badge.description || "")}">
              <span class="profile-badge-icon">${getBadgeEmoji(badge.name)}</span>
              <strong>${escapeHtml(badge.name)}</strong>
              <p>${escapeHtml(badge.description || "Sem descricao")}</p>
            </article>
          `).join("")}
        </div>
      ` : `
        <p class="profile-empty">Voce ainda nao desbloqueou conquistas.</p>
      `}
    </section>
  `;
}

function renderLoadingPanel() {
  return `
    <section class="dashboard-main profile-panel profile-loading-panel">
      <div class="profile-loading">
        <div class="dashboard-spinner"></div>
        <h2>Carregando perfil</h2>
        <p>Buscando seus dados autenticados e sincronizando a experiencia da conta.</p>
      </div>
    </section>
  `;
}

function renderProfileContent() {
  return `
    <div class="profile-layout">
      <section class="profile-view-shell">
        <div class="profile-view-track profile-view-track-${state.activeTab}">
          <div class="profile-view-panel">
            ${renderDadosTab()}
          </div>
          <div class="profile-view-panel">
            ${renderProgressTab()}
          </div>
          <div class="profile-view-panel">
            ${renderBadgesTab()}
          </div>
        </div>
      </section>
    </div>
  `;
}

function renderProfilePage() {
  const user = state.user || {};
  const initials = buildInitials(user.name, user.email);
  const activeContent = state.loading && !state.user ? renderLoadingPanel() : renderProfileContent();

  return `
    <div class="dashboard-page fade-in profile-page">
      <button type="button" class="dashboard-menu-toggle" id="dashboard-menu-toggle" aria-label="Abrir menu">☰</button>

      <section class="dashboard-main profile-hero">
        <div class="profile-avatar">${escapeHtml(initials)}</div>
        <div class="profile-hero-copy">
          <span class="profile-eyebrow">Perfil</span>
          <h1>${escapeHtml(user.name || "Usuario autenticado")}</h1>
          <p>Gerencie os dados da sua conta, acompanhe a sincronizacao do perfil e veja sua progressao sem sair da area autenticada.</p>
        </div>
        <div class="profile-hero-status ${state.loading ? "profile-hero-status-loading" : ""}">
          <span>${state.loading ? "Sincronizando" : "Conta pronta"}</span>
          <strong>${escapeHtml(user.email || "Sem email")}</strong>
          <small>${escapeHtml(formatLastSyncLabel())}</small>
        </div>
      </section>

      ${renderFeedback()}

      <div class="profile-tabs-wrap">
        <div class="profile-tabs" role="tablist" aria-label="Abas do perfil">
          <span class="profile-tabs-indicator profile-tabs-indicator-${state.activeTab}" aria-hidden="true"></span>
          <button type="button" role="tab" aria-selected="${state.activeTab === "dados"}" class="profile-tab ${state.activeTab === "dados" ? "profile-tab-active" : ""}" data-tab="dados">Dados</button>
          <button type="button" role="tab" aria-selected="${state.activeTab === "progress"}" class="profile-tab ${state.activeTab === "progress" ? "profile-tab-active" : ""}" data-tab="progress">Progresso</button>
          <button type="button" role="tab" aria-selected="${state.activeTab === "badges"}" class="profile-tab ${state.activeTab === "badges" ? "profile-tab-active" : ""}" data-tab="badges">Conquistas</button>
        </div>
      </div>

      ${activeContent}

      ${renderSidebar()}
    </div>
  `;
}

function setFeedback(type, message, title = "Atualizacao") {
  state.feedback = message ? { type, message, title } : null;
}

function setFormErrors(errors = {}) {
  state.formErrors = errors;
}

function clearFieldError(fieldName) {
  if (!state.formErrors[fieldName]) {
    return;
  }

  delete state.formErrors[fieldName];
  const fieldError = root?.querySelector(`[data-field-error="${fieldName}"]`);
  const input = root?.querySelector(`[name="${fieldName}"]`);

  if (fieldError) {
    fieldError.textContent = "";
    fieldError.classList.remove("profile-field-error-visible");
  }

  input?.setAttribute("aria-invalid", "false");
}

function renderProfile() {
  if (!root) {
    return;
  }

  resetSidebarState();
  root.innerHTML = renderProfilePage();
  initializeSidebar();
  bindProfileEvents();
}

async function loadProfileData(options = {}) {
  const { preserveFeedback = false } = options;

  state.loading = true;
  state.mockMode = isMockMode();
  setFormErrors({});

  if (!preserveFeedback) {
    state.feedback = null;
  }

  renderProfile();

  if (state.mockMode) {
    state.user = getStoredUser();
    state.progressDetail = {
      progress: 0,
      completed_tasks: 0,
      total_tasks: 0,
      streak: 0,
      best_streak: 0,
      badges: [],
    };
    state.lastSyncedAt = new Date();
    state.loading = false;
    setFeedback("info", "Modo mock ativo: edicao de conta e progresso detalhado exigem backend real.", "Modo de execucao");
    renderProfile();
    return;
  }

  try {
    const user = await getCurrentUserProfile();
    const progressDetail = await getProgressByUserId(user.id);

    state.user = user;
    state.progressDetail = progressDetail;
    state.lastSyncedAt = new Date();
    saveSession({ user });
    state.loading = false;
    renderProfile();
  } catch (error) {
    state.loading = false;
    setFeedback("error", error.message || "Nao foi possivel carregar os dados do perfil.", "Falha ao carregar");
    renderProfile();
  }
}

async function handleAccountSubmit(event) {
  event.preventDefault();
  if (state.mockMode || state.saving || state.loading) {
    return;
  }

  const form = event.currentTarget;
  const formData = new FormData(form);
  const validation = validateProfilePayload({
    name: formData.get("name"),
    email: formData.get("email"),
    phone: formData.get("phone"),
    birthdate: formData.get("birthdate"),
  }, state.user || {});

  if (!validation.isValid) {
    setFormErrors(validation.errors);
    setFeedback("error", "Revise os campos destacados antes de salvar.", "Validacao");
    renderProfile();
    return;
  }

  if (!validation.hasChanges) {
    setFormErrors({});
    setFeedback("info", "Nenhuma alteracao foi detectada no perfil.", "Sem mudancas");
    renderProfile();
    return;
  }

  state.saving = true;
  setFormErrors({});
  setFeedback("info", "Salvando suas alteracoes no backend...", "Sincronizando");
  renderProfile();

  try {
    const updatedUser = await updateCurrentUserProfile(validation.payload);
    state.user = updatedUser;
    state.editMode = false;
    state.lastSyncedAt = new Date();
    saveSession({ user: updatedUser });
    setFeedback("success", "Dados da conta atualizados com sucesso.", "Perfil salvo");
  } catch (error) {
    if (error.message?.toLowerCase().includes("email")) {
      setFormErrors({ email: error.message });
    }
    setFeedback("error", error.message || "Nao foi possivel atualizar seus dados.", "Falha ao salvar");
  } finally {
    state.saving = false;
    renderProfile();
  }
}

function syncProfileView() {
  root?.querySelectorAll(".profile-tab").forEach((button) => {
    const isActive = button.dataset.tab === state.activeTab;
    button.classList.toggle("profile-tab-active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });

  const indicator = root?.querySelector(".profile-tabs-indicator");
  if (indicator) {
    indicator.className = `profile-tabs-indicator profile-tabs-indicator-${state.activeTab}`;
  }

  const track = root?.querySelector(".profile-view-track");
  if (track) {
    track.classList.toggle("profile-view-track-dados", state.activeTab === "dados");
    track.classList.toggle("profile-view-track-progress", state.activeTab === "progress");
    track.classList.toggle("profile-view-track-badges", state.activeTab === "badges");
  }
}

function bindProfileEvents() {
  root?.querySelectorAll(".profile-tab").forEach((button) => {
    button.addEventListener("click", () => {
      const nextTab = button.dataset.tab;
      if (!nextTab || nextTab === state.activeTab) {
        return;
      }

      state.activeTab = nextTab;
      syncProfileView();
    });
  });

  root?.querySelector('[data-action="edit-mode"]')?.addEventListener("click", () => {
    state.editMode = true;
    setFormErrors({});
    renderProfile();
  });

  root?.querySelector('[data-action="refresh-profile"]')?.addEventListener("click", () => {
    void loadProfileData({ preserveFeedback: true });
  });

  root?.querySelector('[data-action="cancel-edit"]')?.addEventListener("click", () => {
    state.editMode = false;
    setFormErrors({});
    renderProfile();
  });

  root?.querySelector("#profile-account-form")?.addEventListener("submit", (event) => {
    void handleAccountSubmit(event);
  });

  root?.querySelectorAll("#profile-account-form input").forEach((input) => {
    input.addEventListener("input", () => {
      clearFieldError(input.name);
      if (state.feedback?.type === "error") {
        setFeedback(null, null);
      }
    });
  });

  syncProfileView();
}

void loadProfileData();