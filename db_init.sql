CREATE TABLE IF NOT EXISTS Roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(255) UNIQUE NOT NULL,
    PermissionLevel INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender CHAR(1),
    Active TINYINT DEFAULT 0,
    RoleID INT NOT NULL DEFAULT 1,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

CREATE TABLE IF NOT EXISTS Healthrecords (
    ID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    RecordType VARCHAR(255) NOT NULL,
    RecordDate DATE NOT NULL,
    Description TEXT,
    ProviderName VARCHAR(255),
    Attachments TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS Medications (
    ID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    MedicationName VARCHAR(255) NOT NULL,
    Dosage VARCHAR(255) NOT NULL,
    StartDate DATE,
    EndDate DATE,
    Reason TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS Allergies (
    ID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    Allergen VARCHAR(255) NOT NULL,
    Reaction TEXT,
    Severity VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS Emergencycontacts (
    ID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    Relationship VARCHAR(255) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);


INSERT IGNORE INTO Roles (RoleName, PermissionLevel )
VALUES
('USER', 1),
('ADMIN', 5);

INSERT IGNORE INTO Users (Username, PasswordHash, Email, FullName, DateOfBirth, Gender, Active, RoleID)
VALUES
('johndoe', 'e4r5t6y7u8i9o0p', 'john.doe@example.com', 'John Doe', '1985-01-01', 'M', 1, 1),
('janedoe', 'u8y7t6r5e4w3q2', 'jane.doe@example.com', 'Jane Doe', '1990-02-02', 'F', 1, 1);