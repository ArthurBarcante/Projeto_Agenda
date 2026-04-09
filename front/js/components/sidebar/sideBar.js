export default function Sidebar({ menuOpen = false } = {}) {
  const overlayClassName = menuOpen
    ? "dashboard-sidebar-overlay dashboard-sidebar-overlay-visible"
    : "dashboard-sidebar-overlay";

  const sidebarClassName = menuOpen
    ? "dashboard-sidebar dashboard-sidebar-open"
    : "dashboard-sidebar";

  return `
		<div class="${overlayClassName}" id="dashboard-sidebar-overlay"></div>
		<aside class="${sidebarClassName}" id="sidebar">
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
