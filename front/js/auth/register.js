import { getUserByEmail, registerRequest } from "../core/api/api.js";
import { isMockMode } from "../core/configs/config.js";
import { saveSession } from "../core/configs/session.js";

const form = document.getElementById("register-form");
const goToLogin = document.getElementById("go-to-login");
const cpfInput = document.getElementById("cpf");

cpfInput.addEventListener("input", () => {
  let v = cpfInput.value.replace(/\D/g, "").slice(0, 11);
  if (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, "$1.$2.$3-$4");
  else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{1,3})/, "$1.$2.$3");
  else if (v.length > 3) v = v.replace(/(\d{3})(\d{1,3})/, "$1.$2");
  cpfInput.value = v;
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  const phone = document.getElementById("phone").value;
  const cpf = document.getElementById("cpf").value;
  const birthDate = document.getElementById("birthdate").value;

  if (password !== confirmPassword) {
    alert("As senhas nao coincidem!");
    return;
  }

  try {
    const existingUser = await getUserByEmail(email);

    if (existingUser.length > 0) {
      alert("Email já cadastrado!");
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
      alert("Conta criada e login realizado!");
      window.loadPage("dashboard");
      return;
    }

    alert("Conta criada com sucesso! Faça login.");
    window.loadPage("login");

  } catch (error) {
    alert(error.message || "Erro ao cadastrar");
  }
});

goToLogin.addEventListener("click", () => {
  window.loadPage("login");
});
