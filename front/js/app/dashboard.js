import Sidebar from "../components/sidebar/sideBar.js";
import {
  initializeSidebar,
  resetSidebarState,
} from "../components/sidebar/sideBarController.js";
import { isAuthenticated } from "../core/configs/auth.js";

const root = document.getElementById("dashboard-root");

if (!isAuthenticated()) {
  if (typeof window.loadPage === "function") {
    window.loadPage("login");
  } else {
    window.location.href = "./index.html#/login";
  }

  throw new Error("Acesso nao autorizado ao dashboard.");
}

function renderDashboard() {
  if (!root) {
    return;
  }

  resetSidebarState();

  root.innerHTML = `
    <div class="dashboard-page fade-in">
      <button type="button" class="dashboard-menu-toggle" id="dashboard-menu-toggle" aria-label="Abrir menu">
        ☰
      </button>

      <div class="dashboard-main dashboard-main-standalone">
        <h1>Dashboard</h1>
        <p>Area autenticada</p>
      </div>

      ${Sidebar()}
    </div>
  `;

  initializeSidebar();
}

function loadDashboard() {
  if (!root) {
    return;
  }

  renderDashboard();
}

loadDashboard();