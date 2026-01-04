document.addEventListener('DOMContentLoaded', () => {
  const sidebars = document.getElementById('sidebarid');
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const topbar = document.getElementById('topbar');

  // pastikan elemen ada sebelum akses classList
  if (!sidebars || !hamburgerBtn || !topbar) return;

  // Load saved state
  const collapsed = localStorage.getItem('sidebarCollapsed') === 'true';
  if (collapsed) {
    sidebars.classList.add('collapsed');
    topbar.classList.add('collapsed');
  }

  // Toggle and save state
  hamburgerBtn.addEventListener('click', () => {
    sidebars.classList.toggle('collapsed');
    topbar.classList.toggle('collapsed');
    const isCollapsed = sidebars.classList.contains('collapsed');
    localStorage.setItem('sidebarCollapsed', isCollapsed);
  });
});

