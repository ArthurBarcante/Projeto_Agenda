import { getApiUrl } from "../utils/config.js";
import { fetchWithAuth } from "./api.js";

const PROGRESS_CACHE_STORAGE_KEY = "aigenda.progress.cache";

const runtime = (typeof window !== "undefined")
  ? (window.__AIGENDA_PROGRESS_RUNTIME__ ||= {
    cache: null,
    inFlight: null,
    lastFetchAt: 0,
  })
  : {
    cache: null,
    inFlight: null,
    lastFetchAt: 0,
  };

const PROGRESS_CACHE_TTL_MS = 60000;

function hydrateCacheFromSessionStorage() {
  if (typeof window === "undefined" || runtime.cache || runtime.lastFetchAt) {
    return;
  }

  try {
    const rawValue = window.sessionStorage.getItem(PROGRESS_CACHE_STORAGE_KEY);

    if (!rawValue) {
      return;
    }

    const parsed = JSON.parse(rawValue);

    if (!parsed?.payload || !parsed?.timestamp) {
      return;
    }

    if (Date.now() - parsed.timestamp >= PROGRESS_CACHE_TTL_MS) {
      window.sessionStorage.removeItem(PROGRESS_CACHE_STORAGE_KEY);
      return;
    }

    runtime.cache = parsed.payload;
    runtime.lastFetchAt = parsed.timestamp;
  } catch {
    window.sessionStorage.removeItem(PROGRESS_CACHE_STORAGE_KEY);
  }
}

function persistCache(payload) {
  if (typeof window === "undefined") {
    return;
  }

  try {
    window.sessionStorage.setItem(PROGRESS_CACHE_STORAGE_KEY, JSON.stringify({
      payload,
      timestamp: runtime.lastFetchAt,
    }));
  } catch {
    // Ignora falhas de persistencia de cache no navegador.
  }
}

function getProgressEndpoint() {
  return `${getApiUrl()}/progress`;
}

export async function getProgress() {
  hydrateCacheFromSessionStorage();
  const now = Date.now();

  if (runtime.inFlight) {
    return runtime.inFlight;
  }

  if (runtime.cache && now - runtime.lastFetchAt < PROGRESS_CACHE_TTL_MS) {
    return runtime.cache;
  }

  runtime.inFlight = fetchWithAuth(getProgressEndpoint())
    .then((payload) => {
      runtime.cache = payload;
      runtime.lastFetchAt = Date.now();
      persistCache(payload);
      return payload;
    })
    .finally(() => {
      runtime.inFlight = null;
    });

  return runtime.inFlight;
}

export async function getProgressByUserId(userId) {
  const url = `${getProgressEndpoint()}/${userId}`;
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar progresso: ${response.statusText}`);
  }
  return response.json();
}

export async function updateDailyGoal(dailyGoal) {
  const payload = await fetchWithAuth(getProgressEndpoint(), {
    method: "PUT",
    body: JSON.stringify({ daily_goal: Number(dailyGoal) }),
  });

  runtime.cache = payload;
  runtime.lastFetchAt = Date.now();
  persistCache(payload);
  return payload;
}