import { STORAGE_KEYS, isMockMode, isRealMode } from "./config.js";
import {
  getLocalItem,
  getLocalJson,
  getSessionItem,
  removeLocalItem,
  removeSessionItem,
  setLocalItem,
  setLocalJson,
  setSessionItem,
} from "./storage.js";

export const AUTH_MESSAGE_STORAGE_KEY = "authMessage";

function clearMockSession() {
  removeLocalItem(STORAGE_KEYS.mockUser);
}

function clearRealSession() {
  removeLocalItem(STORAGE_KEYS.realToken);
  removeLocalItem(STORAGE_KEYS.realUser);
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

  return getLocalItem(STORAGE_KEYS.realToken);
}

export function getStoredUser() {
  const storageKey = isMockMode() ? STORAGE_KEYS.mockUser : STORAGE_KEYS.realUser;
  return getLocalJson(storageKey);
}

export function saveSession({ token, user }) {
  if (isMockMode()) {
    clearRealSession();

    if (user) {
      setLocalJson(STORAGE_KEYS.mockUser, user);
    }

    return;
  }

  clearMockSession();

  if (token) {
    setLocalItem(STORAGE_KEYS.realToken, token);
  }

  if (user) {
    setLocalJson(STORAGE_KEYS.realUser, user);
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
  setSessionItem(AUTH_MESSAGE_STORAGE_KEY, message);
}

export function consumeAuthMessage() {
  const message = getSessionItem(AUTH_MESSAGE_STORAGE_KEY);

  if (!message) {
    return "";
  }

  removeSessionItem(AUTH_MESSAGE_STORAGE_KEY);
  return message;
}

export function hasSession() {
  if (isMockMode()) {
    return !!getLocalItem(STORAGE_KEYS.mockUser);
  }

  if (isRealMode()) {
    const token = getLocalItem(STORAGE_KEYS.realToken);

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
