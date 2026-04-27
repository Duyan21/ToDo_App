-- =========================
-- CREATE DATABASE
-- =========================
IF DB_ID('todo_app_db') IS NULL
BEGIN
    CREATE DATABASE todo_app_db;
END
GO

USE todo_app_db;
GO

-- =========================
-- DROP TABLES (nếu tồn tại)
-- =========================
IF OBJECT_ID('Notifications', 'U') IS NOT NULL DROP TABLE Notifications;
IF OBJECT_ID('Files', 'U') IS NOT NULL DROP TABLE Files;
IF OBJECT_ID('Tasks', 'U') IS NOT NULL DROP TABLE Tasks;
IF OBJECT_ID('Users', 'U') IS NOT NULL DROP TABLE Users;
GO

-- =========================
-- USERS
-- =========================
CREATE TABLE Users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    email NVARCHAR(100) NOT NULL UNIQUE,
    password_hash NVARCHAR(200) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- =========================
-- TASKS
-- =========================
CREATE TABLE Tasks (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    title NVARCHAR(200),
    description NVARCHAR(MAX),
    deadline DATETIME,
    priority NVARCHAR(20),
    status NVARCHAR(50),
    reminder_minutes INT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- =========================
-- NOTIFICATIONS
-- =========================
CREATE TABLE Notifications (
    id INT IDENTITY(1,1) PRIMARY KEY,
    task_id INT,
    user_id INT,
    message NVARCHAR(200),
    notify_time DATETIME,
    FOREIGN KEY (task_id) REFERENCES Tasks(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- =========================
-- FILES
-- =========================
CREATE TABLE Files (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    file_type NVARCHAR(50),
    created_at DATETIME DEFAULT GETDATE(),
    path NVARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
GO