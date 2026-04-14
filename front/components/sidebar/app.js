import { logout } from "../../utils/auth.js";

const SIDEBAR_ANIMATION_MS = 320;

let menuOpen = false;
let hideSidebarTimeout = null;

export function renderSidebar({ showMissions = true } = {}) {
  return `
    <div class="dashboard-sidebar-overlay dashboard-sidebar-overlay-hidden" id="dashboard-sidebar-overlay" aria-hidden="true"></div>
    <aside class="dashboard-sidebar dashboard-sidebar-hidden" id="sidebar" aria-hidden="true">
      <div class="dashboard-sidebar-header logo">
        <h2>AIGENDA</h2>
      </div>
      <ul class="dashboard-sidebar-nav menu">
        <li>
          <a href="#/dashboard" class="dashboard-sidebar-link" data-route="dashboard">
            <i class="fas fa-home"></i>
            <span>Dashboard</span>
          </a>
        </li>
        <li>
          <a href="#/agenda" class="dashboard-sidebar-link" data-route="agenda">
            <i class="fas fa-calendar-alt"></i>
            <span>Agenda</span>
          </a>
        </li>
        <li>
          <a href="#/profile" class="dashboard-sidebar-link" data-route="profile">
            <i class="fas fa-user"></i>
            <span>Perfil</span>
          </a>
        </li>
        ${showMissions ? `
        <li>
          <a href="#/missions" class="dashboard-sidebar-link" data-route="missions">
            <i class="fas fa-bullseye"></i>
            <span>Missões</span>
          </a>
        </li>` : ""}
      </ul>
      <div class="dashboard-sidebar-logout logout">
        <button type="button" id="logout-btn" class="dashboard-logout-button">
          <i class="fas fa-sign-out-alt"></i>
          <span>Sair</span>
        </button>
      </div>
    </aside>
  `;
}

function setMenuOpen(nextState) {
  menuOpen = nextState;
  syncMenuState();
}

function clearSidebarHideTimeout() {
  if (hideSidebarTimeout) {
    window.clearTimeout(hideSidebarTimeout);
    hideSidebarTimeout = null;
  }
}

function syncMenuState() {
  const menuToggleButton = document.getElementById("dashboard-menu-toggle");
  const sidebar = document.querySelector(".dashboard-sidebar");
  const sidebarOverlay = document.getElementById("dashboard-sidebar-overlay");

  clearSidebarHideTimeout();
  menuToggleButton?.classList.toggle("dashboard-menu-toggle-hidden", menuOpen);

  if (menuOpen) {
    sidebar?.classList.remove("dashboard-sidebar-hidden");
    sidebarOverlay?.classList.remove("dashboard-sidebar-overlay-hidden");

    window.requestAnimationFrame(() => {
      sidebar?.classList.add("dashboard-sidebar-open");
      sidebarOverlay?.classList.add("dashboard-sidebar-overlay-visible");
    });

    sidebar?.setAttribute("aria-hidden", "false");
    sidebarOverlay?.setAttribute("aria-hidden", "false");
    return;
  }

  sidebar?.classList.remove("dashboard-sidebar-open");
  sidebarOverlay?.classList.remove("dashboard-sidebar-overlay-visible");
  sidebar?.setAttribute("aria-hidden", "true");
  sidebarOverlay?.setAttribute("aria-hidden", "true");

  hideSidebarTimeout = window.setTimeout(() => {
    sidebar?.classList.add("dashboard-sidebar-hidden");
    sidebarOverlay?.classList.add("dashboard-sidebar-overlay-hidden");
  }, SIDEBAR_ANIMATION_MS);
}

function bindSidebarNavigation() {
  const sidebarLinks = document.querySelectorAll(".dashboard-sidebar-link");
  const logoutButton = document.getElementById("logout-btn");
  const menuToggleButton = document.getElementById("dashboard-menu-toggle");
  const sidebarOverlay = document.getElementById("dashboard-sidebar-overlay");

  menuToggleButton?.addEventListener("click", () => {
    setMenuOpen(true);
  });

  sidebarOverlay?.addEventListener("click", () => {
    setMenuOpen(false);
  });

  sidebarLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const route = link.dataset.route;
      setMenuOpen(false);
      if (route) {
        window.loadPage(route);
      }
    });
  });

  logoutButton?.addEventListener("click", () => {
    setMenuOpen(false);
    logout();
  });
}

export function initializeSidebar() {
  bindSidebarNavigation();
  syncMenuState();
}

export function resetSidebarState() {
  menuOpen = false;
}
