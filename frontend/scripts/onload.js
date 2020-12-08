
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
	if (!isLoggedIn()) {
        	window.location.replace('login.html');
	}

	const http = new XMLHttpRequest();

	// Load student classes
	if (localStorage.isstudent == "true") {
		http.open("POST", "https://professit-backend.herokuapp.com/get_all_classes")
		http.setRequestHeader("Content-Type", "application/json");
		http.send(JSON.stringify({"studentid": localStorage.token}));
		document.getElementById('create-class').style.display = "none"
	}
	// Load instructor classes
	else {
		http.open("POST", "https://professit-backend.herokuapp.com/get_all_teaching")
		http.setRequestHeader("Content-Type", "application/json");
		http.send(JSON.stringify({"instructorid": localStorage.token}));
		document.getElementById('join-class').style.display = "none"
	}
	// Fill page with classes
	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		const classdiv = document.getElementById("classes");
		for (var i = 0; i < response.result.length; i++) {
			classdiv.innerHTML += "<a href=class.html?id=" +
				response.result[i].classid + "> <div>" +
				response.result[i].classname + "</div>" +
				(response.result[i].instructor ? "<div>" +
				response.result[i].instructor + "</div>" : "") +
				"</a>"
		}
	}
}
