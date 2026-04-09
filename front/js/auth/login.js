import { authenticate } from "../core/api/api.js";
import { isAuthenticated } from "../core/configs/auth.js";
import { consumeAuthMessage } from "../core/configs/session.js";

const form = document.querySelector("#login-form");
const goToRegister = document.getElementById("go-to-register");
const errorMessage = document.getElementById("error");

if (isAuthenticated()) {
  if (typeof window.loadPage === "function") {
    window.loadPage("dashboard");
  } else {
    window.location.href = "./index.html#/dashboard";
  }

  throw new Error("Usuario autenticado nao pode acessar a tela de login.");
}

function showError(message) {
  if (errorMessage) {
    errorMessage.textContent = message;
  }
}

function clearError() {
  if (errorMessage) {
    errorMessage.textContent = "";
  }
}

const pendingAuthMessage = consumeAuthMessage();

if (pendingAuthMessage) {
  showError(pendingAuthMessage);
}

async function handleLogin(e) {
  e.preventDefault();
  clearError();

  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  try {
    await authenticate(email, password);

    window.loadPage("dashboard");
  } catch (error) {
    showError(error.message || "Email ou senha inválidos");
  }
}

// Setup dos event listeners
if (form) {
  form.addEventListener("submit", handleLogin);
}

if (goToRegister) {
  goToRegister.addEventListener("click", (e) => {
    e.preventDefault();
    clearError();
    window.loadPage("register");
  });
}
