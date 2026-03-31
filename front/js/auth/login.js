import { loginRequest } from "../core/api.js";

const email = document.getElementById("email");
const password = document.getElementById("password");
const errorEl = document.getElementById("error");
const loginForm = document.getElementById("login-form");
const goToRegister = document.getElementById("go-to-register");

async function login(e) {
  e.preventDefault();

  const emailValue = email.value;
  const passwordValue = password.value;

  errorEl.innerText = "";

  if (!emailValue || !passwordValue) {
    errorEl.innerText = "Preencha todos os campos";
    return;
  }

  try {
    const users = await loginRequest(emailValue, passwordValue);

    if (users.length > 0) {
      const user = users[0];

      alert("Login realizado com sucesso!");

      // Simula sessão
      localStorage.setItem("user", JSON.stringify(user));

      // redirecionamento futuro
      console.log("Usuário logado:", user);
    } else {
      errorEl.innerText = "Email ou senha inválidos";
    }
  } catch (error) {
    errorEl.innerText = "Erro ao conectar com o servidor";
  }
}

// Setup dos event listeners
if (loginForm) {
  loginForm.addEventListener("submit", login);
}

if (goToRegister) {
  goToRegister.addEventListener("click", (e) => {
    e.preventDefault();
    window.loadPage("register");
  });
}

// Exportar para uso global
window.login = login;
