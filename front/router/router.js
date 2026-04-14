import { getAuthMode, isAuthenticated, setAuthMode } from "../utils/auth.js";
import { PrivateRoute } from "./routerRules.js";

const APP_BASE_URL = new URL("../", import.meta.url);
const APP_BASE_PATH = APP_BASE_URL.pathname.endsWith("/")
  ? APP_BASE_URL.pathname
  : `${APP_BASE_URL.pathname}/`;
const APP_ENTRY_PATH = new URL("index.html", APP_BASE_URL).pathname;
const templateCache = new Map();
let inFlightNavigation = null;
let inFlightNavigationKey = "";
let inFlightResolvedPage = "";
let lastNavigationPage = "";
let lastNavigationAt = 0;
let latestNavigationId = 0;
const NAVIGATION_DEBOUNCE_MS = 400;

const ROUTES = {
  agenda: {
    pagePath: "pages/agenda/render.html",
    scriptPath: "pages/agenda/app.js",
  },
  "create-item": {
    pagePath: "pages/create-item/render.html",
    scriptPath: "pages/create-item/app.js",
  },
  dashboard: {
    pagePath: "pages/dashboard/render.html",
    scriptPath: "pages/dashboard/app.js",
  },
  login: {
    pagePath: "pages/login/render.html",
    scriptPath: "pages/login/app.js",
  },
  missions: {
    pagePath: "pages/missions/render.html",
    scriptPath: "pages/missions/app.js",
  },
  register: {
    pagePath: "pages/register/render.html",
    scriptPath: "pages/register/app.js",
  },
  profile: {
    pagePath: "pages/profile/render.html",
    scriptPath: "pages/profile/app.js",
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
  const { forceReload = false, updateHistory = true } = options;
  const normalizedPage = normalizePage(page);
  const now = Date.now();
  const currentRenderedPage = document.body.dataset.currentPage;
  const preResolvedPage = PrivateRoute(normalizedPage);
  const navigationId = ++latestNavigationId;

  if (!forceReload && normalizedPage === lastNavigationPage && now - lastNavigationAt < NAVIGATION_DEBOUNCE_MS) {
    return;
  }

  lastNavigationPage = normalizedPage;
  lastNavigationAt = now;

  if (!forceReload && inFlightNavigation && (inFlightNavigationKey === normalizedPage || inFlightResolvedPage === preResolvedPage)) {
    return inFlightNavigation;
  }

  if (!forceReload && currentRenderedPage && (currentRenderedPage === normalizedPage || currentRenderedPage === preResolvedPage)) {
    return;
  }

  const navigationPromise = (async () => {
    const resolvedPage = PrivateRoute(normalizedPage);
    const latestRenderedPage = document.body.dataset.currentPage;

    if (!forceReload && latestRenderedPage && latestRenderedPage === resolvedPage) {
      return;
    }

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

      if (navigationId !== latestNavigationId) {
        return;
      }

      // Remove scripts anteriores e limpa completamente
      const oldScripts = document.querySelectorAll("script[data-page-script]");
      oldScripts.forEach(s => {
        s.remove();
      });

      const app = document.getElementById("app");
      app.innerHTML = html;

      const dashboardLikePages = ["dashboard", "agenda", "profile", "missions", "create-item"];
      document.body.classList.toggle("dashboard-page", dashboardLikePages.includes(resolvedPage));
      document.body.dataset.currentPage = resolvedPage;

      if (route.scriptPath) {
        await new Promise(resolve => setTimeout(resolve, 50));

        if (navigationId !== latestNavigationId) {
          return;
        }

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
  })();

  inFlightNavigation = navigationPromise;
  inFlightNavigationKey = normalizedPage;
  inFlightResolvedPage = preResolvedPage;

  try {
    await navigationPromise;
  } finally {
    if (inFlightNavigation === navigationPromise) {
      inFlightNavigation = null;
      inFlightNavigationKey = "";
      inFlightResolvedPage = "";
    }
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
  const nextPage = getCurrentPathPage();
  if (nextPage === document.body.dataset.currentPage) {
    return;
  }

  void loadPage(nextPage, { updateHistory: false });
});

window.addEventListener("auth:unauthorized", () => {
  void loadPage("login", { forceReload: true });
});

// carregar página inicial
void loadPage(getCurrentPathPage(), { updateHistory: false });
