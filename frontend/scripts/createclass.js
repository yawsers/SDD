// Create a class under the current instructor
function createClass() {
	const createClassForm = document.getElementById("createclass-form")
	const classname = createClassForm.Classname.value;
	
	const http = new XMLHttpRequest();
	http.open("POST", "https://professit-backend.herokuapp.com/save_class")
	http.setRequestHeader("Content-Type", "application/json");
	http.send(JSON.stringify({"classname": classname, "instructorid": localStorage.token}));

	http.onload = function() {
        	const response = JSON.parse(http.responseText);
		// Login successful, redirect to classes page
		if (response.status) {
			alert("Class successfully added");
			window.location.replace('classes.html')
		}
		else {
                	alert("Class unsuccessfully added");
		}
	}
}
