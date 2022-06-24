const getUsernameAndPassword = () => {
    var username = document.getElementById('usernameInput');
    var password = document.getElementById('passwordInput');
    var remember = document.getElementById('rememberInput');

    if (!username.value || !password.value) {
        return { 'result': 'error', 'reason': 'Empty username or password' }
    }

    return {
        'result': 'success',
        'username': username.value,
        'password': password.value,
        'remember': remember.checked
    }
}

const showMessage = (message, type) => {
    var errorContainer = document.getElementById('messageContainer');

    var errorElement = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    errorContainer.innerHTML = errorElement;
}

const setCookie = (cname, cvalue, exdays) => {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

const getCookie = (cname) => {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

const saveUsername = (username) => {
    setCookie('username', username, 10);
}

const loadUsername = () => {
    var username = document.getElementById('usernameInput');
    var savedUsername = getCookie('username');

    if (savedUsername != "") {
        username.value = savedUsername;
    }
}

const validateInput = (username, password) => {
    const usernameRegex = /^[a-zA-Z0-9]+$/;
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;

    if(!username.match(usernameRegex)) {
        showMessage('Username must contain only uppercase and lowercase charaters and numbers');
        return false;
    }
    if(!password.match(passwordRegex)) {
        showMessage('Password must<br>Contain at least 8 characters<br>Contain at least 1 number<br>Contain at least 1 lowercase character<br>Contain at least 1 uppercase character (A-Z)<br>Contains only English letters, numbers and symbols', 'danger')
        return false;
    }

    return true;
}

const authenticate = (form, type, target) => {
    var info = getUsernameAndPassword();

    if (info['result'] != 'success') {
        showMessage(info['reason'], 'danger');
        return false;
    }

    if(type == 'Registered') {
        if(!validateInput(info['username'], info['password'])) {
            return false;
        }
    }

    let data = `username=${info['username']}&password=${info['password']}`;


    fetch(form, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data,
    })
        .then(res => {
            if (!res.ok) {
                throw res
            }
            return res
        })
        .then(res => {
            if (info['remember']) {
                saveUsername(info['username']);
            }
            showMessage(`${type} successfully, redirecting...`, 'success');
            setTimeout(() => {
                window.location.replace(target);
            }, 1000)
        })
        .catch(error => error.json().then(json => showMessage(json['reason'], 'danger')))

    return false;
};