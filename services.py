"""
Services Module
Contains core business logic and operations for the Veterinary Clinic.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from database import Database
from queries import QueryManager


class VeterinaryClinicService:
    """Main service class for veterinary clinic operations."""
    
    def __init__(self, db: Database):
        """
        Initialize the service.
        
        Args:
            db: Database instance
        """
        self.db = db
        self.queries = QueryManager(db)
    
    # ==================== OWNER MANAGEMENT ====================
    
    def register_owner(self, name: str, billing_address: str, 
                       emergency_contact: str) -> Tuple[bool, Optional[int]]:
        """
        Register a new owner in the system.
        
        Args:
            name: Owner name
            billing_address: Billing address
            emergency_contact: Emergency contact number
        
        Returns:
            Tuple of (success, owner_id)
        """
        if not name or not billing_address or not emergency_contact:
            print("✗ All owner fields are required")
            return False, None
        
        owner_id = self.queries.create_owner(name, billing_address, emergency_contact)
        if owner_id:
            print(f"✓ Owner registered successfully (ID: {owner_id})")
            return True, owner_id
        else:
            print("✗ Failed to register owner")
            return False, None
    
    def get_owner_profile(self, owner_id: int) -> Optional[Dict]:
        """Get complete owner profile with their pets."""
        owner = self.queries.get_owner(owner_id)
        if not owner:
            return None
        
        pets = self.queries.get_pets_by_owner(owner_id)
        
        return {
            'owner': owner,
            'pets': pets,
            'pet_count': len(pets)
        }
    
    # ==================== PET MANAGEMENT ====================
    
    def register_pet(self, owner_id: int, name: str, species: str,
                    breed: str, age: int) -> Tuple[bool, Optional[int]]:
        """
        Register a new pet for an owner.
        
        Args:
            owner_id: Owner ID
            name: Pet name
            species: Species (e.g., Dog, Cat)
            breed: Breed
            age: Age in years
        
        Returns:
            Tuple of (success, pet_id)
        """
        if not all([name, species, breed, age]):
            print("✗ All pet fields are required")
            return False, None
        
        # Verify owner exists
        if not self.queries.get_owner(owner_id):
            print(f"✗ Owner with ID {owner_id} not found")
            return False, None
        
        pet_id = self.queries.create_pet(owner_id, name, species, breed, age)
        if pet_id:
            print(f"✓ Pet registered successfully (ID: {pet_id})")
            return True, pet_id
        else:
            print("✗ Failed to register pet")
            return False, None
    
    def get_pet_health_record(self, pet_id: int) -> Optional[Dict]:
        """Get comprehensive health record for a pet."""
        pet = self.queries.get_pet(pet_id)
        if not pet:
            return None
        
        visits = self.queries.get_visits_by_pet(pet_id)
        owner = self.queries.get_owner(pet.owner_id)
        
        return {
            'pet': pet,
            'owner': owner,
            'visits': visits,
            'visit_count': len(visits),
            'last_visit': visits[0] if visits else None
        }
    
    # ==================== VETERINARIAN MANAGEMENT ====================
    
    def register_veterinarian(self, name: str, expertise: str,
                             email: str, phone: str) -> Tuple[bool, Optional[int]]:
        """
        Register a new veterinarian.
        
        Args:
            name: Veterinarian name
            expertise: Area of expertise
            email: Email address
            phone: Phone number
        
        Returns:
            Tuple of (success, vet_id)
        """
        if not all([name, expertise, email, phone]):
            print("✗ All veterinarian fields are required")
            return False, None
        
        vet_id = self.queries.create_veterinarian(name, expertise, email, phone)
        if vet_id:
            print(f"✓ Veterinarian registered successfully (ID: {vet_id})")
            return True, vet_id
        else:
            print("✗ Failed to register veterinarian")
            return False, None
    
    def get_veterinarian_schedule(self, vet_id: int) -> Optional[Dict]:
        """Get veterinarian information and their recent visits."""
        vet = self.queries.get_veterinarian(vet_id)
        if not vet:
            return None
        
        query = """
            SELECT v.*, p.Name as PetName, o.Name as OwnerName
            FROM MedicalVisit v
            JOIN Pet p ON v.PetID = p.PetID
            JOIN Owner o ON v.OwnerID = o.OwnerID
            WHERE v.VetID = ?
            ORDER BY v.Date DESC
        """
        recent_visits = self.db.fetch_all(query, (vet_id,))
        
        return {
            'veterinarian': vet,
            'recent_visits': recent_visits,
            'total_visits': len(recent_visits)
        }
    
    # ==================== CLINIC MANAGEMENT ====================
    
    def register_clinic(self, name: str, location: str,
                       emergency_facilities: str) -> Tuple[bool, Optional[int]]:
        """
        Register a new clinic.
        
        Args:
            name: Clinic name
            location: Location address
            emergency_facilities: Emergency facilities description
        
        Returns:
            Tuple of (success, clinic_id)
        """
        if not all([name, location]):
            print("✗ Clinic name and location are required")
            return False, None
        
        clinic_id = self.queries.create_clinic(name, location, emergency_facilities or "None")
        if clinic_id:
            print(f"✓ Clinic registered successfully (ID: {clinic_id})")
            return True, clinic_id
        else:
            print("✗ Failed to register clinic")
            return False, None
    
    # ==================== MEDICAL VISITS ====================
    
    def record_medical_visit(self, pet_id: int, vet_id: int, clinic_id: int,
                            visit_date: str, weight: float, diagnosis: str,
                            clinical_notes: str) -> Tuple[bool, Optional[int]]:
        """
        Record a medical visit for a pet.
        
        Args:
            pet_id: Pet ID
            vet_id: Veterinarian ID
            clinic_id: Clinic ID
            visit_date: Visit date (YYYY-MM-DD)
            weight: Pet weight in kg
            diagnosis: Diagnosis
            clinical_notes: Clinical notes
        
        Returns:
            Tuple of (success, visit_id)
        """
        # Validate pet, vet, and clinic exist
        if not self.queries.get_pet(pet_id):
            print(f"✗ Pet with ID {pet_id} not found")
            return False, None
        
        if not self.queries.get_veterinarian(vet_id):
            print(f"✗ Veterinarian with ID {vet_id} not found")
            return False, None
        
        if not self.queries.get_clinic(clinic_id):
            print(f"✗ Clinic with ID {clinic_id} not found")
            return False, None
        
        # Validate date format
        try:
            datetime.strptime(visit_date, "%Y-%m-%d")
        except ValueError:
            print("✗ Invalid date format. Use YYYY-MM-DD")
            return False, None
        
        visit_id = self.queries.create_visit(
            pet_id, vet_id, clinic_id, visit_date, weight, diagnosis, clinical_notes
        )
        
        if visit_id:
            print(f"✓ Medical visit recorded successfully (ID: {visit_id})")
            return True, visit_id
        else:
            print("✗ Failed to record medical visit")
            return False, None
    
    def get_visit_details(self, visit_id: int) -> Optional[Dict]:
        """Get detailed information about a specific visit."""
        query = """
            SELECT v.*, p.Name as PetName, p.Species, p.Breed,
                   o.Name as OwnerName, o.EmergencyContact,
                   vet.Name as VetName, vet.Expertise,
                   c.Name as ClinicName, c.Location
            FROM MedicalVisit v
            JOIN Pet p ON v.PetID = p.PetID
            JOIN Owner o ON v.OwnerID = o.OwnerID
            JOIN Veterinarian vet ON v.VetID = vet.VetID
            JOIN Clinic c ON v.ClinicID = c.ClinicID
            WHERE v.VisitID = ?
        """
        return self.db.fetch_one(query, (visit_id,))
    
    # ==================== HEALTH MONITORING ====================
    
    def get_pets_needing_checkup(self, days_threshold: int = 90) -> List[Dict]:
        """
        Get pets that haven't had a checkup in the specified days.
        
        Args:
            days_threshold: Days since last visit (default 90)
        
        Returns:
            List of pets needing checkup
        """
        query = """
            SELECT p.PetID, p.Name, p.Species, p.Breed, 
                   o.Name as OwnerName, o.EmergencyContact,
                   MAX(v.Date) as LastVisitDate
            FROM Pet p
            JOIN Owner o ON p.OwnerID = o.OwnerID
            LEFT JOIN MedicalVisit v ON p.PetID = v.PetID
            GROUP BY p.PetID, p.Name, p.Species, p.Breed, o.Name, o.EmergencyContact
            HAVING MAX(v.Date) < DATEADD(day, -?, GETDATE()) 
               OR MAX(v.Date) IS NULL
            ORDER BY p.Name
        """
        return self.db.fetch_all(query, (days_threshold,))
    
    def get_pet_visit_history(self, pet_id: int, limit: int = 10) -> List[Dict]:
        """
        Get visit history for a pet.
        
        Args:
            pet_id: Pet ID
            limit: Maximum number of visits to retrieve
        
        Returns:
            List of visits
        """
        query = f"""
            SELECT TOP {limit} v.VisitID, v.Date, v.PetWeight, v.Diagnosis, v.ClinicalNote,
                   vet.Name as VetName, c.Name as ClinicName
            FROM MedicalVisit v
            JOIN Veterinarian vet ON v.VetID = vet.VetID
            JOIN Clinic c ON v.ClinicID = c.ClinicID
            WHERE v.PetID = ?
            ORDER BY v.Date DESC
        """
        return self.db.fetch_all(query, (pet_id,))
    
    # ==================== REPORTING ====================
    
    def get_clinic_statistics(self, clinic_id: int) -> Optional[Dict]:
        """Get statistics for a specific clinic."""
        stats = {}
        
        # Total visits
        total_visits = self.db.execute_scalar(
            "SELECT COUNT(*) FROM MedicalVisit WHERE ClinicID = ?",
            (clinic_id,)
        )
        
        # Total unique pets treated
        unique_pets = self.db.execute_scalar(
            """
            SELECT COUNT(DISTINCT PetID) 
            FROM MedicalVisit 
            WHERE ClinicID = ?
            """,
            (clinic_id,)
        )
        
        # Veterinarians working at clinic
        vets = self.db.fetch_all(
            """
            SELECT DISTINCT vet.VetID, vet.Name
            FROM MedicalVisit v
            JOIN Veterinarian vet ON v.VetID = vet.VetID
            WHERE v.ClinicID = ?
            """,
            (clinic_id,)
        )
        
        clinic = self.queries.get_clinic(clinic_id)
        
        return {
            'clinic': clinic,
            'total_visits': total_visits,
            'unique_pets_treated': unique_pets,
            'veterinarians': vets
        }
    
    def get_system_overview(self) -> Dict:
        """Get overall system statistics."""
        return {
            'total_owners': self.db.execute_scalar("SELECT COUNT(*) FROM Owner"),
            'total_pets': self.db.execute_scalar("SELECT COUNT(*) FROM Pet"),
            'total_veterinarians': self.db.execute_scalar("SELECT COUNT(*) FROM Veterinarian"),
            'total_clinics': self.db.execute_scalar("SELECT COUNT(*) FROM Clinic"),
            'total_visits': self.db.execute_scalar("SELECT COUNT(*) FROM MedicalVisit")
        }
    
    # ==================== DATA VALIDATION & UTILITIES ====================
    
    def search_owners(self, search_term: str) -> List[Dict]:
        """Search for owners by name or contact."""
        query = """
            SELECT * FROM Owner
            WHERE Name LIKE ? OR EmergencyContact LIKE ?
            ORDER BY Name
        """
        search_param = f"%{search_term}%"
        return self.db.fetch_all(query, (search_param, search_param))
    
    def search_pets(self, search_term: str) -> List[Dict]:
        """Search for pets by name."""
        query = """
            SELECT p.*, o.Name as OwnerName
            FROM Pet p
            JOIN Owner o ON p.OwnerID = o.OwnerID
            WHERE p.Name LIKE ? OR p.Breed LIKE ? OR p.Species LIKE ?
            ORDER BY p.Name
        """
        search_param = f"%{search_term}%"
        return self.db.fetch_all(query, (search_param, search_param, search_param))
    
    def validate_owner_exists(self, owner_id: int) -> bool:
        """Validate if owner exists."""
        return self.queries.get_owner(owner_id) is not None
    
    def validate_pet_exists(self, pet_id: int) -> bool:
        """Validate if pet exists."""
        return self.queries.get_pet(pet_id) is not None
    
    def validate_vet_exists(self, vet_id: int) -> bool:
        """Validate if veterinarian exists."""
        return self.queries.get_veterinarian(vet_id) is not None
    
    def validate_clinic_exists(self, clinic_id: int) -> bool:
        """Validate if clinic exists."""
        return self.queries.get_clinic(clinic_id) is not None
