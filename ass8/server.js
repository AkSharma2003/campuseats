
const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());

// Serve frontend files
app.use(express.static(path.join(__dirname, 'public')));

// In-memory data
let items = [
    {
        id: 1,
        name: 'Veg Thali',
        price: 90,
        available: true
    },
    {
        id: 2,
        name: 'Paneer Roll',
        price: 70,
        available: true
    },
    {
        id: 3,
        name: 'Masala Dosa',
        price: 60,
        available: true
    },
    {
        id: 4,
        name: 'Chicken Biryani',
        price: 150,
        available: false
    }
];

let nextId = 5;


// ROUTE 1: GET ALL ITEMS
app.get('/items', (req, res) => {
    res.json(items);
});


// ROUTE 2: GET ONE ITEM BY ID
app.get('/items/:id', (req, res) => {

    const id = Number(req.params.id);

    const item = items.find(item => item.id === id);

    if (!item) {
        return res.status(404).json({
            error: 'Dish not found'
        });
    }

    res.json(item);
});


// ROUTE 3: ADD NEW ITEM
app.post('/items', (req, res) => {

    const { name, price, available } = req.body;

    // Validate required name
    if (typeof name !== 'string' || !name.trim()) {
        return res.status(422).json({
            error: 'Name is required'
        });
    }

    // Validate price
    if (
        price !== undefined &&
        (typeof price !== 'number' ||
         !Number.isFinite(price) ||
         price < 0)
    ) {
        return res.status(422).json({
            error: 'Price must be a valid non-negative number'
        });
    }

    // Create new item
    const newItem = {
        id: nextId++,
        name: name.trim(),
        price: price ?? 0,
        available: available ?? true
    };

    items.push(newItem);

    // Return 201 Created
    res.status(201).json(newItem);
});


// START SERVER
app.listen(PORT, () => {
    console.log(
        `CampusEats REST API running at http://localhost:${PORT}`
    );
});
