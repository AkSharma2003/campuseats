
const express = require('express');
const path = require('path');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = 3000;

// JWT secret
const JWT_SECRET = process.env.JWT_SECRET;

if (!JWT_SECRET) {
    throw new Error('Please set JWT_SECRET environment variable');
}

// Middleware
app.use(express.json());

// Serve frontend
app.use(express.static(path.join(__dirname, 'public')));


// USERS
// Seed two users with different roles

const users = [
    {
        id: 1,
        email: 'customer@campuseats.com',
        passwordHash: bcrypt.hashSync('customer123', 10),
        role: 'customer'
    },
    {
        id: 2,
        email: 'restaurant@campuseats.com',
        passwordHash: bcrypt.hashSync('restaurant123', 10),
        role: 'restaurant'
    }
];


// EXISTING MENU DATA

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


// ROUTE 1: LOGIN

app.post('/login', (req, res) => {

    const { email, password } = req.body;

    const user = users.find(u => u.email === email);

    if (!user || !bcrypt.compareSync(password, user.passwordHash)) {
        return res.status(401).json({
            error: 'Invalid email or password'
        });
    }

    const token = jwt.sign(
        {
            sub: user.id,
            email: user.email,
            role: user.role
        },
        JWT_SECRET,
        {
            expiresIn: '1h'
        }
    );

    res.json({
        message: 'Login successful',
        token: token,
        role: user.role
    });
});


// ROUTE 2: AUTHENTICATION MIDDLEWARE

function auth(req, res, next) {

    const header = req.headers.authorization;

    if (!header || !header.startsWith('Bearer ')) {
        return res.status(401).json({
            error: 'Missing authentication token'
        });
    }

    const token = header.split(' ')[1];

    try {

        const decoded = jwt.verify(token, JWT_SECRET);

        req.user = decoded;

        next();

    } catch (error) {

        return res.status(401).json({
            error: 'Invalid or expired token'
        });

    }
}


// ROUTE 3: ROLE AUTHORIZATION MIDDLEWARE

function requireRole(...roles) {

    return (req, res, next) => {

        if (!req.user || !roles.includes(req.user.role)) {
            return res.status(403).json({
                error: 'Forbidden: insufficient permissions'
            });
        }

        next();
    };
}


// ROUTE 4: GET ALL ITEMS
// Any authenticated user can read

app.get('/items', auth, (req, res) => {
    res.json(items);
});


// ROUTE 5: GET ONE ITEM
// Any authenticated user can read

app.get('/items/:id', auth, (req, res) => {

    const id = Number(req.params.id);

    const item = items.find(item => item.id === id);

    if (!item) {
        return res.status(404).json({
            error: 'Dish not found'
        });
    }

    res.json(item);
});


// ROUTE 6: ADD NEW ITEM
// Only restaurant and admin can write

app.post(
    '/items',
    auth,
    requireRole('restaurant', 'admin'),
    (req, res) => {

        const { name, price, available } = req.body;

        if (typeof name !== 'string' || !name.trim()) {
            return res.status(422).json({
                error: 'Name is required'
            });
        }

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

        const newItem = {
            id: nextId++,
            name: name.trim(),
            price: price ?? 0,
            available: available ?? true
        };

        items.push(newItem);

        res.status(201).json(newItem);
    }
);


// START SERVER

app.listen(PORT, () => {
    console.log(
        `Secure CampusEats API running at http://localhost:${PORT}`
    );
});
