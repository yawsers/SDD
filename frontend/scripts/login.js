// Called when user clicks "Login" button on login page.
// If successful, stores form info into localStorage and
// redirects to classes page
function login() {
	const loginForm = document.getElementById("login-form")
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
			localStorage.setItem('isstudent', response.isstudent)
			window.location.replace('classes.html');
		}
		else {
                	alert("Invalid login");
		}
	}
}
