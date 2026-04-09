import { getApiUrl, isMockMode, isRealMode } from "../configs/config.js";
import {
  clearSession,
  getStoredToken,
  loadCurrentUser,
  saveSession,
  setAuthMessage,
} from "../configs/session.js";

function getCurrentApiUrl() {
  return getApiUrl();
}

function buildUnavailableError() {
  const currentApiUrl = getCurrentApiUrl();
  if (isMockMode()) {
    return new Error(`Mock indisponivel. Inicie o JSON Server em ${currentApiUrl}`);
  }

  return new Error(`Backend indisponivel. Inicie a API em ${currentApiUrl}`);
}

async function parseErrorResponse(response, fallbackMessage) {
  try {
    const errorData = await response.json();
    return errorData.detail || fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}

function handleUnauthorizedResponse(errorMessage) {
  clearSession();
  setAuthMessage("Sua sessao expirou ou se tornou invalida. Faca login novamente.");

  if (typeof window !== "undefined") {
    window.dispatchEvent(new CustomEvent("auth:unauthorized", {
      detail: { message: errorMessage }
    }));
  }
}

const authApi = {
  async login(email, password) {
    const response = await fetch(`${getCurrentApiUrl()}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const errorMessage = await parseErrorResponse(response, "Erro ao fazer login");
      throw new Error(errorMessage);
    }

    return response.json();
  },

  async register(userData) {
    const response = await fetch(`${getCurrentApiUrl()}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const errorMessage = await parseErrorResponse(response, "Erro ao cadastrar");
      throw new Error(errorMessage);
    }

    return response.json();
  },

  async getCurrentUser() {
    return fetchWithAuth(`${getCurrentApiUrl()}/auth/me`);
  },

  async getUserByEmail() {
    return [];
  },

  async authenticate(email, password) {
    clearSession();

    const data = await this.login(email, password);
    const token = data?.access_token;

    if (!token) {
      clearSession();
      throw new Error("Nao foi possivel iniciar a sessao.");
    }

    saveSession({ token });

    try {
      const user = await this.getCurrentUser();

      if (!user) {
        throw new Error("Nao foi possivel carregar o usuario autenticado.");
      }

      saveSession({ token, user });
      return { token, user };
    } catch (error) {
      clearSession();
      throw error;
    }
  }
};

const authMock = {
  async login(email, password) {
    const response = await fetch(`${getCurrentApiUrl()}/users?email=${email}&password=${password}`);
    const data = await response.json();

    if (data.length === 0) {
      throw new Error("Email ou senha inválidos");
    }

    return { user: data[0] };
  },

  async register(userData) {
    const response = await fetch(`${getCurrentApiUrl()}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(userData)
    });

    return response.json();
  },

  async getCurrentUser() {
    return loadCurrentUser();
  },

  async getUserByEmail(email) {
    const response = await fetch(`${getCurrentApiUrl()}/users?email=${email}`);
    return response.json();
  },

  async authenticate(email, password) {
    clearSession();

    const data = await this.login(email, password);

    if (!data?.user) {
      clearSession();
      throw new Error("Nao foi possivel iniciar a sessao.");
    }

    saveSession({ user: data.user });
    return { user: data.user };
  }
};

function getAuthAdapter() {
  return isRealMode() ? authApi : authMock;
}

export async function login(email, password) {
  try {
    return await getAuthAdapter().login(email, password);
  } catch (error) {
    if (error instanceof TypeError) {
      throw buildUnavailableError();
    }

    console.error("Erro:", error);
    throw error;
  }
}

export async function authenticate(email, password) {
  try {
    return await getAuthAdapter().authenticate(email, password);
  } catch (error) {
    clearSession();

    if (error instanceof TypeError) {
      throw buildUnavailableError();
    }

    throw error;
  }
}

export function getToken() {
  return getStoredToken();
}

export async function fetchWithAuth(url, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
    "Authorization": `Bearer ${token}`
  };

  const response = await fetch(url, {
    ...options,
    headers
  });

  if (!response.ok) {
    const errorMessage = await parseErrorResponse(response, "Erro na requisição autenticada");

    const error = new Error(errorMessage);
    error.status = response.status;

    if (response.status === 401 && isRealMode()) {
      handleUnauthorizedResponse(error.message);
    }

    throw error;
  }

  return response.json();
}

export async function getCurrentUser() {
  try {
    return await getAuthAdapter().getCurrentUser();
  } catch (error) {
    if (error instanceof TypeError) {
      throw buildUnavailableError();
    }

    throw error;
  }
}

export async function loginRequest(email, password) {
  return authenticate(email, password);
}

export async function registerRequest(userData) {
  try {
    return await getAuthAdapter().register(userData);
  } catch (error) {
    if (error instanceof TypeError) {
      throw buildUnavailableError();
    }

    throw error;
  }
}

export async function getUserByEmail(email) {
  try {
    return await getAuthAdapter().getUserByEmail(email);
  } catch (error) {
    if (error instanceof TypeError) {
      throw buildUnavailableError();
    }

    throw error;
  }
}
