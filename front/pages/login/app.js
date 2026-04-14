import { authenticate } from "../../api/api.js";
import { consumeAuthMessage } from "../../utils/session.js";

const emailInput = document.getElementById("email");
const errorMessage = document.getElementById("error");
const form = document.getElementById("login-form");
const goToRegister = document.getElementById("go-to-register");
const passwordInput = document.getElementById("password");

function goToPage(page) {
  if (typeof window.loadPage === "function") {
    window.loadPage(page);
    return;
  }
  window.location.href = `./index.html#/${page}`;
}

function showLoginError(message) {
  if (errorMessage) {
    errorMessage.textContent = message;
  }
}

function clearLoginError() {
  if (errorMessage) {
    errorMessage.textContent = "";
  }
}

const pendingAuthMessage = consumeAuthMessage();
if (pendingAuthMessage) {
  showLoginError(pendingAuthMessage);
}

async function handleLogin(e) {
  e.preventDefault();
  clearLoginError();

  const email = emailInput?.value ?? "";
  const password = passwordInput?.value ?? "";

  try {
    await authenticate(email, password);
    goToPage("dashboard");
  } catch (error) {
    showLoginError(error.message || "Email ou senha inválidos");
  }
}

form?.addEventListener("submit", handleLogin);

goToRegister?.addEventListener("click", (e) => {
  e.preventDefault();
  clearLoginError();
  goToPage("register");
});
