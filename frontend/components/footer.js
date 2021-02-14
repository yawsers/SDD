class Footer extends HTMLElement {
	constructor() {
		super();
	}
	connectedCallback() {
		this.innerHTML = `<footer><span>&copy; 2020 Profess.it</span><a
		href="https://github.com/yawsers/SDD">Github</a><a
		href="https://info.rpi.edu/
		statement-of-accessibility">Accessibility</a></footer>`;
	}
}

customElements.define('footer-component', Footer);
