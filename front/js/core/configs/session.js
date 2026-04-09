import { STORAGE_KEYS, isMockMode, isRealMode } from "./config.js";

export const AUTH_MESSAGE_STORAGE_KEY = "authMessage";

function clearMockSession() {
  localStorage.removeItem(STORAGE_KEYS.mockUser);
}

function clearRealSession() {
  localStorage.removeItem(STORAGE_KEYS.realToken);
  localStorage.removeItem(STORAGE_KEYS.realUser);
}

function parseJwt(token) {
  try {
    const base64Payload = token.split(".")[1];
    const normalizedPayload = base64Payload
      .replace(/-/g, "+")
      .replace(/_/g, "/");
    const paddedPayload = normalizedPayload.padEnd(Math.ceil(normalizedPayload.length / 4) * 4, "=");
    const payload = atob(paddedPayload);
    return JSON.parse(payload);
  } catch (error) {
    return null;
  }
}

function isTokenValid(token) {
  const data = parseJwt(token);

  if (!data) {
    return false;
  }

  const now = Date.now() / 1000;
  return !!data.exp && data.exp > now;
}

export function getStoredToken() {
  if (!isRealMode()) {
    return null;
  }

  return localStorage.getItem(STORAGE_KEYS.realToken);
}

export function getStoredUser() {
  const storageKey = isMockMode() ? STORAGE_KEYS.mockUser : STORAGE_KEYS.realUser;
  const rawUser = localStorage.getItem(storageKey);

  if (!rawUser) {
    return null;
  }

  try {
    return JSON.parse(rawUser);
  } catch (error) {
    console.error("Falha ao ler usuario salvo:", error);
    localStorage.removeItem(storageKey);
    return null;
  }
}

export function saveSession({ token, user }) {
  if (isMockMode()) {
    clearRealSession();

    if (user) {
      localStorage.setItem(STORAGE_KEYS.mockUser, JSON.stringify(user));
    }

    return;
  }

  clearMockSession();

  if (token) {
    localStorage.setItem(STORAGE_KEYS.realToken, token);
  }

  if (user) {
    localStorage.setItem(STORAGE_KEYS.realUser, JSON.stringify(user));
  }
}

export function clearSession() {
  if (isMockMode()) {
    clearMockSession();
    return;
  }

  if (isRealMode()) {
    clearRealSession();
  }
}

export function setAuthMessage(message) {
  sessionStorage.setItem(AUTH_MESSAGE_STORAGE_KEY, message);
}

export function consumeAuthMessage() {
  const message = sessionStorage.getItem(AUTH_MESSAGE_STORAGE_KEY);

  if (!message) {
    return "";
  }

  sessionStorage.removeItem(AUTH_MESSAGE_STORAGE_KEY);
  return message;
}

export function hasSession() {
  if (isMockMode()) {
    return !!localStorage.getItem(STORAGE_KEYS.mockUser);
  }

  if (isRealMode()) {
    const token = localStorage.getItem(STORAGE_KEYS.realToken);

    if (!token) {
      return false;
    }

    return isTokenValid(token);
  }

  return false;
}

export function loadCurrentUser() {
  return getStoredUser();
}

export function saveAuthSession(sessionData) {
  return saveSession(sessionData);
}

export function clearCurrentAuthSession() {
  return clearSession();
}

export function clearAuthSession() {
  clearRealSession();
  clearMockSession();
}
