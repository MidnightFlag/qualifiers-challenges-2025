const puppeteer = require("puppeteer");

const delay = (time) => {
    return new Promise(resolve => setTimeout(resolve, time));
}

async function goto(uuid, base_url, user, pwd) {
    console.log("[BOT] - Wake up !");
	const browser = await puppeteer.launch({
		headless: "new",
		ignoreHTTPSErrors: true,
		args: [
            "--no-sandbox",
            "--ignore-certificate-errors",
            "--disable-web-security",
            "--disable-gpu"
        ],
        executablePath: "/usr/bin/chromium"
    });

	const page = await browser.newPage();

	try {
        console.log("[BOT] - Logging into application");
	    await page.goto(`${base_url}/login`);
        await page.waitForSelector('#username');
        await page.type("#username", user);
        await page.type("#password", pwd);
        await Promise.all([
            page.click('#submit'),
            page.waitForNavigation()
        ]);
	} catch {
        return false;
    }

    try {
        console.log(`[BOT] - Fetching URL : ${base_url}/playground?id=${uuid}`);
        await page.goto(`${base_url}/playground?id=${uuid}`);
        await delay(5000);
    } catch(e) {
        console.log("[BOT] - Nightmare...");
        console.log(e);
        return false;
    }

    console.log("[BOT] - Go to sleep...");
    browser.close();
	return true;
}

module.exports = {
    goto
}