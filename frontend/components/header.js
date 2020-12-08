class Header extends HTMLElement {
	constructor() {
		super();
	}
	connectedCallback() {
		var header = `<header><a href="index.html"
		id="wordmark">Profess.it</a><div id="primary-nav" class="links">`;
		if (localStorage.getItem('token'))
			header += `<a href="classes.html">My classes</a><a
			href="#">Account settings</a><a href="#"
			onmouseup="signOut()">Sign out</a>`;
		else
			header += `<a href="login.html">Sign in</a><a
			href="register.html">Create an account</a>`;
		header += `</div></header>`;
		this.innerHTML = header;
	}
}

// Logs the current user out by clearing localStorage()
// and redirecting to index page
function signOut() {
	localStorage.clear();
	window.location.replace('../pages/index.html')
}

customElements.define('header-component', Header);
