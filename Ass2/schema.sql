CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ACCOUNTS SERVICE
CREATE TABLE accounts_users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts_addresses (
    address_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    label VARCHAR(80),
    building VARCHAR(150) NOT NULL,
    room VARCHAR(80),
    campus VARCHAR(120),
    instructions TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_addresses_user
        FOREIGN KEY (user_id) REFERENCES accounts_users(user_id)
        ON DELETE CASCADE
);

-- CATALOGUE SERVICE
CREATE TABLE catalogue_restaurants (
    restaurant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    is_open BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE catalogue_menus (
    menu_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID NOT NULL,
    name VARCHAR(120) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_menus_restaurant
        FOREIGN KEY (restaurant_id) REFERENCES catalogue_restaurants(restaurant_id)
        ON DELETE CASCADE
);

CREATE TABLE catalogue_menu_items (
    item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_id UUID NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_items_menu
        FOREIGN KEY (menu_id) REFERENCES catalogue_menus(menu_id)
        ON DELETE CASCADE
);

-- ORDERS SERVICE
CREATE TABLE orders_orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,            
    address_id UUID NOT NULL,         
    status VARCHAR(30) NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount >= 0),
    placed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders_order_items (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    item_id UUID NOT NULL,             
    item_name VARCHAR(150) NOT NULL,   
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders_orders(order_id)
        ON DELETE CASCADE
);

-- PAYMENTS SERVICE
CREATE TABLE payments_payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,           
    amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(30) NOT NULL,
    provider_transaction_id VARCHAR(255) UNIQUE,
    paid_at TIMESTAMPTZ
);

CREATE TABLE payments_refunds (
    refund_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id UUID NOT NULL,
    amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    reason TEXT,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_refunds_payment
        FOREIGN KEY (payment_id) REFERENCES payments_payments(payment_id)
        ON DELETE CASCADE
);

-- DELIVERY SERVICE
CREATE TABLE delivery_riders (
    rider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    status VARCHAR(30) NOT NULL DEFAULT 'available'
);

CREATE TABLE delivery_assignments (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,             
    rider_id UUID NOT NULL,
    status VARCHAR(30) NOT NULL,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    picked_up_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    CONSTRAINT fk_assignments_rider
        FOREIGN KEY (rider_id) REFERENCES delivery_riders(rider_id)
        ON DELETE RESTRICT
);


-- NOTIFICATIONS SERVICE
CREATE TABLE notifications_notifications (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,             
    order_id UUID,                      
    type VARCHAR(40) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMPTZ
);