const DOMEN = "http://127.0.0.1:8000/";

document.getElementById("form-login").addEventListener("submit", async function(event) {
event.preventDefault();
const formData = {
    login: document.getElementById("login").value,
    password: document.getElementById("password").value
}

const response = await fetch(`${DOMEN}login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
const response_body = await response.json();
window.location.href = `${DOMEN}${response_body.login}`;
});
