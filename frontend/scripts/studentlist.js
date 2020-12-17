// Add a student to the current class given their email
function addStudent() {
	const studentAddForm = document.getElementById("studentadd-form")
	const email = studentAddForm.Email.value.toLowerCase();
	
	const urlParams = new URLSearchParams(window.location.search);
	const http = new XMLHttpRequest();
	http.open("POST", "https://professit-backend.herokuapp.com/add_student")
	http.setRequestHeader("Content-Type", "application/json");
	http.send(JSON.stringify({"email": email, "classid": urlParams.get('id')}));

	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		// Login successful, redirect to classes page
		if (response.status) {
			alert("Student successfully added");
		}
		else {
                	alert("Student doesn't exist / already in class");
		}
	}
}
