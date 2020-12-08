class Header extends HTMLElement {
	constructor() {
		super();
	}
	connectedCallback() {
		this.innerHTML = `<header><a href="index.html"
		id="wordmark">Profess.it</a><div id="primary-nav" class="links"><a
		href="login.html">Sign in</a><a
		href="register.html">Create an account</a><a
		href="classes.html">My classes</a><a href="#">Account settings</a><a
		href="#">Sign out</a></div></header>`;
		var links = document.getElementById("primary-nav").getElementsByTagName("a");
		console.log(links);
		var i;
		if (localStorage.getItem('token'))
			for (i = 0; i < 2; i++) links[0].remove();
		else for (i = 0; i < 3; i++) links[2].remove();
	}
}

customElements.define('header-component', Header);
