async function afterLoginDuties() {
	if (g_logining || !g_logined)
		return;
	enablePlayers();
	getCurriculum(with_live = false).then(() => {
		if (g_logining || !g_logined)
			return;
		let b = document.getElementById("curriculum-button");
		b.style.display = "inline";
		if (localStorage.getItem("fid") == "16820")
			getCurriculum(with_live = true);
	});
	[
		"login-button", "logout-button",
		"player0-scan-button", "camera-scan-button",
		"locations-button", "activities-button"
	].forEach((v) => {
		displayTag(v, "inline");
	});
	alert("Logged in successfully.");
}

async function afterLogoutDuties() {
	if (g_logining || g_logined)
		return;
	hideOtherLists();
	[
		"login-button", "logout-button",
		"player0-scan-button", "camera-scan-button",
		"locations-button", "activities-button", "curriculum-button"
	].forEach((v) => {
		displayTag(v, "inline");
	});
}

async function promptLogin() {
	if (g_logining || g_logined)
		return;
	promptLogin.calling = true;
	let username = localStorage.getItem("username");
	let password = localStorage.getItem("password");
	let method = (localStorage.getItem("login_method") === "ids");
	if (!username ||
		      !confirm(`Use previously entered account ${username}?`)) {
		method = !confirm("Login?\nChoose account type: " +
				 "confirm for Chaoxing, else IDS.");
		username = prompt("Input username:");
		if (username === null)
			return;
		assert(username, "Invalid username.");
		password = prompt("Input password:");
		if (password === null)
			return;
	}
	try {
		let success = await (method ?
				     idsLoginPrepare(username, password):
				     chaoxingLogin(username, password));
		assert(success === true, success);
	}
	catch (err) {
		alert(`Login failed. (${err.message})`);
	}
}

async function promptLogout(quiet = false) {
	if (g_logining || !g_logined)
		return;
	if (confirm("Logout?")) {
		g_logined = false;
		await afterLogoutDuties();
		if (!quiet)
			alert("Logged out successfully.");
	}
	else
		alert("Logout failed.");
}

async function chaoxingLogin(username, password, force = false) {
	if (!force) {
		if (g_logining || g_logined)
			return;
		g_logining = true;
		g_logined = false;
	}
	let ret = false;
	let cookies;
	if (force)
		cookies = localStorage.getItem("cookies");
	else
		cookies = ((username != localStorage.getItem("username") ||
			password != localStorage.getItem("password")) ?
		       "" : localStorage.getItem("cookies"));
	try {
		let res = await post("/chaoxing/login", {
			"username": username,
			"password": password,
			"cookies": cookies
		});
		assert(res.status_code == 200, "Backend error.");
		let data = res.json();
		assert(!data.err, data.err);
		localStorage.setItem("login_method", "chaoxing");
		localStorage.setItem("username", username);
		localStorage.setItem("password", password);
		localStorage.setItem("cookies", data["cookies"]);
		localStorage.setItem("fid", data["fid"]);
		g_courses = data["courses"];
		ret = true;
	}
	catch (err) {
		ret = err.message;
	}
	if (!force) {
		g_logined = (ret === true);
		g_logining = false;
		afterLoginDuties();
	}
	return ret;
}

async function idsLoginPrepare(username, password) {
	if (g_logining || g_logined)
		return;
	g_logining = true;
	let ret = g_logined = false;
	let cookies = ((username != localStorage.getItem("username") ||
			password != localStorage.getItem("password")) ?
		"" : localStorage.getItem("cookies"));
	try {
		if (cookies) {
			ret = await chaoxingLogin("", "", true);
			if (ret === true) {
				localStorage.setItem("login_method", "ids");
				localStorage.setItem("username", username);
				localStorage.setItem("password", password);
				g_logining = false;
				g_logined = true;
				afterLoginDuties();
				return true;
			}
		}
		idsLoginCaptcha(username, password);
		ret = true;
	}
	catch (err) {
		ret = err.message;
	}
	return ret;
}

async function idsLoginCaptcha(username, password) {
	let res = await post("/ids/login_prepare");
	assert(res.status_code == 200, "Backend error.");
	let data = res.json();
	assert(!data.err, data.err);
	let b = document.getElementById("login-button");
	let c = document.getElementById("ids-login-captcha-container-div");
	let l = document.getElementById("ids-login-captcha-line-div");
	let s = document.getElementById("ids-login-captcha-input");
	s.oninput = (() => {
		l.style.left = `${(c.offsetWidth - 3) * s.value / 280}px`;
	});
	document.getElementById("ids-login-captcha-button").onclick = (() => {
		idsLoginFinish(username, password, s.value)
		.then((ret) => {
			b.disabled = false;
			if (ret === true)
				afterLoginDuties();
			else
				alert(`Login failed. (${ret})`);
		});
		displayTag("ids-login-captcha-div");
	});
	let img = document.getElementById("ids-login-captcha-img");
	img.onload = (() => {
		l.style.left = `${s.value = 0}px`;
		displayTag("ids-login-captcha-div");
	});
	img.src = `data:image/png;base64,${data.big_img_src}`;
	b.disabled = true;
}

async function idsLoginFinish(username, password, vcode) {
	if (!g_logining || g_logined)
		return;
	let ret = false;
	try {
		let res = await post("/ids/login_finish", {
			"username": username,
			"password": password,
			"vcode": vcode
		});
		assert(res.status_code == 200, "Backend error.");
		let data = res.json();
		assert(!data.err, data.err);
		localStorage.setItem("login_method", "ids");
		localStorage.setItem("username", username);
		localStorage.setItem("password", password);
		localStorage.setItem("cookies", data["cookies"]);
		localStorage.setItem("fid", data["fid"]);
		ret = true;
	}
	catch (err) {
		ret = err.message;
	}
	g_logined = (ret === true);
	g_logining = false;
	return ret;
}