###TO_EVAL###
function addVariableInput() {
    let random_id = (Math.random() + 1).toString(36).substring(2);

    const sidebar = document.querySelector('.sidebar ul');
    const variableGroup = document.createElement('li');
    variableGroup.id = random_id;
    variableGroup.className = 'variable-group';

    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.id = 'var_name';
    nameInput.placeholder = 'Variable Name';

    const valueInput = document.createElement('input');
    valueInput.type = 'text';
    valueInput.id = 'var_value';
    valueInput.placeholder = 'Variable Value';

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'x';
    deleteButton.onclick = () => {
        sidebar.removeChild(variableGroup);
        let current_vars = JSON.parse(localStorage.getItem("vars")) ?? [];
        current_vars.pop(random_id);
        localStorage.setItem("vars", JSON.stringify(current_vars));
    };

    variableGroup.appendChild(nameInput);
    variableGroup.appendChild(valueInput);
    variableGroup.appendChild(deleteButton);

    sidebar.appendChild(variableGroup);
    let current_vars = JSON.parse(localStorage.getItem("vars")) ?? [];
    current_vars.push(random_id);
    localStorage.setItem("vars", JSON.stringify(current_vars));
}

function loadVariableInput(name, value){
    let random_id = (Math.random() + 1).toString(36).substring(2);

    const sidebar = document.querySelector('.sidebar ul');
    const variableGroup = document.createElement('li');
    variableGroup.id = random_id;
    variableGroup.className = 'variable-group';

    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.id = 'var_name';
    nameInput.value = name;

    const valueInput = document.createElement('input');
    valueInput.type = 'text';
    valueInput.id = 'var_value';
    valueInput.value = value;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'x';
    deleteButton.onclick = () => {
        sidebar.removeChild(variableGroup);
        console.log(`deleting ${random_id}`)
        let current_vars = JSON.parse(localStorage.getItem("vars")) ?? [];
        let index = current_vars.indexOf(random_id);
        current_vars.splice(index, 1);
        localStorage.setItem("vars", JSON.stringify(current_vars));
    };

    variableGroup.appendChild(nameInput);
    variableGroup.appendChild(valueInput);
    variableGroup.appendChild(deleteButton);

    sidebar.appendChild(variableGroup);
    let current_vars = JSON.parse(localStorage.getItem("vars")) ?? [];
    current_vars.push(random_id);
    localStorage.setItem("vars", JSON.stringify(current_vars));
}

function isValidUrl(string) {
    let url;
    
    try {
      url = new URL(string);
    } catch (_) {
      return false;  
    }
  
    return url.protocol === "http:" || url.protocol === "https:";
}

function getVariables(){
    let vars = JSON.parse(localStorage.getItem("vars")) ?? [];
    let vars_data = {};
    vars.forEach((elem) => {
        const subnodes = document.getElementById(elem).childNodes;
        let var_name = null;
        let var_value = null;
    
        subnodes.forEach((node) => {
            if (node.id === "var_name") {
                var_name = node.value;
            } else if (node.id === "var_value") {
                var_value = node.value;
            }
            if (var_name && var_value) {
                return;
            }
        });
    
        if (var_name !== null && var_value !== null) {
            vars_data[var_name] = var_value;
        }
    });
    return vars_data;
}

function parseAndExec(){
    let vars_data = getVariables();
    let exec_frame = document.getElementById("exec_frame");
    let url = document.getElementById("url").value;
    if(!isValidUrl(url)) {
        Swal.fire({
            title: "PostPlayground",
            text: "URL is undefined or invalid.",
            icon: "error"
        });
        return;
    }
    exec_frame.contentWindow.postMessage({"vars":{"variables":vars_data, "url": url, "originUrl": location.hostname+":"+location.port }}, "*");
}

async function saveProject(){
    let vars_data = getVariables();
    let url = document.getElementById("url").value;
    if(!isValidUrl(url)) {
        Swal.fire({
            title: "PostPlayground",
            text: "URL is undefined or invalid.",
            icon: "error"
        });
        return;
    }
    fetch(`/api/playground/${current_project_id}`,{
        credentials: "include", 
        method: "POST", 
        body: new URLSearchParams({"data": 
            JSON.stringify({
                "vars_data":vars_data, 
                "url": url
            })
        })
    })
    .then(async (resp) => {
        return await resp.json();
    })
    .then((resp) => {
        if(resp.status === 200) {
            Swal.fire({
                title: "PostPlayground",
                text: "Project has been saved.",
                icon: "success"
            });
        } else {
            Swal.fire({
                title: "PostPlayground",
                text: "An error occured while saving the project, please try again.",
                icon: "error"
            });
        }
    })
    .catch((_) => {
        Swal.fire({
            title: "PostPlayground",
            text: "An error occured while saving the project, please try again.",
            icon: "error"
        });
    })
}

async function getProjects() {
    fetch("/api/playgrounds", {
        credentials: "include"
    })
    .then((resp) => resp.json())
    .then((fetch_res) => {
        if(fetch_res.status === 200) {
            const projects = fetch_res.data;
            if(projects.length <= 0) {
                Swal.fire({
                    title: "PostPlayground",
                    text: "You don't have any projects except this new one, time to try our tool !",
                    icon: "success"
                });
                return;
            }
            const projectItems = projects.map(project => {
                return `
                    <div class="project-item" data-uuid="${project.uuid}" style="padding: 12px; margin: 6px 0; border: 1px solid #ddd; border-radius: 8px; cursor: pointer; background-color: #f9f9f9; transition: background-color 0.3s;">
                        ${project.uuid}
                    </div>
                `;
            }).join("");
    
            const popupContent = `
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px;">
                    <h2 style="font-size: 1.5rem; margin: 0;">Choose a Project</h2>
                    <button id="closePopup" style="border: none; background: none; font-size: 1.5rem; color: red; cursor: pointer;">&times;</button>
                </div>
                <div style="padding: 20px;">
                    ${projectItems}
                </div>
            `;
    
            Swal.fire({
                html: popupContent,
                showConfirmButton: false,
                allowOutsideClick: true,
                didOpen: () => {
                    const closeButton = document.getElementById("closePopup");
                    closeButton.addEventListener("click", () => {
                        Swal.close();
                    });
    
                    const projectElements = document.querySelectorAll(".project-item");
                    projectElements.forEach(item => {
                        item.addEventListener("click", () => {
                            const uuid = item.getAttribute("data-uuid");
                            if (uuid) {
                                window.top.location.href = `/playground?id=${uuid}`;
                            }
                        });
                    });
                }
            });
        } else {
            Swal.fire({
                title: "PostPlayground",
                text: "An error occured while fetching projects. This page will be reloaded.",
                icon: "error"
            }).then(() => {
                location.reload();
            });
        }
    });
}    

###EOF_EVAL###