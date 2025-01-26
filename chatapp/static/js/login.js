import { getCookies } from "/static/js/utils.js"
import { login, userExists, adminPassword } from "/static/js/events.js"

let cookies = getCookies()

// attempting to go directly to the admin page redirects here with cookie
// alert the user and delete the cookie
if (cookies['auth-reject']) {
    alert(JSON.parse(cookies['auth-reject']))
}

// remove all cookies gained by logging in
['auth-reject', 'cookie', 'module'].forEach((cookie) => { document.cookie = `esther-${cookie}=; max-age=0`})

const Username = document.getElementById('username')
const Password = document.getElementById('password')
const Login    = document.getElementById('login')
const Error    = document.getElementById('error')

async function performLogin() {
    
    let user = Username.value.trim().toLowerCase()

    if (user === 'admin') {
        // Check password for admin
        const response = await adminPassword(Password.value)
        if (response.check) {
            document.cookie = `esther-cookie=${response.cookie}; path=/`
            window.location.href = '/dashboard'
        } else {
            showErrorMessage('Incorrect password. Please try again.');
        }
    } else {
        
        if (await userExists(user)) {
            const cookie = await login(user)
            document.cookie=`esther-cookie=${cookie}; path=/`
            window.location.href = `/home`
        } else {
            showErrorMessage('Username not recognised. Please try again.')
        }
    }
}

// Function to show error message
function showErrorMessage(message) {
    Error.textContent = message;
    Error.style.display = 'block';
    Error.style.color = 'red'; // Set color to red for error message
}

// Function to check username and initiate login process
function checkUsername() {

    if (Username.value.trim().toLowerCase() === 'admin') {
        // Show password field if username is 'admin'
        Password.style.display = 'block';
        Password.focus(); // Focus on password field
    } else {
        // Hide password field for other usernames
        Password.style.display = 'none';
    }
}

// Handle Enter key press event in the username input field
Username.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        checkUsername();
    }
});

// Handle Enter key press event in the password input field
Password.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        performLogin();
    }
});

Login.addEventListener('click', () => {
    performLogin();
})

// JavaScript to handle input focus


// Handle input event in the username input field to hide error message and manage password field visibility
Username.addEventListener('input', function () {

    Error.style.display = 'none'; // Hide error message initially

    if (Username.value !== 'admin') {
        // Hide password field if username is not 'admin'
        Password.value = '';
        Password.style.display = 'none';
    }

});

Password.addEventListener('input', function () {

    Error.style.display = 'none'; // Hide error message initially

});

Username.addEventListener('focus', function() {
    Username.style.textAlign = 'left';
});

Username.addEventListener('blur', function() {
    if (Username.value === '') {
        Username.style.textAlign = 'center';
    }
});