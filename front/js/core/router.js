export async function loadPage(page) {
  let pagePath;
  let scriptPath;

  switch (page) {
    case "login":
      pagePath = "ui/auth/login.html";
      scriptPath = "js/auth/login.js";
      break;
    case "register":
      pagePath = "ui/auth/register.html";
      scriptPath = "js/auth/register.js";
      break;
    default:
      pagePath = page;
      scriptPath = null;
  }

  // Fetcha o HTML
  const response = await fetch(pagePath);
  const html = await response.text();

  // Remove scripts anteriores e limpa completamente
  const oldScripts = document.querySelectorAll("script[data-page-script]");
  oldScripts.forEach(s => {
    // Remove o script do DOM
    s.remove();
  });

  // Limpa o conteúdo
  const app = document.getElementById("app");
  app.innerHTML = html;

  // Carrega o novo script com cache-busting
  if (scriptPath) {
    // Aguarda um pouco para garantir que o DOM está atualizado
    await new Promise(resolve => setTimeout(resolve, 50));

    const script = document.createElement("script");
    script.type = "module";
    // Adiciona timestamp para evitar cache
    script.src = scriptPath + "?v=" + Date.now();
    script.setAttribute("data-page-script", "true");
    document.body.appendChild(script);
  }
}

// Expor globalmente para garantir acesso
window.loadPage = loadPage;

// carregar página inicial
loadPage("login");
