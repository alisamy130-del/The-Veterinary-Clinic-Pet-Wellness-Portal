"""
Queries Module
Contains all database CRUD operations and data retrieval queries.
"""

from typing import List, Dict, Optional, Any
from database import Database
from models import (
    Owner, Pet, Clinic, Veterinarian, VetSpecialty, 
    Visit, ClinicalNote, Vaccination, Reminder
)


class QueryManager:
    """Manages all database queries and CRUD operations."""
    
    def __init__(self, db: Database):
        """
        Initialize QueryManager with database connection.
        
        Args:
            db: Database instance
        """
        self.db = db
    
    # ==================== OWNER QUERIES ====================
    
    def create_owner(self, name: str, billing_address: str, emergency_contact: str) -> Optional[int]:
        """
        Create a new owner.
        
        Args:
            name: Owner name
            billing_address: Billing address
            emergency_contact: Emergency contact number
        
        Returns:
            Owner ID if successful, None otherwise
        """
        query = """
            INSERT INTO Owner (Name, BillingAddress, EmergencyContact)
            VALUES (?, ?, ?)
        """
        if self.db.execute_query(query, (name, billing_address, emergency_contact)):
            # Retrieve the inserted ID
            owner_id = self.db.execute_scalar(
                "SELECT MAX(OwnerID) FROM Owner"
            )
            return owner_id
        return None
    
    def get_owner(self, owner_id: int) -> Optional[Owner]:
        """Get owner by ID."""
        query = "SELECT * FROM Owner WHERE OwnerID = ?"
        result = self.db.fetch_one(query, (owner_id,))
        if result:
            return Owner(
                owner_id=result['OwnerID'],
                name=result.get('Name', 'Unknown'),
                billing_address=result['BillingAddress'],
                emergency_contact=result['EmergencyContact']
            )
        return None
    
    def get_all_owners(self) -> List[Owner]:
        """Get all owners."""
        query = "SELECT * FROM Owner ORDER BY OwnerID"
        results = self.db.fetch_all(query)
        return [
            Owner(
                owner_id=r['OwnerID'],
                name=r.get('Name', 'Unknown'),
                billing_address=r['BillingAddress'],
                emergency_contact=r['EmergencyContact']
            )
            for r in results
        ]
    
    def update_owner(self, owner_id: int, name: str = None, 
                     billing_address: str = None, emergency_contact: str = None) -> bool:
        """Update owner information."""
        updates = []
        params = []
        
        if name:
            updates.append("Name = ?")
            params.append(name)
        if billing_address:
            updates.append("BillingAddress = ?")
            params.append(billing_address)
        if emergency_contact:
            updates.append("EmergencyContact = ?")
            params.append(emergency_contact)
        
        if not updates:
            return False
        
        params.append(owner_id)
        query = f"UPDATE Owner SET {', '.join(updates)} WHERE OwnerID = ?"
        return self.db.execute_query(query, tuple(params))
    
    def delete_owner(self, owner_id: int) -> bool:
        """Delete owner by ID."""
        query = "DELETE FROM Owner WHERE OwnerID = ?"
        return self.db.execute_query(query, (owner_id,))
    
    # ==================== PET QUERIES ====================
    
    def create_pet(self, owner_id: int, name: str, species: str, 
                   breed: str, age: int) -> Optional[int]:
        """Create a new pet."""
        query = """
            INSERT INTO Pet (OwnerID, Name, Species, Breed, Age)
            VALUES (?, ?, ?, ?, ?)
        """
        if self.db.execute_query(query, (owner_id, name, species, breed, age)):
            pet_id = self.db.execute_scalar("SELECT MAX(PetID) FROM Pet")
            return pet_id
        return None
    
    def get_pet(self, pet_id: int) -> Optional[Pet]:
        """Get pet by ID."""
        query = "SELECT * FROM Pet WHERE PetID = ?"
        result = self.db.fetch_one(query, (pet_id,))
        if result:
            return Pet(
                pet_id=result['PetID'],
                owner_id=result['OwnerID'],
                name=result['Name'],
                species=result['Species'],
                breed=result['Breed'],
                age=result['Age']
            )
        return None
    
    def get_pets_by_owner(self, owner_id: int) -> List[Pet]:
        """Get all pets for a specific owner."""
        query = "SELECT * FROM Pet WHERE OwnerID = ? ORDER BY PetID"
        results = self.db.fetch_all(query, (owner_id,))
        return [
            Pet(
                pet_id=r['PetID'],
                owner_id=r['OwnerID'],
                name=r['Name'],
                species=r['Species'],
                breed=r['Breed'],
                age=r['Age']
            )
            for r in results
        ]
    
    def get_all_pets(self) -> List[Pet]:
        """Get all pets."""
        query = "SELECT * FROM Pet ORDER BY PetID"
        results = self.db.fetch_all(query)
        return [
            Pet(
                pet_id=r['PetID'],
                owner_id=r['OwnerID'],
                name=r['Name'],
                species=r['Species'],
                breed=r['Breed'],
                age=r['Age']
            )
            for r in results
        ]
    
    def update_pet(self, pet_id: int, name: str = None, species: str = None,
                   breed: str = None, age: int = None) -> bool:
        """Update pet information."""
        updates = []
        params = []
        
        if name:
            updates.append("Name = ?")
            params.append(name)
        if species:
            updates.append("Species = ?")
            params.append(species)
        if breed:
            updates.append("Breed = ?")
            params.append(breed)
        if age is not None:
            updates.append("Age = ?")
            params.append(age)
        
        if not updates:
            return False
        
        params.append(pet_id)
        query = f"UPDATE Pet SET {', '.join(updates)} WHERE PetID = ?"
        return self.db.execute_query(query, tuple(params))
    
    def delete_pet(self, pet_id: int) -> bool:
        """Delete pet by ID."""
        query = "DELETE FROM Pet WHERE PetID = ?"
        return self.db.execute_query(query, (pet_id,))
    
    # ==================== VETERINARIAN QUERIES ====================
    
    def create_veterinarian(self, name: str, expertise: str, 
                           email: str, phone: str) -> Optional[int]:
        """Create a new veterinarian."""
        query = """
            INSERT INTO Veterinarian (Name, Expertise, Email, Phone)
            VALUES (?, ?, ?, ?)
        """
        if self.db.execute_query(query, (name, expertise, email, phone)):
            vet_id = self.db.execute_scalar("SELECT MAX(VetID) FROM Veterinarian")
            return vet_id
        return None
    
    def get_veterinarian(self, vet_id: int) -> Optional[Veterinarian]:
        """Get veterinarian by ID."""
        query = "SELECT * FROM Veterinarian WHERE VetID = ?"
        result = self.db.fetch_one(query, (vet_id,))
        if result:
            return Veterinarian(
                vet_id=result['VetID'],
                name=result.get('Name', 'Unknown'),
                email=result.get('Email', 'N/A'),
                phone=result.get('Phone', 'N/A')
            )
        return None
    
    def get_all_veterinarians(self) -> List[Veterinarian]:
        """Get all veterinarians."""
        query = "SELECT * FROM Veterinarian ORDER BY VetID"
        results = self.db.fetch_all(query)
        return [
            Veterinarian(
                vet_id=r['VetID'],
                name=r.get('Name', 'Unknown'),
                email=r.get('Email', 'N/A'),
                phone=r.get('Phone', 'N/A')
            )
            for r in results
        ]
    
    def update_veterinarian(self, vet_id: int, name: str = None,
                           expertise: str = None, email: str = None,
                           phone: str = None) -> bool:
        """Update veterinarian information."""
        updates = []
        params = []
        
        if name:
            updates.append("Name = ?")
            params.append(name)
        if expertise:
            updates.append("Expertise = ?")
            params.append(expertise)
        if email:
            updates.append("Email = ?")
            params.append(email)
        if phone:
            updates.append("Phone = ?")
            params.append(phone)
        
        if not updates:
            return False
        
        params.append(vet_id)
        query = f"UPDATE Veterinarian SET {', '.join(updates)} WHERE VetID = ?"
        return self.db.execute_query(query, tuple(params))
    
    def delete_veterinarian(self, vet_id: int) -> bool:
        """Delete veterinarian by ID."""
        query = "DELETE FROM Veterinarian WHERE VetID = ?"
        return self.db.execute_query(query, (vet_id,))
    
    # ==================== CLINIC QUERIES ====================
    
    def create_clinic(self, name: str, location: str, 
                     emergency_facilities: str) -> Optional[int]:
        """Create a new clinic."""
        query = """
            INSERT INTO Clinic (Name, Location, EmergencyFacilities)
            VALUES (?, ?, ?)
        """
        if self.db.execute_query(query, (name, location, emergency_facilities)):
            clinic_id = self.db.execute_scalar("SELECT MAX(ClinicID) FROM Clinic")
            return clinic_id
        return None
    
    def get_clinic(self, clinic_id: int) -> Optional[Clinic]:
        """Get clinic by ID."""
        query = "SELECT * FROM Clinic WHERE ClinicID = ?"
        result = self.db.fetch_one(query, (clinic_id,))
        if result:
            return Clinic(
                clinic_id=result['ClinicID'],
                name=result.get('Name', 'Unknown'),
                location=result['Location'],
                emergency_facilities=result.get('EmergencyFacilities', 'N/A')
            )
        return None
    
    def get_all_clinics(self) -> List[Clinic]:
        """Get all clinics."""
        query = "SELECT * FROM Clinic ORDER BY ClinicID"
        results = self.db.fetch_all(query)
        return [
            Clinic(
                clinic_id=r['ClinicID'],
                name=r.get('Name', 'Unknown'),
                location=r['Location'],
                emergency_facilities=r.get('EmergencyFacilities', 'N/A')
            )
            for r in results
        ]
    
    def delete_clinic(self, clinic_id: int) -> bool:
        """Delete clinic by ID."""
        query = "DELETE FROM Clinic WHERE ClinicID = ?"
        return self.db.execute_query(query, (clinic_id,))
    
    # ==================== VISIT QUERIES ====================
    
    def create_visit(self, pet_id: int, vet_id: int, clinic_id: int,
                     visit_date: str, weight: float, diagnosis: str,
                     clinical_notes: str) -> Optional[int]:
        """
        Create a new medical visit.
        
        Args:
            pet_id: Pet ID
            vet_id: Veterinarian ID
            clinic_id: Clinic ID
            visit_date: Visit date (YYYY-MM-DD format)
            weight: Pet weight in kg
            diagnosis: Diagnosis
            clinical_notes: Clinical notes
        
        Returns:
            Visit ID if successful, None otherwise
        """
        query = """
            INSERT INTO MedicalVisit (PetID, VetID, ClinicID, Date, 
                                     PetWeight, Diagnosis, ClinicalNote, OwnerID)
            VALUES (?, ?, ?, ?, ?, ?, ?, 
                   (SELECT OwnerID FROM Pet WHERE PetID = ?))
        """
        if self.db.execute_query(
            query, 
            (pet_id, vet_id, clinic_id, visit_date, weight, diagnosis, clinical_notes, pet_id)
        ):
            visit_id = self.db.execute_scalar("SELECT MAX(VisitID) FROM MedicalVisit")
            return visit_id
        return None
    
    def get_visit(self, visit_id: int) -> Optional[Visit]:
        """Get visit by ID."""
        query = "SELECT * FROM MedicalVisit WHERE VisitID = ?"
        result = self.db.fetch_one(query, (visit_id,))
        if result:
            return Visit(
                visit_id=result['VisitID'],
                pet_id=result['PetID'],
                vet_id=result['VetID'],
                clinic_id=result['ClinicID'],
                visit_date=result['Date']
            )
        return None
    
    def get_visits_by_pet(self, pet_id: int) -> List[Visit]:
        """Get all visits for a specific pet."""
        query = "SELECT * FROM MedicalVisit WHERE PetID = ? ORDER BY Date DESC"
        results = self.db.fetch_all(query, (pet_id,))
        return [
            Visit(
                visit_id=r['VisitID'],
                pet_id=r['PetID'],
                vet_id=r['VetID'],
                clinic_id=r['ClinicID'],
                visit_date=r['Date']
            )
            for r in results
        ]
    
    def get_all_visits(self) -> List[Dict[str, Any]]:
        """Get all visits with full details."""
        query = """
            SELECT v.VisitID, v.Date, v.PetWeight, v.Diagnosis, v.ClinicalNote,
                   p.Name as PetName, o.Name as OwnerName, 
                   vet.Name as VetName, c.Name as ClinicName
            FROM MedicalVisit v
            JOIN Pet p ON v.PetID = p.PetID
            JOIN Owner o ON v.OwnerID = o.OwnerID
            JOIN Veterinarian vet ON v.VetID = vet.VetID
            JOIN Clinic c ON v.ClinicID = c.ClinicID
            ORDER BY v.Date DESC
        """
        return self.db.fetch_all(query)
    
    def delete_visit(self, visit_id: int) -> bool:
        """Delete visit by ID."""
        query = "DELETE FROM MedicalVisit WHERE VisitID = ?"
        return self.db.execute_query(query, (visit_id,))
