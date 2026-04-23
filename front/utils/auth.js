import { getAuthMode, setAuthMode } from "./config.js";
import {
  clearSession,
  hasSession
} from "./session.js";

export { getAuthMode, setAuthMode };

export function isAuthenticated() {
  return hasSession();
}

export function logout() {
  clearSession();

  if (typeof window.loadPage === "function") {
    window.loadPage("login");
    return;
  }

  window.location.href = "./index.html#/login";
}