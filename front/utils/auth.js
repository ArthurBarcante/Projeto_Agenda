import { getAuthMode, isMockMode, isRealMode, setAuthMode } from "./config.js";
import {
  clearSession,
  getStoredToken,
  hasSession
} from "./session.js";

export { getAuthMode, setAuthMode };

export function isAuthenticated() {
  return hasSession();
}

export async function revalidateSession() {
  if (isMockMode()) {
    return hasSession();
  }

  if (!isRealMode()) {
    return false;
  }

  if (!hasSession()) {
    clearSession();
    return false;
  }

  const token = getStoredToken();
  if (!token) {
    clearSession();
    return false;
  }

  // Validacao agressiva local: evita chamadas ciclicas para /auth/me durante roteamento.
  return true;
}

export function logout() {
  clearSession();

  if (typeof window.loadPage === "function") {
    window.loadPage("login");
    return;
  }

  window.location.href = "./index.html#/login";
}