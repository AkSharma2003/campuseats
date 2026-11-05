
// HTML elements
const dishList = document.getElementById('dishList');

const statusText = document.getElementById('status');

const message = document.getElementById('message');

const dishForm = document.getElementById('dishForm');


// GET: Load all dishes
async function loadDishes() {

    statusText.textContent = 'Loading menu...';

    try {

        const response = await fetch('/items');

        if (!response.ok) {
            throw new Error('Unable to load menu');
        }

        const items = await response.json();

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

    const name = document.getElementById('name').value.trim();

    const price = Number(
        document.getElementById('price').value
    );

    const available =
        document.getElementById('available').value === 'true';

    try {

        const response = await fetch('/items', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                name: name,
                price: price,
                available: available
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


// Refresh button
document.getElementById('refreshBtn')
    .addEventListener('click', loadDishes);


// Load menu when page opens
loadDishes();
