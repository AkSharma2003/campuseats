
// CampusEats frontend with JWT authentication

const dishList = document.getElementById('dishList');
const statusText = document.getElementById('status');
const message = document.getElementById('message');
const dishForm = document.getElementById('dishForm');

const loginForm = document.getElementById('loginForm');
const loginMessage = document.getElementById('loginMessage');
const loginSection = document.getElementById('loginSection');
const userSection = document.getElementById('userSection');
const userInfo = document.getElementById('userInfo');

const addSection = document.querySelector('.form-section form#dishForm')
    .parentElement;

// Store login details for this browser tab
let token = sessionStorage.getItem('token');
let userRole = sessionStorage.getItem('role');


// Show the correct sections based on login status

function updateUI() {

    const loggedIn = Boolean(token && userRole);

    // Show login only when logged out
    loginSection.hidden = loggedIn;

    // Show logout section after login
    userSection.hidden = !loggedIn;

    // Show menu only after login
    document.getElementById('menuSection').hidden = !loggedIn;

    // Show add dish form only for restaurant/admin
    addSection.hidden =
        !loggedIn || !['restaurant', 'admin'].includes(userRole);

    // Enable refresh only after login
    document.getElementById('refreshBtn').disabled = !loggedIn;

    if (loggedIn) {
        userInfo.textContent = 'Logged in as: ' + userRole;
    } else {
        dishList.innerHTML = '';
        statusText.textContent = 'Please login to view the menu.';
    }
}



// Login
loginForm.addEventListener('submit', async (event) => {

    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    loginMessage.textContent = 'Logging in...';

    try {

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Login failed');
        }

        token = result.token;
        userRole = result.role;

        sessionStorage.setItem('token', token);
        sessionStorage.setItem('role', userRole);

        loginMessage.textContent = 'Login successful!';
        loginMessage.className = 'success';

        loginForm.reset();

        updateUI();
        await loadDishes();

    } catch (error) {

        loginMessage.textContent = error.message;
        loginMessage.className = 'error';

    }
});


// Add JWT token to protected API requests
async function apiFetch(url, options = {}) {

    const headers = {
        ...options.headers,
        Authorization: 'Bearer ' + token
    };

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (response.status === 401) {
        logout();
        throw new Error('Session expired. Please login again.');
    }

    return response;
}


// GET: Load all dishes
async function loadDishes() {

    if (!token) {
        statusText.textContent = 'Please login first.';
        return;
    }

    statusText.textContent = 'Loading menu...';

    try {

        const response = await apiFetch('/items');

        const items = await response.json();

        if (!response.ok) {
            throw new Error(items.error || 'Unable to load menu');
        }

        dishList.innerHTML = '';

        items.forEach(item => {

            const card = document.createElement('div');
            card.className = 'dish-card';

            const name = document.createElement('h3');
            name.textContent = item.name;

            const price = document.createElement('p');
            price.textContent = 'Price: ₹' + item.price;

            const availability = document.createElement('p');

            availability.textContent = item.available
                ? 'Available'
                : 'Not Available';

            availability.className = item.available
                ? 'available'
                : 'unavailable';

            card.appendChild(name);
            card.appendChild(price);
            card.appendChild(availability);

            dishList.appendChild(card);

        });

        statusText.textContent =
            items.length + ' dishes loaded successfully.';

    } catch (error) {

        statusText.textContent = error.message;

    }
}


// POST: Add a new dish
dishForm.addEventListener('submit', async (event) => {

    event.preventDefault();

    if (!['restaurant', 'admin'].includes(userRole)) {
        message.textContent = 'You are not allowed to add dishes.';
        message.className = 'error';
        return;
    }

    const name = document.getElementById('name').value.trim();
    const price = Number(document.getElementById('price').value);

    const available =
        document.getElementById('available').value === 'true';

    try {

        const response = await apiFetch('/items', {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                name,
                price,
                available
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Unable to add dish');
        }

        message.textContent =
            'Dish added successfully! ID: ' + result.id;

        message.className = 'success';

        dishForm.reset();

        await loadDishes();

    } catch (error) {

        message.textContent = error.message;
        message.className = 'error';

    }

});


// Logout
function logout() {

    token = null;
    userRole = null;

    sessionStorage.removeItem('token');
    sessionStorage.removeItem('role');

    dishList.innerHTML = '';
    message.textContent = '';
    loginMessage.textContent = '';

    updateUI();
}

document.getElementById('logoutBtn')
    .addEventListener('click', logout);


// Refresh menu
document.getElementById('refreshBtn')
    .addEventListener('click', loadDishes);


// Restore session when page reloads
updateUI();

if (token && userRole) {
    loadDishes();
}
