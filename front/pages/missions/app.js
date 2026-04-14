import { initializeSidebar, renderSidebar, resetSidebarState } from "../../components/sidebar/app.js";

const root = document.getElementById("missions-root");

if (root) {
  resetSidebarState();
  root.innerHTML = `
    <div class="dashboard-page fade-in">
      <button type="button" class="dashboard-menu-toggle" id="dashboard-menu-toggle" aria-label="Abrir menu">☰</button>
      <section class="dashboard-main missions-card">
        <h1>Missões</h1>
        <p>Camada reservada para evolução de gamificação do projeto.</p>
      </section>
      ${renderSidebar()}
    </div>
  `;
  initializeSidebar();
}
