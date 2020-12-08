const accountForm = document.getElementById("account-form")

// Called when user clicks "Create Student Account" button on account creation
// page.  If successful, adds new student to database and redirects to main
// student page
function registerStudent() {
	const name = accountForm.Fullname.value.toLowerCase();
	const email = accountForm.Email.value.toLowerCase();
	const password = accountForm.Password.value;

	const http = new XMLHttpRequest();
	http.open("POST", "https://professit-backend.herokuapp.com/add_user")
	http.setRequestHeader("Content-Type", "application/json");
	http.send(JSON.stringify({"name": name, "email": email, "password": password, "isstudent": true}));

	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		// Account creation successful, continue
		if (response.status) {
                	localStorage.setItem('token', response.usid)
			window.location.replace('classes.html');
		}
		else {
                	alert("Invalid account / Email already used");
		}
	}
}

// Called when user clicks "Create Instructor Account" button on account
// creation page.  If successful, adds new instructor to database and redirects to
// main instructor page
function registerInstructor() {
	const name = accountForm.Fullname.value.toLowerCase();
	const email = accountForm.Email.value.toLowerCase();
	const password = accountForm.Password.value;

	const http = new XMLHttpRequest();
	http.open("POST", "https://professit-backend.herokuapp.com/add_user")
	http.setRequestHeader("Content-Type", "application/json");
	http.send(JSON.stringify({"name": name, "email": email, "password": password, "isstudent": false}));

	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		// Account creation successful, continue
		if (response.status) {
                	localStorage.setItem('token', response.usid)
			window.location.replace('classes.html');
		}
		else {
                	alert("Invalid account / Email already used");
		}
	}
}
