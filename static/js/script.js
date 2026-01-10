if (!window.__sidebarInitialized) {
  window.__sidebarInitialized = true;

  document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded triggered');

    const sidebar = document.getElementById('sidebarid');
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const topbar = document.getElementById('topbar');

    if (!sidebar || !hamburgerBtn || !topbar) return;

    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';

    sidebar.classList.toggle('collapsed', isCollapsed);
    topbar.classList.toggle('collapsed', isCollapsed);

    hamburgerBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      const collapsed = sidebar.classList.toggle('collapsed');
      topbar.classList.toggle('collapsed', collapsed);
      localStorage.setItem('sidebarCollapsed', collapsed);
    });
  });
}
