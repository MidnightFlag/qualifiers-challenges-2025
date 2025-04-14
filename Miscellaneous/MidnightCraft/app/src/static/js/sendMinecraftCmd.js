
function clean(text) {
    return text.replace(/§./g, '');
}

async function sendCommand() {
const command = document.getElementById('cmd').value;
if (!command) return;

try {
    const response = await fetch('/send_minecraft_cmd', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ cmd: command })
    });

    const result = await response.json();
    result.output = clean(result.output);
    const responseDiv = document.getElementById('commandResponse');
    responseDiv.innerText = result.output;
    responseDiv.hidden = false;
    document.getElementById('cmd').value = '';
} catch (error) {
    console.error('Error:', error);
    const responseDiv = document.getElementById('commandResponse');
    responseDiv.innerText = 'Une erreur est survenue.';
    responseDiv.hidden = false;
}
}

document.getElementById('cmd_btn').addEventListener('click', sendCommand);

document.getElementById('cmd').addEventListener('keypress', async (event) => {
if (event.key === 'Enter') {
    event.preventDefault();
    await sendCommand();
}
});