// Called when user clicks "Create ... Account" button on account creation
// page. Argument "isStudent" is "true" if Student account, "false" if
// instructor.
// If successful, adds new user to database and redirects to classes page
function register(isStudent) {
	const accountForm = document.getElementById("account-form")
	const name = accountForm.Fullname.value.toLowerCase();
	const email = accountForm.Email.value.toLowerCase();
	const password = accountForm.Password.value;

	const http = new XMLHttpRequest();
	http.open("POST", "https://professit-backend.herokuapp.com/add_user")
	http.setRequestHeader("Content-Type", "application/json");
	if (isStudent == 'true') {
		http.send(JSON.stringify({"name": name, "email": email, "password": password, "isstudent": true}));
	}
	else {
		http.send(JSON.stringify({"name": name, "email": email, "password": password, "isstudent": false}));
	}

	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		// Account creation successful, continue
		if (response.status) {
                	localStorage.setItem('token', response.usid)
                	localStorage.setItem('isstudent', isStudent)
			window.location.replace('classes.html');
		}
		else {
                	alert("Invalid account / Email already used");
		}
	}
}
