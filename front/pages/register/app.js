import { getUserByEmail, registerRequest } from "../../api/api.js";
import { isMockMode } from "../../utils/config.js";
import { saveSession } from "../../utils/session.js";

const birthDateInput = document.getElementById("birthdate");
const confirmPasswordInput = document.getElementById("confirm-password");
const cpfInput = document.getElementById("cpf");
const emailInput = document.getElementById("email");
const form = document.getElementById("register-form");
const goToLogin = document.getElementById("go-to-login");
const nameInput = document.getElementById("name");
const passwordInput = document.getElementById("password");
const phoneInput = document.getElementById("phone");

function goToPage(page) {
  if (typeof window.loadPage === "function") {
    window.loadPage(page);
    return;
  }
  window.location.href = `./index.html#/${page}`;
}

function showRegisterError(message) {
  window.alert(message);
}

function showRegisterSuccess(message) {
  window.alert(message);
}

function applyCpfMask() {
  if (!cpfInput) return;

  let value = cpfInput.value.replace(/\D/g, "").slice(0, 11);

  if (value.length > 9) {
    value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, "$1.$2.$3-$4");
  } else if (value.length > 6) {
    value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, "$1.$2.$3");
  } else if (value.length > 3) {
    value = value.replace(/(\d{3})(\d{1,3})/, "$1.$2");
  }

  cpfInput.value = value;
}

cpfInput?.addEventListener("input", applyCpfMask);

async function handleRegister(e) {
  e.preventDefault();

  const name = nameInput?.value ?? "";
  const email = emailInput?.value ?? "";
  const password = passwordInput?.value ?? "";
  const confirmPassword = confirmPasswordInput?.value ?? "";
  const phone = phoneInput?.value ?? "";
  const cpf = cpfInput?.value ?? "";
  const birthDate = birthDateInput?.value ?? "";

  if (password !== confirmPassword) {
    showRegisterError("As senhas nao coincidem!");
    return;
  }

  try {
    const existingUser = await getUserByEmail(email);

    if (existingUser.length > 0) {
      showRegisterError("Email já cadastrado!");
      return;
    }

    const newUser = await registerRequest({
      name,
      email,
      password,
      confirm_password: confirmPassword,
      birthdate: birthDate,
      role: "user",
      cpf,
      phone,
    });

    if (isMockMode()) {
      saveSession({ user: newUser });
      showRegisterSuccess("Conta criada e login realizado!");
      goToPage("dashboard");
      return;
    }

    showRegisterSuccess("Conta criada com sucesso! Faça login.");
    goToPage("login");
  } catch (error) {
    showRegisterError(error.message || "Erro ao cadastrar");
  }
}

form?.addEventListener("submit", handleRegister);

goToLogin?.addEventListener("click", (event) => {
  event.preventDefault();
  goToPage("login");
});
