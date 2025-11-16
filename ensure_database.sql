-- Ensure the vulnerable_db database and users table exist

CREATE DATABASE IF NOT EXISTS vulnerable_db;
USE vulnerable_db;

-- Create users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users if table is empty
INSERT IGNORE INTO users (username, password, email, is_admin) VALUES
('admin', 'admin123', 'admin@securecorp.com', TRUE),
('john', 'password123', 'john@securecorp.com', FALSE),
('jane', 'jane2023', 'jane@securecorp.com', FALSE),
('bob', 'bobsecure', 'bob@securecorp.com', FALSE),
('alice', 'alice456', 'alice@securecorp.com', FALSE),
('root', 'toor', 'root@securecorp.com', TRUE);

-- Create or update web_user
GRANT ALL PRIVILEGES ON vulnerable_db.* TO 'web_user'@'localhost' IDENTIFIED BY 'web_pass123';
FLUSH PRIVILEGES;