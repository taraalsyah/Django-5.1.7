(() => {
  console.log('sidebar.js loaded');

  if (window.__sidebarInitialized) {
    console.warn('sidebar already initialized');
    return;
  }
  window.__sidebarInitialized = true;

  console.log('binding sidebar toggle');

  const sidebar = document.getElementById('sidebarid');
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const topbar = document.getElementById('topbar');

  if (!sidebar || !hamburgerBtn || !topbar) return;

  const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';

  sidebar.classList.remove('collapsed');
  topbar.classList.remove('collapsed');

  if (isCollapsed) {
    sidebar.classList.add('collapsed');
    topbar.classList.add('collapsed');
  }

  hamburgerBtn.addEventListener('click', (e) => {
    e.preventDefault();

    const collapsed = sidebar.classList.toggle('collapsed');
    topbar.classList.toggle('collapsed', collapsed);

    localStorage.setItem('sidebarCollapsed', collapsed);
  });
})();
