create table Owner
(
 OwnerID INT IDENTITY(1,1) PRIMARY KEY,
 Name VARCHAR(100) NOT NULL,
 EmergencyContact VARCHAR(50) NOT NULL,
 BillingAddress VARCHAR(255) NOT NULL
);

CREATE TABLE CLINIC
(
 ClinicID INT IDENTITY(1,1) PRIMARY KEY,
 Name VARCHAR(100) NOT NULL,
 Location VARCHAR(255) NOT NULL,
 EmergencyFacilities VARCHAR(255)
);
create table Veterinarian
(
 VetID INT IDENTITY(1,1) PRIMARY KEY,
 Name VARCHAR(100) NOT NULL,
 Email VARCHAR(100),
 Phone VARCHAR(20),
 Expertise VARCHAR(100) NOT NULL
);
create table Pet
(
 PetID INT IDENTITY(1,1) PRIMARY KEY,
 Age INT,
 Breed varchar(50),
 Name varchar(100) NOT NULL,
 Species varchar(100) NOT NULL,
 OwnerID INT NOT NULL,
 CONSTRAINT FK_PET_OWNER FOREIGN KEY (OwnerID) REFERENCES  Owner(OwnerID)
);
create table Clinic_Veterinarian
(
 ClinicID INT NOT NULL,
 VetID INT NOT NULL,
 PRIMARY KEY(ClinicID,VetID),
 CONSTRAINT FK_CV_CLINIC FOREIGN KEY (ClinicID) REFERENCES CLINIC(ClinicID),
 CONSTRAINT FK_CV_Veterinarian FOREIGN KEY (VetID) REFERENCES Veterinarian(VetID)
);
CREATE TABLE MedicalVisit 
(
    VisitID INT IDENTITY(1,1) PRIMARY KEY,
    Date DATETIME NOT NULL,
    ClinicalNote VARCHAR(MAX),
    Diagnosis VARCHAR(255),
    PetWeight DECIMAL(5,2),
    OwnerID INT NOT NULL,
    PetID INT NOT NULL,
    ClinicID INT NOT NULL,
    VetID INT NOT NULL,
    CONSTRAINT FK_Visit_Owner FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID),
    CONSTRAINT FK_Visit_Pet FOREIGN KEY (PetID) REFERENCES Pet(PetID),
    CONSTRAINT FK_Visit_Clinic FOREIGN KEY (ClinicID) REFERENCES Clinic(ClinicID),
    CONSTRAINT FK_Visit_Vet FOREIGN KEY (VetID) REFERENCES Veterinarian(VetID)
);
CREATE TABLE VaccinationRecord 
(
    VaccinationID INT IDENTITY(1,1) PRIMARY KEY,
    VaccineType VARCHAR(100) NOT NULL,
    BatchNumber VARCHAR(50) NOT NULL,
    DateAdministered DATE NOT NULL,
    NextBoosterDate DATE,
    VisitID INT NOT NULL,
    CONSTRAINT FK_Vaccination_Visit FOREIGN KEY (VisitID) REFERENCES MedicalVisit(VisitID)
);

CREATE TABLE VaccineReminder
(
    ReminderID INT IDENTITY(1,1) PRIMARY KEY,
    VaccinationID INT NOT NULL,
    OwnerID INT NOT NULL,
    ReminderDate DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'pending',
    CONSTRAINT FK_Reminder_Vaccination FOREIGN KEY (VaccinationID) REFERENCES VaccinationRecord(VaccinationID),
    CONSTRAINT FK_Reminder_Owner FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID)
);

CREATE TABLE VaccineInventory
(
    InventoryID INT IDENTITY(1,1) PRIMARY KEY,
    ClinicID INT NOT NULL,
    VaccineType VARCHAR(100) NOT NULL,
    StockLevel INT NOT NULL DEFAULT 0,
    ExpirationDate DATE,
    CONSTRAINT FK_Inventory_Clinic FOREIGN KEY (ClinicID) REFERENCES Clinic(ClinicID)
);
