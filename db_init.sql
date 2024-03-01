CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender CHAR(1)
);

CREATE TABLE IF NOT EXISTS HealthRecords (
    RecordID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    RecordType VARCHAR(255) NOT NULL,
    RecordDate DATE NOT NULL,
    Description TEXT,
    ProviderName VARCHAR(255),
    Attachments TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS Medications (
    MedicationID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    MedicationName VARCHAR(255) NOT NULL,
    Dosage VARCHAR(255) NOT NULL,
    StartDate DATE,
    EndDate DATE,
    Reason TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS Allergies (
    AllergyID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    Allergen VARCHAR(255) NOT NULL,
    Reaction TEXT,
    Severity VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS EmergencyContacts (
    ContactID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    Relationship VARCHAR(255) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

INSERT IGNORE INTO Users (Username, PasswordHash, Email, FullName, DateOfBirth, Gender)
VALUES
('johndoe', 'e4r5t6y7u8i9o0p', 'john.doe@example.com', 'John Doe', '1985-01-01', 'M'),
('janedoe', 'u8y7t6r5e4w3q2', 'jane.doe@example.com', 'Jane Doe', '1990-02-02', 'F');

INSERT INTO HealthRecords (UserID, RecordType, RecordDate, Description, ProviderName)
VALUES
(1, 'Vaccination', '2020-03-01', 'COVID-19 vaccine, first dose', 'City Health Department'),
(2, 'Vaccination', '2020-03-15', 'COVID-19 vaccine, first dose', 'Local Clinic')

INSERT INTO Medications (UserID, MedicationName, Dosage, StartDate, EndDate, Reason)
VALUES
(1, 'Amoxicillin', '500mg three times a day', '2023-01-01', '2023-01-14', 'Bacterial Infection'),
(2, 'Ibuprofen', '200mg as needed', '2023-02-01', NULL, 'Pain relief');

INSERT INTO Allergies (UserID, Allergen, Reaction, Severity)
VALUES
(1, 'Peanuts', 'Hives, Swelling', 'High'),
(2, 'Penicillin', 'Rash', 'Medium');

INSERT INTO EmergencyContacts (UserID, FullName, Relationship, Phone, Email)
VALUES
(1, 'Emily Doe', 'Sister', '555-1234', 'emily.doe@example.com'),
(2, 'David Doe', 'Brother', '555-5678', 'david.doe@example.com');
