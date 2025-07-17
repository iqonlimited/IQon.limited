// Highlight Active Link Based on URL
document.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname;
  const links = document.querySelectorAll('.sidebar a');

  links.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});

// Optional Sidebar Toggle Example (if you want toggle effect)
function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  sidebar.classList.toggle('collapsed');
}
