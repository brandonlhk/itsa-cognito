CREATE DATABASE IF NOT EXISTS itsa;
USE itsa;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(191) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    role ENUM('ADMIN', 'AGENT') NOT NULL DEFAULT 'AGENT',
    password VARCHAR(255) NOT NULL,
    disabled BOOLEAN NOT NULL DEFAULT FALSE,
    is_root BOOLEAN NOT NULL DEFAULT FALSE
);

-- root admin
INSERT INTO users (email, full_name, role, password, disabled, is_root)
SELECT 'admin@scrooge-bank.com',
       'root-admin',
       'ADMIN',
       '$2b$12$RBXgAkqc8UBpYg0EH6o.yeHibZNmnA2iVmEb9gEp1COXjZnYMnqLy',
       FALSE,
       TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@scrooge-bank.com'
);