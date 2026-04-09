import { getCurrentUser } from "../api/api.js";
import { getAuthMode, isMockMode, isRealMode, setAuthMode } from "./config.js";
import {
  clearSession,
  getStoredToken,
  hasSession,
  saveSession,
  setAuthMessage,
} from "./session.js";

export { getAuthMode, setAuthMode };

export function isAuthenticated() {
  return hasSession();
}

export async function revalidateSession() {
  if (isMockMode()) {
    // Mock persiste localmente entre reloads sem depender do backend.
    return hasSession();
  }

  if (!isRealMode()) {
    return false;
  }

  // No modo real, reload so mantem a sessao se o backend aceitar o token atual.
  if (!hasSession()) {
    clearSession();
    return false;
  }

  const token = getStoredToken();

  if (!token) {
    clearSession();
    return false;
  }

  try {
    const user = await getCurrentUser();
    saveSession({ token, user });
    return true;
  } catch (error) {
    clearSession();

    if (error?.status === 401) {
      return false;
    }

    setAuthMessage("Nao foi possivel revalidar sua sessao. Faca login novamente.");
    console.error("Falha ao revalidar sessao no modo real:", error);
    return false;
  }
}

export function logout() {
  clearSession();

  if (typeof window.loadPage === "function") {
    window.loadPage("login");
    return;
  }

  window.location.href = "./index.html#/login";
}