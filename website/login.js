const loginForm = document.getElementById("login-form")

// Called when user clicks "Student Login" button on login page.
// If successful, stores form info into localStorage and
// redirects to main student page
function studentLogin() {
	const email = loginForm.Email.value;
	const password = loginForm.Password.value;

	console.log(email, password, "student");

	if (email == "User@rpi.edu" && password == "Password") {
        	console.log("Successfully logged in")
	}
}

// Called when user clicks "Instructor Login" button on login page.
// If successful, stores form info into localStorage and
// redirects to main instructor page
function instructorLogin() {
	const email = loginForm.Email.value;
	const password = loginForm.Password.value;

	console.log(email, password, "instructor");

	if (email == "User@rpi.edu" && password == "Password") {
        	console.log("Successfully logged in")
	}
}
