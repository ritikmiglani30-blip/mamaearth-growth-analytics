CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT,
    city TEXT,
    city_tier INTEGER,
    signup_date TEXT,
    acquisition_source TEXT
);

CREATE TABLE product (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    product_id TEXT,
    order_date TEXT,
    quantity INTEGER,
    discount_pct REAL,
    payment_method TEXT,
    rating REAL,
    returned INTEGER,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES product(product_id)
);