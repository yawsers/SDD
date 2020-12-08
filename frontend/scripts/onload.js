
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
	}
	// Load instructor classes
	else {
		http.open("POST", "https://professit-backend.herokuapp.com/get_all_teaching")
		http.setRequestHeader("Content-Type", "application/json");
		http.send(JSON.stringify({"instructorid": localStorage.token}));
	}
	// Fill page with classes
	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		const classdiv = document.getElementById("classes");
		for (var i = 0; i < response.result.length; i++) {
			classdiv.innerHTML += "<a href=\"class.html?id=" +
				response.result[i].classid + "\"> <div class=\"title\">" +
				response.result[i].classname + "</div>" +
				(response.result[i].instructor ? "<div class=\"instructor\">" +
				response.result[i].instructor + "</div>" : "") +
				"</a>"
		}
	}
}


// onload for class page
// TODO: Finish implementation with calls to database
// If the user is logged in and in a valid class, load the respective lectures / other info
// If not logged in, redirect to login page
function loadClass() {
	if (!isLoggedIn()) {
		window.location.replace('login.html');
	}

	// Get query params to find class
	const urlParams = new URLSearchParams(window.location.search);

	// Currently hardcoded for demo purposes
	if (urlParams.get('id') == '1') {
        	document.getElementById("class-title").innerHTML = "Class 1";
		document.getElementById("lectures").innerHTML = '<iframe width="560" height="315" src="https://www.youtube.com/embed/FdqOpFVp25M" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

	}

	if (urlParams.get('id') == '2') {
        	document.getElementById("class-title").innerHTML = "Class 2";
		document.getElementById("lectures").innerHTML = '<iframe width="560" height="315" src="https://www.youtube.com/embed/ynig2wrF_as" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

	}

}
