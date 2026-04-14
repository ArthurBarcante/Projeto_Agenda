const AUTH_MODE_STORAGE_KEY = "authMode";
const DEFAULT_AUTH_MODE = "real";

import { getLocalItem, setLocalItem } from "./storage.js";

export const API_URLS = {
  mock: "http://127.0.0.1:3002",
  real: "http://127.0.0.1:8000",
};

export const STORAGE_KEYS = {
  mockUser: "mockUser",
  realUser: "user",
  realToken: "token",
};

function normalizeAuthMode(mode) {
  return mode === "mock" ? "mock" : "real";
}

function getPersistedAuthMode() {
  return getLocalItem(AUTH_MODE_STORAGE_KEY);
}

export const AUTH_MODE = DEFAULT_AUTH_MODE;

export function setAuthMode(mode) {
  const nextMode = normalizeAuthMode(mode);
  setLocalItem(AUTH_MODE_STORAGE_KEY, nextMode);
  return nextMode;
}

export function getAuthMode() {
  return normalizeAuthMode(getPersistedAuthMode() || DEFAULT_AUTH_MODE);
}

export function isMockMode() {
  return getAuthMode() === "mock";
}

export function isRealMode() {
  return getAuthMode() === "real";
}

export function getApiUrl() {
  return isMockMode() ? API_URLS.mock : API_URLS.real;
}
