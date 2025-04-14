const urlParams = new URLSearchParams(window.location.search);
let currentFolder = urlParams.get('folder') || '';

const SwalDark = Swal.mixin({
    customClass: {
        popup: 'swal2-dark',
    },
    background: '#111',
    color: '#fff',
    confirmButtonColor: '#00ffe7',
    cancelButtonColor: '#ff0055',
});

function escapeHTML(str) {
    return str
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}


function updateBreadcrumb() {
    const parts = currentFolder.split('/').filter(Boolean);
    let html = '<a href="/home">$> root</a>';
    let path = '';
    parts.forEach(part => {
        path += '/' + part;
        const safeText = escapeHTML(part);
        const safePath = encodeURIComponent(path.slice(1));
        html += ' / <a href="/home?folder=' + safePath + '">' + safeText + '</a>';
    });
    document.getElementById('breadcrumb').innerHTML = html;
}


function listFolder() {
    fetch('/api/folder/list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'folder=' + encodeURIComponent(currentFolder)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'ok') {
            const folders = document.getElementById('folders');
            folders.innerHTML = '';
            data.folders.forEach(f => {
                const div = document.createElement('div');
                div.className = 'item';
                const icon = document.createElement('span');
                icon.className = 'item-icon';
                icon.textContent = '📁';

                const link = document.createElement('a');
                const folderPath = currentFolder ? currentFolder + '/' + f : f;
                link.href = `/home?folder=${encodeURIComponent(folderPath)}`;
                link.textContent = f;

                const br = document.createElement('br');

                const delBtn = document.createElement('button');
                delBtn.innerHTML = '🗑️';
                delBtn.onclick = () => deleteItem(f, true);

                div.appendChild(icon);
                div.appendChild(link);
                div.appendChild(br);
                div.appendChild(delBtn);
                folders.appendChild(div);
            });

            const files = document.getElementById('files');
            files.innerHTML = '';
            data.files.forEach(f => {
                const div = document.createElement('div');
                div.className = 'item';
                const icon = document.createElement('span');
                icon.className = 'item-icon';
                icon.textContent = '🖼️';
                const nameLink = document.createElement('a');
                nameLink.href = '#';
                nameLink.textContent = f;
                nameLink.onclick = (e) => {
                    e.preventDefault();
                    downloadFile(f);
                };

                const br = document.createElement('br');

                const delBtn = document.createElement('button');
                delBtn.innerHTML = '🗑️';
                delBtn.onclick = () => deleteItem(f, false);

                div.appendChild(icon);
                div.appendChild(nameLink);
                div.appendChild(br);
                div.appendChild(delBtn);
                files.appendChild(div);
            });
        }
    });
}

function deleteItem(name, isFolder) {
    SwalDark.fire({
        title: 'Are you sure?',
        text: `Delete ${name}? This cannot be undone.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel',
    }).then(result => {
        if (result.isConfirmed) {
            const endpoint = isFolder ? '/api/folder/delete' : '/api/files/delete';
            let params = new URLSearchParams();
            if (isFolder) {
                params.append('folder', currentFolder ? currentFolder + '/' + name : name);
            } else {
                params.append('folder', currentFolder);
                params.append('filename', name);
            }

            fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: params
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    SwalDark.fire('Deleted!', `${name} was deleted.`, 'success');
                    listFolder();
                } else {
                    SwalDark.fire('Error', data.message || 'Could not delete.', 'error');
                }
            });
        }
    });
}


function openCreateFolder() {
    SwalDark.fire({
        title: 'Create New Folder',
        input: 'text',
        inputLabel: 'Folder name',
        inputPlaceholder: 'Enter folder name',
        showCancelButton: true,
        confirmButtonText: 'Create',
        preConfirm: (name) => {
            if (!name) return SwalDark.showValidationMessage('Folder name cannot be empty');
            if (name.includes('..') || name.includes('/') || name.includes('\\')) {
                return SwalDark.showValidationMessage('Invalid folder name');
            }

            let fullPath = currentFolder ? currentFolder + '/' + name : name;

            return fetch('/api/folder/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'folder=' + encodeURIComponent(fullPath)
            })
            .then(res => res.json())
            .then(data => {
                if (data.status !== 'ok') {
                    throw new Error(data.message || 'Failed to create folder');
                }
                return data;
            })
            .catch(err => {
                SwalDark.showValidationMessage(err.message);
            });
        }
    }).then(result => {
        if (result.isConfirmed) {
            SwalDark.fire('Created!', 'Folder has been created.', 'success');
            listFolder();
        }
    });
}

function openUploadFile() {
    SwalDark.fire({
        title: 'Upload Image',
        html: `
            <input type="file" id="swal-file" accept=".png,.jpg,.jpeg" class="swal2-input">
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: 'Upload',
        preConfirm: () => {
            const fileInput = document.getElementById('swal-file');
            const file = fileInput.files[0];

            if (!file) {
                SwalDark.showValidationMessage('Please select a file.');
                return false;
            }

            const filename = file.name;

            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const base64 = e.target.result.split(',')[1];
                    fetch('/api/files/upload', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: new URLSearchParams({
                            folder: currentFolder,
                            filename: filename,
                            content: base64
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status !== 'ok') {
                            throw new Error(data.message || 'Upload failed');
                        }
                        resolve(data);
                    })
                    .catch(err => {
                        SwalDark.showValidationMessage(err.message);
                    });
                };
                reader.readAsDataURL(file);
            });
        }
    }).then(result => {
        if (result.isConfirmed) {
            SwalDark.fire('Uploaded!', 'Your image has been uploaded.', 'success');
            listFolder();
        }
    });
}

function downloadFile(name) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/api/files/download';
    form.style.display = 'none';

    const folderInput = document.createElement('input');
    folderInput.name = 'folder';
    folderInput.value = currentFolder;
    form.appendChild(folderInput);

    const filenameInput = document.createElement('input');
    filenameInput.name = 'filename';
    filenameInput.value = name;
    form.appendChild(filenameInput);

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

updateBreadcrumb();
listFolder();