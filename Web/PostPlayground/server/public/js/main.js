const v4 = new RegExp(/^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i);

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function getId(){
    const id = getQueryParam("id");
    if(id) {
        return id;
    } else {
        return undefined;
    }
}

async function report(){
    let uuid = document.getElementById("render_frame").contentDocument.getElementById("project_id_text").innerText.split(": ")[1];
    fetch("/api/bot", {
        method: "POST",
        credentials: "include",
        body: new URLSearchParams({"uuid":uuid})
    })
    .then(async (resp) => {
        return await resp.json();
    })
    .then((resp) => {
        if(resp.status === 200) {
            Swal.fire({
                title: "PostPlayground",
                text: resp.data,
                icon: "success"
            });
        } else {
            Swal.fire({
                title: "PostPlayground",
                text: resp.error,
                icon: "error"
            });
        }
    })
    .catch((_) => {
        Swal.fire({
            title: "PostPlayground",
            text: "Unknown error occured",
            icon: "error"
        });
    })
}

let render_frame = document.getElementById("render_frame");

render_frame.addEventListener("load", function(_) { 
    const id = getId();
    if(id){
        if(v4.exec(id)) {
            render_frame.contentWindow.postMessage({"action":"load_scripts", "vars":{"srcs":["/js/render_frame.js"]}});
            render_frame.contentWindow.postMessage({"action":"load_variable","vars":{"id":id}}, "*");
        } else {
            Swal.fire({
                title: "PostPlayground",
                text: "Provided id is incorrect, the page will be reloaded to create a new one",
                icon: "error"
            })
            .then(() => {
                location = "/playground";
            })
        }
    } else {
        render_frame.contentWindow.postMessage({"action":"load_scripts", "vars":{"srcs":["/js/render_frame.js"]}});
        render_frame.contentWindow.postMessage({"action":"load_variable","vars":{"id":"NULL"}}, "*");
    }
});

window.addEventListener("message", function (event) {
    render_frame.contentWindow.postMessage(event.data);
})