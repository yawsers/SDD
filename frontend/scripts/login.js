const loginForm = document.getElementById("login-form")

// Called when user clicks "Student Login" button on login page.
// If successful, stores form info into localStorage and
// redirects to main student page
function loginStudent() {
	const email = loginForm.Email.value.toLowerCase();
	const password = loginForm.Password.value;

	const http = new XMLHttpRequest();
	http.open("POST", "https://professit-backend.herokuapp.com/verify_user_login")
	http.setRequestHeader("Content-Type", "application/json");
	http.send(JSON.stringify({"email": email, "password": password}));

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

// Called when user clicks "Instructor Login" button on login page.
// If successful, stores form info into localStorage and
// redirects to main instructor page
function loginInstructor() {
	const email = loginForm.Email.value;
	const password = loginForm.Password.value;

	console.log(email, password, "instructor");

	if (email == "User@rpi.edu" && password == "Password") {
        	console.log("Successfully logged in");
	}
}
