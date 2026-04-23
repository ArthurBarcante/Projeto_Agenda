import { escapeHtml } from "../../utils/escapeHtml.js";

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

function renderFieldError(formErrors, fieldName) {
  const errorMessage = formErrors[fieldName];
  return `
    <small class="profile-field-error ${errorMessage ? "profile-field-error-visible" : ""}" data-field-error="${fieldName}">
      ${escapeHtml(errorMessage || "")}
    </small>
  `;
}

function renderFeedback(feedback) {
  if (!feedback?.message) {
    return "";
  }

  return `
    <div class="profile-feedback profile-feedback-${feedback.type}" role="status" aria-live="polite">
      <strong>${escapeHtml(feedback.title || "Atualizacao")}</strong>
      <span>${escapeHtml(feedback.message)}</span>
    </div>
  `;
}

function renderReadonlyHighlights({ loading, mockMode, user, lastSyncLabel }) {
  return `
    <div class="profile-highlight-grid">
      <article class="profile-highlight-card">
        <span>Status da conta</span>
        <strong>${mockMode ? "Modo mock" : "Conta autenticada"}</strong>
        <p>${mockMode ? "Alteracoes reais exigem o backend ativo." : "Os dados abaixo sao carregados a partir do seu JWT."}</p>
      </article>
      <article class="profile-highlight-card">
        <span>Ultima sincronizacao</span>
        <strong>${escapeHtml(lastSyncLabel)}</strong>
        <p>${loading ? "Atualizando dados agora." : "Perfil sincronizado com o backend."}</p>
      </article>
      <article class="profile-highlight-card">
        <span>Identidade</span>
        <strong>${escapeHtml(user.role || "Usuario")}</strong>
        <p>${escapeHtml(user.email || "Sem email cadastrado")}</p>
      </article>
    </div>
  `;
}

function renderDadosTab({ state, formatBirthdateInput, formatBirthdateLabel, lastSyncLabel }) {
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
            ${renderFieldError(state.formErrors, "name")}
          </label>
          <label>
            <span>Email</span>
            <input type="email" name="email" value="${escapeHtml(user.email || "")}" autocomplete="email" aria-invalid="${state.formErrors.email ? "true" : "false"}" required>
            <small class="profile-field-hint">Usado como identificador de login da sua conta.</small>
            ${renderFieldError(state.formErrors, "email")}
          </label>
          <label>
            <span>Telefone</span>
            <input type="tel" name="phone" value="${escapeHtml(user.phone || "")}" autocomplete="tel" aria-invalid="${state.formErrors.phone ? "true" : "false"}" required>
            <small class="profile-field-hint">Informe DDD e numero para manter seu cadastro consistente.</small>
            ${renderFieldError(state.formErrors, "phone")}
          </label>
          <label>
            <span>Data de nascimento</span>
            <input type="date" name="birthdate" value="${escapeHtml(formatBirthdateInput(user.birthdate))}" autocomplete="bday" aria-invalid="${state.formErrors.birthdate ? "true" : "false"}" required>
            <small class="profile-field-hint">A data e mantida no backend e refletida no seu perfil.</small>
            ${renderFieldError(state.formErrors, "birthdate")}
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

      ${renderReadonlyHighlights({ loading: state.loading, mockMode: state.mockMode, user, lastSyncLabel })}

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

function renderProgressTab(progressDetail) {
  if (!progressDetail) {
    return `
      <section class="dashboard-main profile-panel">
        <div class="profile-loading"><div class="dashboard-spinner"></div><p>Carregando progresso...</p></div>
      </section>
    `;
  }

  const completionRate = Number(progressDetail.progress || 0);
  const completedTasks = Number(progressDetail.completed_tasks || 0);
  const streak = Number(progressDetail.streak || 0);
  const bestStreak = Number(progressDetail.best_streak || 0);
  const accountLevel = Number(progressDetail.account_level || 1);
  const currentXp = Number(progressDetail.current_xp || 0);
  const xpToNextLevel = Math.max(1, Number(progressDetail.xp_to_next_level || 100));
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

function renderBadgesTab(progressDetail) {
  if (!progressDetail) {
    return `
      <section class="dashboard-main profile-panel">
        <div class="profile-loading"><div class="dashboard-spinner"></div><p>Carregando conquistas...</p></div>
      </section>
    `;
  }

  const badges = Array.isArray(progressDetail.badges) ? progressDetail.badges : [];

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

function renderProfileContent({ activeTab, dadosTabMarkup, progressTabMarkup, badgesTabMarkup }) {
  return `
    <div class="profile-layout">
      <section class="profile-view-shell">
        <div class="profile-view-track profile-view-track-${activeTab}">
          <div class="profile-view-panel">
            ${dadosTabMarkup}
          </div>
          <div class="profile-view-panel">
            ${progressTabMarkup}
          </div>
          <div class="profile-view-panel">
            ${badgesTabMarkup}
          </div>
        </div>
      </section>
    </div>
  `;
}

export function renderProfilePage({ state, formatBirthdateInput, formatBirthdateLabel, lastSyncLabel, sidebarMarkup }) {
  const user = state.user || {};
  const initials = buildInitials(user.name, user.email);
  const dadosTabMarkup = renderDadosTab({ state, formatBirthdateInput, formatBirthdateLabel, lastSyncLabel });
  const progressTabMarkup = renderProgressTab(state.progressDetail);
  const badgesTabMarkup = renderBadgesTab(state.progressDetail);
  const activeContent = state.loading && !state.user
    ? renderLoadingPanel()
    : renderProfileContent({
      activeTab: state.activeTab,
      dadosTabMarkup,
      progressTabMarkup,
      badgesTabMarkup,
    });

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
          <small>${escapeHtml(lastSyncLabel)}</small>
        </div>
      </section>

      ${renderFeedback(state.feedback)}

      <div class="profile-tabs-wrap">
        <div class="profile-tabs" role="tablist" aria-label="Abas do perfil">
          <span class="profile-tabs-indicator profile-tabs-indicator-${state.activeTab}" aria-hidden="true"></span>
          <button type="button" role="tab" aria-selected="${state.activeTab === "dados"}" class="profile-tab ${state.activeTab === "dados" ? "profile-tab-active" : ""}" data-tab="dados">Dados</button>
          <button type="button" role="tab" aria-selected="${state.activeTab === "progress"}" class="profile-tab ${state.activeTab === "progress" ? "profile-tab-active" : ""}" data-tab="progress">Progresso</button>
          <button type="button" role="tab" aria-selected="${state.activeTab === "badges"}" class="profile-tab ${state.activeTab === "badges" ? "profile-tab-active" : ""}" data-tab="badges">Conquistas</button>
        </div>
      </div>

      ${activeContent}

      ${sidebarMarkup}
    </div>
  `;
}
