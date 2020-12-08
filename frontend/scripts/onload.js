
// Returns true if a user is currently logged in, dependent on localStorage.
// Otherwise, returns false
function isLoggedIn() {
	return localStorage.token != null;
}

// onload for login page and create account page
// If the user is already logged in, redirect to the home page (index.html)
function loadLogin() {
	if (isLoggedIn()) {
        	window.location.replace('index.html');
	}
}
