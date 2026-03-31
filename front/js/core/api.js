const USE_REAL_API = false;
const MOCK_API_URL = "http://localhost:3000";
const REAL_API_URL = "http://127.0.0.1:8000";

const API_URL = USE_REAL_API ? REAL_API_URL : MOCK_API_URL;

export async function loginRequest(email, password) {
  if (USE_REAL_API) {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error("Email ou senha inválidos");
    }

    return response.json();
  }

  // 🔁 MOCK
  const response = await fetch(`${API_URL}/users?email=${email}&password=${password}`);
  const data = await response.json();

  if (data.length === 0) {
    throw new Error("Email ou senha inválidos");
  }

  return { user: data[0] };
}

export async function registerRequest(userData) {
  if (USE_REAL_API) {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.json();
  }

  // 🔁 MOCK
  const response = await fetch(`${API_URL}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(userData)
  });

  return response.json();
}

export async function getUserByEmail(email) {
  if (USE_REAL_API) {
    // futuramente backend vai ter rota pra isso
    return [];
  }

  const response = await fetch(`${API_URL}/users?email=${email}`);
  return response.json();
}
