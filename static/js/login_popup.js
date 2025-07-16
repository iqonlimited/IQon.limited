window.onload = function() {
  document.getElementById("loginPopup").style.display = "flex";
};

function login() {
  window.location.href = "/login";
}

function guestAccess() {
  document.getElementById("loginPopup").style.display = "none";
}
