import { getProgressByUserId } from "../../api/progress.js";
import { getCurrentUserProfile, updateCurrentUserProfile } from "../../api/users.js";
import { initializeSidebar, renderSidebar, resetSidebarState } from "../../components/sidebar/app.js";
import { isMockMode } from "../../utils/config.js";
import { getStoredUser, saveSession } from "../../utils/session.js";
import { renderProfilePage } from "./render.js";
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

function createMockProgressDetail() {
  return {
    progress: 0,
    completed_tasks: 0,
    total_tasks: 0,
    streak: 0,
    best_streak: 0,
    badges: [],
  };
}

async function fetchProfileLoadData(mockMode) {
  if (mockMode) {
    return {
      feedback: {
        message: "Modo mock ativo: edicao de conta e progresso detalhado exigem backend real.",
        title: "Modo de execucao",
        type: "info",
      },
      progressDetail: createMockProgressDetail(),
      user: getStoredUser(),
    };
  }

  const user = await getCurrentUserProfile();
  const progressDetail = await getProgressByUserId(user.id);

  return {
    feedback: null,
    progressDetail,
    user,
  };
}

function buildAccountSubmitValidation(form, currentUser) {
  const formData = new FormData(form);
  return validateProfilePayload({
    name: formData.get("name"),
    email: formData.get("email"),
    phone: formData.get("phone"),
    birthdate: formData.get("birthdate"),
  }, currentUser || {});
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
  root.innerHTML = renderProfilePage({
    state,
    formatBirthdateInput,
    formatBirthdateLabel,
    lastSyncLabel: formatLastSyncLabel(),
    sidebarMarkup: renderSidebar(),
  });
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

  try {
    const nextData = await fetchProfileLoadData(state.mockMode);

    state.user = nextData.user;
    state.progressDetail = nextData.progressDetail;
    state.lastSyncedAt = new Date();

    if (!state.mockMode) {
      saveSession({ user: nextData.user });
    }

    state.loading = false;

    if (nextData.feedback) {
      setFeedback(nextData.feedback.type, nextData.feedback.message, nextData.feedback.title);
    }

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
  const validation = buildAccountSubmitValidation(form, state.user);

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
    track.className = `profile-view-track profile-view-track-${state.activeTab}`;
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