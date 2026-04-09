import { getAuthMode, isAuthenticated, revalidateSession, setAuthMode } from "../configs/auth.js";
import { PrivateRoute } from "./routerRules.js";

const APP_BASE_URL = new URL("../../../", import.meta.url);
const APP_BASE_PATH = APP_BASE_URL.pathname.endsWith("/")
  ? APP_BASE_URL.pathname
  : `${APP_BASE_URL.pathname}/`;
const APP_ENTRY_PATH = new URL("index.html", APP_BASE_URL).pathname;
const templateCache = new Map();

const ROUTES = {
  agenda: {
    pagePath: "ui/app/agenda.html",
    scriptPath: "js/app/agenda.js",
  },
  dashboard: {
    pagePath: "ui/app/dashboard.html",
    scriptPath: "js/app/dashboard.js",
  },
  login: {
    pagePath: "ui/auth/login.html",
    scriptPath: "js/auth/login.js",
  },
  register: {
    pagePath: "ui/auth/register.html",
    scriptPath: "js/auth/register.js",
  },
  profile: {
    pagePath: "ui/app/profile.html",
    scriptPath: "js/app/profile.js",
  },
};

function renderRouteError(page) {
  const app = document.getElementById("app");
  const template = document.getElementById("route-error-template");

  if (!app) {
    return;
  }

  if (template instanceof HTMLTemplateElement) {
    const content = template.content.cloneNode(true);
    const message = content.querySelector("[data-route-error-message]");

    if (message) {
      message.textContent = `Falha ao carregar a pagina ${page}`;
    }

    app.replaceChildren(content);
    return;
  }

  app.innerHTML = `
    <section class="auth-wrapper">
      <div class="login-container fade-in">
        <div class="login-header">
          <h1>AIGENDA</h1>
          <p>Falha ao carregar a pagina ${page}</p>
        </div>
      </div>
    </section>
  `;
}

function installAuthGlobals() {
  if (typeof window !== "undefined") {
    window.setAuthMode = setAuthMode;
    window.getAuthMode = getAuthMode;
    window.isAuthenticated = isAuthenticated;
  }

  if (typeof globalThis !== "undefined") {
    globalThis.setAuthMode = setAuthMode;
    globalThis.getAuthMode = getAuthMode;
    globalThis.isAuthenticated = isAuthenticated;
  }
}

function normalizePage(page) {
  if (!page || page === "/") {
    return "login";
  }

  let normalizedPage = page;

  if (normalizedPage.startsWith("#")) {
    normalizedPage = normalizedPage.replace(/^#\/?/, "");
  }

  try {
    normalizedPage = decodeURIComponent(normalizedPage);
  } catch (error) {
    console.warn("Nao foi possivel decodificar a rota atual:", error);
  }

  if (normalizedPage.startsWith(APP_BASE_PATH)) {
    normalizedPage = normalizedPage.slice(APP_BASE_PATH.length);
  }

  normalizedPage = normalizedPage.replace(/^\/+|\/+$/g, "");

  if (!normalizedPage || normalizedPage === "index.html") {
    return "login";
  }

  return normalizedPage;
}

function getCurrentPathPage() {
  const hashPage = window.location.hash.replace(/^#\/?/, "");

  if (hashPage) {
    return normalizePage(hashPage);
  }

  return normalizePage(window.location.pathname);
}

function getUrlForPage(page) {
  return page === "login" ? APP_ENTRY_PATH : `${APP_ENTRY_PATH}#/${page}`;
}

function getAssetUrl(path) {
  return new URL(path, APP_BASE_URL);
}

async function getTemplate(path) {
  if (templateCache.has(path)) {
    return templateCache.get(path);
  }

  const response = await fetch(getAssetUrl(path));

  if (!response.ok) {
    throw new Error(`Nao foi possivel carregar ${path}`);
  }

  const html = await response.text();
  templateCache.set(path, html);
  return html;
}

function preloadTemplates(paths) {
  const uniquePaths = [...new Set(paths)];

  uniquePaths.forEach((path) => {
    void getTemplate(path).catch((error) => {
      console.warn(`Preload ignorado para ${path}:`, error);
    });
  });
}

export async function loadPage(page, options = {}) {
  const { updateHistory = true } = options;
  const normalizedPage = normalizePage(page);
  await revalidateSession();
  const resolvedPage = PrivateRoute(normalizedPage);
  const route = ROUTES[resolvedPage] ?? {
    pagePath: resolvedPage,
    scriptPath: null,
  };

  try {
    const nextUrl = getUrlForPage(resolvedPage);
    const currentUrl = `${window.location.pathname}${window.location.hash}`;

    if (currentUrl !== nextUrl) {
      if (updateHistory) {
        window.history.pushState({ page: resolvedPage }, "", nextUrl);
      } else if (normalizedPage !== resolvedPage) {
        window.history.replaceState({ page: resolvedPage }, "", nextUrl);
      }
    }

    const html = await getTemplate(route.pagePath);

    // Remove scripts anteriores e limpa completamente
    const oldScripts = document.querySelectorAll("script[data-page-script]");
    oldScripts.forEach(s => {
      s.remove();
    });

    const app = document.getElementById("app");
    app.innerHTML = html;

    document.body.classList.toggle("dashboard-page", resolvedPage === "dashboard");
    document.body.dataset.currentPage = resolvedPage;

    if (route.scriptPath) {
      await new Promise(resolve => setTimeout(resolve, 50));

      const script = document.createElement("script");
      script.type = "module";
      const scriptUrl = getAssetUrl(route.scriptPath);
      scriptUrl.searchParams.set("v", Date.now().toString());
      script.src = scriptUrl.href;
      script.setAttribute("data-page-script", "true");
      document.body.appendChild(script);
    }
  } catch (error) {
    console.error("Erro ao carregar rota:", error);
    document.body.classList.remove("dashboard-page");
    renderRouteError(resolvedPage);
  }
}

// Expor globalmente para garantir acesso
window.loadPage = loadPage;
installAuthGlobals();

const routePagePaths = Object.values(ROUTES).map((route) => route.pagePath);

if (typeof window.requestIdleCallback === "function") {
  window.requestIdleCallback(() => {
    preloadTemplates(routePagePaths);
  });
} else {
  window.setTimeout(() => {
    preloadTemplates(routePagePaths);
  }, 150);
}

window.addEventListener("popstate", () => {
  void loadPage(getCurrentPathPage(), { updateHistory: false });
});

window.addEventListener("hashchange", () => {
  void loadPage(getCurrentPathPage(), { updateHistory: false });
});

window.addEventListener("auth:unauthorized", () => {
  void loadPage("login");
});

// carregar página inicial
loadPage(getCurrentPathPage(), { updateHistory: false });
