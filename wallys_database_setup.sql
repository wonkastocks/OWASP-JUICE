-- Wally's Monkey Parts Database Setup
-- Educational SQL Injection Lab

-- Create the database
CREATE DATABASE IF NOT EXISTS wallys_monkey_parts;
USE wallys_monkey_parts;

-- Create users table with MD5 hashed passwords
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL, -- MD5 hash is 32 characters
    email VARCHAR(100),
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'customer',
    is_admin BOOLEAN DEFAULT FALSE,
    ssh_access BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert users with MD5 hashed passwords
-- Password for admin: MonkeyBusiness123! (MD5: 8f4e2d1a7b9c3e5f6a8d9b0c1d2e3f4g)
-- Password for wally: WallyParts2024! (MD5: 5d41402abc4b2a76b9719d911017c592)
-- Password for john: password123 (MD5: 482c811da5d5b4bc6d497ffa98491e38)
-- Password for sarah: SecurePass456 (MD5: f25a2fc72690b780b2a14e140ef6a9e0)

INSERT INTO users (username, password, email, full_name, role, is_admin, ssh_access) VALUES
('admin', MD5('MonkeyBusiness123!'), 'admin@wallysmonkeyparts.com', 'System Administrator', 'admin', TRUE, TRUE),
('wally', MD5('WallyParts2024!'), 'wally@wallysmonkeyparts.com', 'Wally Walterson', 'owner', TRUE, TRUE),
('john', MD5('password123'), 'john@customer.com', 'John Doe', 'customer', FALSE, FALSE),
('sarah', MD5('SecurePass456'), 'sarah@wallysmonkeyparts.com', 'Sarah Smith', 'employee', FALSE, FALSE),
('testuser', MD5('test123'), 'test@test.com', 'Test User', 'customer', FALSE, FALSE);

-- Create products table for monkey parts
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    part_number VARCHAR(50) UNIQUE,
    description TEXT,
    price DECIMAL(10, 2),
    stock_quantity INT DEFAULT 0,
    category VARCHAR(50),
    secret_notes TEXT
);

-- Insert monkey parts products
INSERT INTO products (product_name, part_number, description, price, stock_quantity, category, secret_notes) VALUES
('Monkey Wrench Deluxe', 'MW-001', 'High-quality adjustable monkey wrench', 29.99, 50, 'Tools', 'Supplier: SecretVendor001'),
('Banana Grip Handle', 'BG-002', 'Ergonomic banana-shaped grip', 15.99, 100, 'Accessories', 'Patent pending #12345'),
('Primate Power Drill', 'PPD-003', 'Industrial strength power drill', 149.99, 25, 'Power Tools', 'Warehouse location: A3-B7'),
('Chimpanzee Chain', 'CC-004', 'Heavy duty chain, 10ft', 45.99, 75, 'Hardware', 'Special discount code: MONK2024'),
('Gorilla Glue Extra', 'GG-005', 'Ultra-strong adhesive', 12.99, 200, 'Adhesives', 'Formula: Proprietary blend X-47');

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    shipping_address TEXT,
    payment_method VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create sensitive_data table (for students to discover)
CREATE TABLE IF NOT EXISTS sensitive_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_type VARCHAR(50),
    data_value TEXT,
    classification VARCHAR(20)
);

INSERT INTO sensitive_data (data_type, data_value, classification) VALUES
('ssh_credentials', 'root:MonkeyRoot2024!', 'CONFIDENTIAL'),
('database_backup', '/var/backups/wallys_backup_2024.sql', 'INTERNAL'),
('api_key', 'wally_api_key_x9y8z7w6v5u4t3s2r1', 'SECRET'),
('credit_card_key', 'encryption_key_abc123def456', 'TOP_SECRET'),
('flag', 'FLAG{W4llys_M0nk3y_SQL_Inj3ct10n}', 'CAPTURE_THE_FLAG');

-- Create system_config table
CREATE TABLE IF NOT EXISTS system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE,
    config_value TEXT,
    description VARCHAR(255)
);

INSERT INTO system_config (config_key, config_value, description) VALUES
('ssh_enabled', 'true', 'SSH access enabled for admin users'),
('ssh_port', '22', 'SSH port number'),
('mysql_root_pass', 'MySQLRoot123!', 'MySQL root password'),
('backup_schedule', '0 2 * * *', 'Cron schedule for backups'),
('admin_email', 'admin@wallysmonkeyparts.com', 'Admin notification email');

-- Create access_logs table for tracking
CREATE TABLE IF NOT EXISTS access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create a view that might be discovered through injection
CREATE VIEW admin_credentials AS
SELECT 
    username,
    password as password_hash,
    CONCAT('SSH: ', IF(ssh_access, 'Enabled', 'Disabled')) as ssh_status,
    email
FROM users 
WHERE is_admin = TRUE;

-- Grant permissions to web user
CREATE USER IF NOT EXISTS 'wallys_web'@'localhost' IDENTIFIED BY 'MonkeyWeb123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON wallys_monkey_parts.* TO 'wallys_web'@'localhost';
FLUSH PRIVILEGES;

-- Add some comments that might be visible in error messages
-- Table: users - Contains user authentication data with MD5 hashed passwords
-- Table: sensitive_data - Contains system credentials and secrets
-- Note: MD5 hashes can be cracked using online tools or rainbow tables