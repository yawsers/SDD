
// Returns true if a user is currently logged in, dependent on localStorage.
// Otherwise, returns false
function isLoggedIn() {
	return localStorage.token != null;
}

// onload for login page and register page
// If the user is already logged in, redirect to the home page (index.html)
function loadLogin() {
	if (isLoggedIn()) {
        	window.location.replace('index.html');
	}
}

// onload for classes page
// If the user is logged in, load the users respective classes
// If not logged in, redirect to login page
function loadClasses() {
	const http = new XMLHttpRequest();

	// Student load
	http.open("POST", "https://professit-backend.herokuapp.com/get_all_classes")
	http.setRequestHeader("Content-Type", "application/json");
	http.send(JSON.stringify({}));

	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		// Login successful, redirect to classes page
		if (response.status) {
                	localStorage.setItem('token', response.usid)
			window.location.replace('classes.html');
		}
		else {
                	alert("Invalid login");
		}
	}
}
