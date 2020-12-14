class Nav extends HTMLElement {
	constructor() {
		super();
	}
	connectedCallback() {
		var nav = `<div id="secondary-nav" class="links">`;
		var loc = window.location.href.split("/");
		loc = loc[loc.length - 1].split(".")[0];
		if (loc == "classes") {
			if (localStorage.getItem('isstudent') == "true")
				nav += `<a href="#">Join a class</a>`;
			else nav += `<a href="#">Create a class</a>`;
		} else if (loc == "class" || loc == "studentlist") {
			const urlParams = new URLSearchParams(window.location.search);
			const classid = urlParams.get('id');
			// update these w specific urls based on class
			nav += `<a href="class.html?id=` + classid + `">Lectures</a><a href="#">Resources</a>`;
			if (localStorage.getItem('isstudent') == "true")
				nav += `<a href="#" onmouseup="redirectLecture()">Join the lecture</a><a href="#">Leave this class</a>`;
			else {
				nav += `<a href="studentlist.html?id=` + classid + `">Student List</a>`;
				nav += `<a href="#" onmouseup="redirectLecture()">Start a lecture</a><a href="#">Class settings</a>`;
			}
		}
		nav += "</div>";
		this.innerHTML = nav;
	}
}

customElements.define('secondary-nav', Nav);

function redirectLecture() {
	window.open("localhost:8000/video_feed");
}
