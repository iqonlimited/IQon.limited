// Show the popup on page load
window.onload = function() {
  document.getElementById('loginPopup').style.display = 'flex';
};

// Login function
function login() {
  document.getElementById('loginPopup').style.display = 'none';
  // Redirect to login page
  window.location.href = '/login';
}

// Guest Access function
function guestAccess() {
  document.getElementById('loginPopup').style.display = 'none';
  // Continue using the app as guest
}
