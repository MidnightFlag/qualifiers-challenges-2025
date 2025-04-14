const hostname = window.location.hostname;
let socket, port;

if (getCookie("port") != null) {
    port = getCookie("port");
}

else {
    port = prompt("Please specify the port number provided by dynamic deploy for the WebSocket:");

    while (isNaN(parseInt(port)) || parseInt(port) <= 0) {
        port = prompt("Please specify the port number provided by dynamic deploy for the WebSocket:");
    }
}

function addCookie(name, value) {
    const date = new Date();
    date.setTime(date.getTime() + (60 * 60 * 1000));
    const expiration = "; expires=" + date.toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}${expiration}; path=/`;
}

function getCookie(name) {
    const match = document.cookie.split('; ').find(row => row.startsWith(name + '='));
    const value = match && decodeURIComponent(match.split('=')[1]);
    const port = parseInt(value, 10);
    return !isNaN(port) ? port : null;
}

function isCookieSet(name) {
    return getCookie(name) !== null;
}
  

function connectWebSocket(port) {
    socket = new WebSocket("ws://" + hostname + ":" + port);

    socket.onopen = function(event) {
        console.log("WebSocket connection established.");
        if (!isCookieSet("port")) {
            addCookie("port", port);
        }
    };

    socket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            displayMessage(data);
        } catch (error) {
            console.error("Error while parsing JSON :", error);
        }
    };

    socket.onclose = function(event) {
        console.log("Websocket closed, trying to reconnect in 5 seconds.");
        setTimeout(connectWebSocket(port), 5000);
    };

    socket.onerror = function(error) {
        console.error("WebSocket error: ", error);
    };
}

function displayMessage(data) {
    const messageList = document.getElementById("solid-chat-box");
    const listItem = document.createElement("p");
    listItem.innerHTML = `<span class="text-green-300 text-sm">[${data.time}]</span> 
                                    <span class="font-bold">${data.player}</span>: ${data.message}`;
    messageList.appendChild(listItem);
}


connectWebSocket(port);