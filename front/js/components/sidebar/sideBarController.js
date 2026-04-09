import { logout } from "../../core/configs/auth.js";

let menuOpen = false;

export function setMenuOpen(nextState) {
  menuOpen = nextState;
  syncMenuState();
}

export function syncMenuState() {
  const menuToggleButton = document.getElementById("dashboard-menu-toggle");
  const sidebar = document.querySelector(".dashboard-sidebar");
  const sidebarOverlay = document.getElementById("dashboard-sidebar-overlay");

  menuToggleButton?.classList.toggle("dashboard-menu-toggle-hidden", menuOpen);
  sidebar?.classList.toggle("dashboard-sidebar-open", menuOpen);
  sidebarOverlay?.classList.toggle("dashboard-sidebar-overlay-visible", menuOpen);
}

export function bindDashboardEvents() {
  const menuToggleButton = document.getElementById("dashboard-menu-toggle");
  const sidebarOverlay = document.getElementById("dashboard-sidebar-overlay");
  const sidebarLinks = document.querySelectorAll(".dashboard-sidebar-link");
  const logoutButton = document.getElementById("logout-btn");

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
  bindDashboardEvents();
  syncMenuState();
}

export function resetSidebarState() {
  menuOpen = false;
}
