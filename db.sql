DROP DATABASE IF EXISTS webstore_db;

CREATE DATABASE webstore_db;

\c webstore_db

--Customers----
INSERT INTO customers (email, name, password, address)
VALUES
     ('owens.eugene@yahoo.com', 'Eugene Owens', 1234, '458 cocanut isle dr'),
     ('owens.sandy@yahoo.com', 'Sandy Owens', 1234, '458 cocanut isle dr'),
     ('Henry.Devyon@yahoo.com', 'Devyon Henry', 1234, '458 cocanut isle dr'),
     ('Spencer.shavonne@yahoo.com', 'Shavonne Spencer', 1234, '458 cocanut isle dr'),
     ('owens.nia@yahoo.com', 'Nia Owens', 1234, '458 cocanut isle dr'),
     ('john.doe@example.com', 'John Doe', 1234, '123 Main St');

     
-- Products
INSERT INTO products (name, description, price, image, availability)
VALUES
    ('T-Shirt', 'Soft and comfortable womens red t-shirt made from 100% cotton.', 19.99, 'https://burst.shopifycdn.com/photos/womens-red-t-shirt.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Smartphone', 'High-end smartphone with a large display and powerful processor.', 799.99, 'product2.jpg', true),
    ('Garden Hose', '50-foot long garden hose made from durable materials.',24.99, 'https://cdn.pixabay.com/photo/2019/01/06/04/54/graphic-3916440_960_720.png', false),
    ('Board Game', 'Family-friendly board game that is easy to learn and fun to play.', 39.99, 'https://burst.shopifycdn.com/photos/bingo-game-flatlay.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Lipstick', 'Long-lasting lipstick that adds vibrant color to your lips.', 9.99, 'https://burst.shopifycdn.com/photos/lipstick-shade-of-red.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Running Shoes', 'Lightweight and breathable shoes designed for running and other physical activities.', 99.99, 'https://burst.shopifycdn.com/photos/pair-of-black-and-white-sneakers.jpg?width=925&format=pjpg&exif=1&iptc=1', true), 
    ('E-Book', 'Digital book that can be read on any device with an e-reader app.', 4.99, 'https://article-imgs.scribdassets.com/2n1a165kw6pafwu/images/fileC0UGH9Q7.jpg', true),
    ('Dog Collar', 'Adjustable dog collar made from high-quality nylon material.', 14.99,'https://burst.shopifycdn.com/photos/green-glowing-dog-collar.jpg?width=925&format=pjpg&exif=1&iptc=1', true),    
    ('Coffee', 'Premium roasted coffee beans from a single origin.', 12.99, 'https://burst.shopifycdn.com/photos/coffee-beans-with-skull.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Bracelet', 'Handmade bracelet with unique design and natural stones.', 29.99, 'https://burst.shopifycdn.com/photos/boho-bangle-bracelet.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Hoodie', 'Warm and cozy hoodie made from soft fleece material.', 39.99, 'https://burst.shopifycdn.com/photos/man-in-hoodie-sits-with-hand-to-chin.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Tablet', 'Lightweight and portable tablet with a high-resolution display.', 299.99, 'https://burst.shopifycdn.com/photos/tablet-and-smartphone-on-table.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Pink Water Bottle', 'Reusable water bottle made from BPA-free plastic.', 12.99, 'https://burst.shopifycdn.com/photos/yoga-mat-flatlay-with-laptop-and-water-bottle.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Black Headphones', 'Comfortable over-ear headphones with high-quality sound.', 49.99, 'https://burst.shopifycdn.com/photos/black-headphones.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Plant', 'Indoor plant that adds a touch of nature to your home or office.', 24.99, 'https://burst.shopifycdn.com/photos/a-hand-holding-a-small-succulent.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Cat Cookies', 'Premium cat food made from real meat and high-quality ingredients.', 9.99,'https://burst.shopifycdn.com/photos/three-fortune-cat-cookies-lined-in-a-container.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Puzzle', '500-piece jigsaw puzzle with beautiful artwork and challenging pieces.', 14.99, 'https://burst.shopifycdn.com/photos/puzzle-pieces-scattered-across-a-surface.jpg?width=925&format=pjpg&exif=1&iptc=1', true),
    ('Guitar', 'Acoustic guitar with rich sound and solid construction.', 399.99, 'https://example.com/guitar.jpg', true),
    ('Wine', 'Full-bodied red wine made from grapes grown in a sunny region.', 29.99, 'https://example.com/wine.jpg', true),
    ('Perfume','Elegant and sophisticated perfume with a delicate floral scent.', 49.99,  'https://burst.shopifycdn.com/photos/black-glass-perfume-bottle-and-spritzer.jpg?width=925&format=pjpg&exif=1&iptc=1', true);

-- Categories
INSERT INTO categories (name)
VALUES
    ('Clothing'),
    ('Electronics'),
    ('Home and Garden'),
    ('Toys and Games'),
    ('Beauty'),
    ('Sports and Outdoors'),
    ('Books and Media'),
    ('Pets'),
    ('Food and Drink'),
    ('Jewelry');

-- Product categories
INSERT INTO product_categories (product_id, category_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 3),
    (5, 4),
    (6, 5),
    (7, 6),
    (8, 6),
    (9, 7),
    (10, 8),
    (11, 9),
    (12, 10),
    (13, 7),
    (14, 8),
    (15, 9),
    (16, 10),
    (17, 1),
    (18, 9),
    (19, 9),
    (20, 9);

---Orders----
INSERT INTO orders (customer_id, total_cost, order_date)
VALUES 
    ('1', 39.96, '2022-01-01'),
    ('2', 29.99, '2022-01-02'),
    ('3', 359.91, '2022-01-03'),
    ('4', 99.99, '2022-01-04');


-- Order products (sample data)
INSERT INTO order_products (order_id, product_id, quantity, price)
VALUES
    (1, 1, 2, 19.98),
    (1, 3, 1, 29.99),
    (2, 2, 1, 19.99),
    (3, 4, 3, 119.97);



