
CREATE DATABASE IF NOT EXISTS transaction_db;
USE transaction_db;

CREATE TABLE IF NOT EXISTS users (
    userID              INT AUTO_INCREMENT PRIMARY KEY,
    username            VARCHAR(255) UNIQUE NOT NULL,
    hashed_password     VARCHAR(255) NOT NULL,
    email_address       VARCHAR(255) NOT NULL,
    enc_data_key        BLOB NOT NULL,
    enc_data_key_server BLOB NOT NULL,
    salt                BLOB NOT NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    accountID        INT AUTO_INCREMENT PRIMARY KEY,
    userID           INT NOT NULL,
    account_name     VARCHAR(255) NOT NULL,
    account_type     ENUM('Cash', 'Bank', 'Credit Card', 'Investment', 'Other') NOT NULL,
    account_currency VARCHAR(3) NOT NULL DEFAULT 'GBP',
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME NULL DEFAULT NULL,
    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
    INDEX user_type_index (userID, account_type)
);

CREATE TABLE IF NOT EXISTS categories (
    categoryID        INT AUTO_INCREMENT PRIMARY KEY,
    userID            INT NOT NULL,
    accountID         INT NOT NULL,
    category_sentence VARCHAR(255) NOT NULL,
    category_list     JSON,
    category_name     VARCHAR(255) NOT NULL,
    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
    FOREIGN KEY (accountID) REFERENCES accounts(accountID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS files (
    file_ID     INT AUTO_INCREMENT PRIMARY KEY,
    accountID   INT NOT NULL,
    file_name   VARCHAR(255) NOT NULL,
    hashed_name VARCHAR(255) NOT NULL,
    file_size   INT NOT NULL,
    file_type   VARCHAR(255) NOT NULL,
    added_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (accountID) REFERENCES accounts(accountID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions (
    transactionID    INT AUTO_INCREMENT PRIMARY KEY,
    accountID        INT NOT NULL,
    file_ID          INT,
    transaction_date DATETIME,
    transaction_type VARCHAR(255) NOT NULL,
    description      VARCHAR(255),
    category         VARCHAR(255),
    amount           DECIMAL(20, 6),
    balance          DECIMAL(20, 6),
    FOREIGN KEY (accountID) REFERENCES accounts(accountID) ON DELETE CASCADE,
    FOREIGN KEY (file_ID) REFERENCES files(file_ID) ON DELETE CASCADE,
    INDEX date_account_index (transaction_date, accountID),
    INDEX account_index (accountID),
    FULLTEXT (description),
    CONSTRAINT different_transactions UNIQUE (accountID, transaction_date, description, amount, balance)
);