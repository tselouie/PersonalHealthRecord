INSERT INTO Healthrecords (UserID, RecordType, RecordDate, Description, ProviderName)
VALUES
(1, 'Vaccination', '2020-03-01', 'COVID-19 vaccine, first dose', 'City Health Department'),
(2, 'Vaccination', '2020-03-15', 'COVID-19 vaccine, first dose', 'Local Clinic');

INSERT INTO Medications (UserID, MedicationName, Dosage, StartDate, EndDate, Reason)
VALUES
(1, 'Amoxicillin', '500mg three times a day', '2023-01-01', '2023-01-14', 'Bacterial Infection'),
(2, 'Ibuprofen', '200mg as needed', '2023-02-01', '2024-02-01', 'Pain relief');

INSERT INTO Allergies (UserID, Allergen, Reaction, Severity)
VALUES
(1, 'Peanuts', 'Hives, Swelling', 'High'),
(2, 'Penicillin', 'Rash', 'Medium');

INSERT INTO Emergencycontacts (UserID, FullName, Relationship, Phone, Email)
VALUES
(1, 'Emily Doe', 'Sister', '555-1234', 'emily.doe@example.com'),
(2, 'David Doe', 'Brother', '555-5678', 'david.doe@example.com');