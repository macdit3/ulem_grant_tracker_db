import unittest
import requests
import json
from datetime import datetime, date

# Base URL for the API
BASE_URL = "http://localhost:8000"  # Change this if your API is running on a different URL

class TestDonorManagementAPI(unittest.TestCase):
    """
    Test class for testing the Donor Management API endpoints
    """

    def setUp(self):
        """Set up test fixtures before each test method is run"""
        # Clear test data or create necessary fixtures
        self.donor_data = {
            "donor_type": "individual",
            "first_name": "John",
            "last_name": "Doe",
            "organization_name": None,
            "email": "john.doe@example.com",
            "phone": "555-123-4567",
            "address_line1": "123 Main St",
            "address_line2": "Apt 4B",
            "city": "Anytown",
            "state": "CA",
            "postal_code": "12345",
            "country": "USA",
            "preferred_contact_method": "email",
            "notes": "Test donor"
        }

        self.program_data = {
            "name": "Test Program",
            "description": "A program created for testing",
            "start_date": str(date.today()),
            "end_date": None,
            "budget": 10000.0,
            "goal_amount": 15000.0,
            "current_progress": 0.0
        }

        # IDs to store created resources for later tests
        self.donor_id = None
        self.program_id = None
        self.donation_id = None
        self.pledge_id = None
        self.tax_receipt_id = None
        self.thank_you_note_id = None

    def tearDown(self):
        """Clean up after each test method is run"""
        # Delete test data if needed
        try:
            if self.thank_you_note_id:
                requests.delete(f"{BASE_URL}/thank_you_notes/{self.thank_you_note_id}")

            if self.tax_receipt_id:
                requests.delete(f"{BASE_URL}/tax_receipts/{self.tax_receipt_id}")

            if self.donation_id:
                requests.delete(f"{BASE_URL}/donations/{self.donation_id}")

            if self.pledge_id:
                requests.delete(f"{BASE_URL}/pledges/{self.pledge_id}")

            if self.program_id:
                requests.delete(f"{BASE_URL}/programs/{self.program_id}")

            if self.donor_id:
                requests.delete(f"{BASE_URL}/donors/{self.donor_id}")
        except Exception as e:
            print(f"Error in teardown: {e}")

    # -------------------- Donor Tests --------------------

    def test_donor_crud(self):
        """Test create, read, update, delete operations for donors"""
        # Create a donor
        response = requests.post(f"{BASE_URL}/donors/", json=self.donor_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.donor_id = data["id"]
        self.assertIsNotNone(self.donor_id)

        # Read the donor
        response = requests.get(f"{BASE_URL}/donors/{self.donor_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], "John")

        # Update the donor
        update_data = self.donor_data.copy()
        update_data["first_name"] = "Jane"
        response = requests.put(f"{BASE_URL}/donors/{self.donor_id}", json=update_data)
        self.assertEqual(response.status_code, 200)

        # Verify update
        response = requests.get(f"{BASE_URL}/donors/{self.donor_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], "Jane")

        # Delete the donor
        response = requests.delete(f"{BASE_URL}/donors/{self.donor_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/donors/{self.donor_id}")
        self.assertEqual(response.status_code, 404)

        # Reset donor_id since we've deleted it
        self.donor_id = None

    def test_read_donors(self):
        """Test reading all donors"""
        # Create a donor first
        response = requests.post(f"{BASE_URL}/donors/", json=self.donor_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.donor_id = data["id"]

        # Get all donors
        response = requests.get(f"{BASE_URL}/donors/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

        # Test with skip and limit parameters
        response = requests.get(f"{BASE_URL}/donors/?skip=0&limit=10")
        self.assertEqual(response.status_code, 200)

    # -------------------- Program Tests --------------------

    def test_program_crud(self):
        """Test create, read, update, delete operations for programs"""
        # Create a program
        response = requests.post(f"{BASE_URL}/programs/", json=self.program_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.program_id = data["id"]
        self.assertIsNotNone(self.program_id)

        # Read the program
        response = requests.get(f"{BASE_URL}/programs/{self.program_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Program")

        # Update the program
        update_data = self.program_data.copy()
        update_data["name"] = "Updated Test Program"
        response = requests.put(f"{BASE_URL}/programs/{self.program_id}", json=update_data)
        self.assertEqual(response.status_code, 200)

        # Verify update
        response = requests.get(f"{BASE_URL}/programs/{self.program_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Updated Test Program")

        # Delete the program
        response = requests.delete(f"{BASE_URL}/programs/{self.program_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/programs/{self.program_id}")
        self.assertEqual(response.status_code, 404)

        # Reset program_id since we've deleted it
        self.program_id = None

    # -------------------- Donation Tests --------------------

    def test_donation_crud(self):
        """Test create, read, update, delete operations for donations"""
        # Create donor and program first
        response = requests.post(f"{BASE_URL}/donors/", json=self.donor_data)
        self.assertEqual(response.status_code, 200)
        self.donor_id = response.json()["id"]

        response = requests.post(f"{BASE_URL}/programs/", json=self.program_data)
        self.assertEqual(response.status_code, 200)
        self.program_id = response.json()["id"]

        # Create a donation
        donation_data = {
            "donor_id": self.donor_id,
            "program_id": self.program_id,
            "amount": 500.0,
            "donation_date": str(date.today()),
            "payment_method": "credit_card",
            "transaction_id": "TX123456",
            "is_tax_deductible": True,
            "notes": "Test donation"
        }

        response = requests.post(f"{BASE_URL}/donations/", json=donation_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.donation_id = data["id"]
        self.assertIsNotNone(self.donation_id)

        # Read the donation
        response = requests.get(f"{BASE_URL}/donations/{self.donation_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["amount"], 500.0)

        # Update the donation
        update_data = donation_data.copy()
        update_data["amount"] = 750.0
        response = requests.put(f"{BASE_URL}/donations/{self.donation_id}", json=update_data)
        self.assertEqual(response.status_code, 200)

        # Verify update
        response = requests.get(f"{BASE_URL}/donations/{self.donation_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["amount"], 750.0)

        # Delete the donation
        response = requests.delete(f"{BASE_URL}/donations/{self.donation_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/donations/{self.donation_id}")
        self.assertEqual(response.status_code, 404)

        # Reset donation_id since we've deleted it
        self.donation_id = None

    # -------------------- Pledge Tests --------------------

    def test_pledge_crud(self):
        """Test create, read, update, delete operations for pledges"""
        # Create donor and program first
        response = requests.post(f"{BASE_URL}/donors/", json=self.donor_data)
        self.assertEqual(response.status_code, 200)
        self.donor_id = response.json()["id"]

        response = requests.post(f"{BASE_URL}/programs/", json=self.program_data)
        self.assertEqual(response.status_code, 200)
        self.program_id = response.json()["id"]

        # Create a pledge
        pledge_data = {
            "donor_id": self.donor_id,
            "program_id": self.program_id,
            "amount": 1000.0,
            "pledge_date": str(date.today()),
            "fulfillment_date": None,
            "status": "pending",
            "amount_fulfilled": 0.0,
            "notes": "Test pledge"
        }

        response = requests.post(f"{BASE_URL}/pledges/", json=pledge_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.pledge_id = data["id"]
        self.assertIsNotNone(self.pledge_id)

        # Read the pledge
        response = requests.get(f"{BASE_URL}/pledges/{self.pledge_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["amount"], 1000.0)

        # Update the pledge
        update_data = pledge_data.copy()
        update_data["status"] = "fulfilled"
        update_data["amount_fulfilled"] = 1000.0
        update_data["fulfillment_date"] = str(date.today())
        response = requests.put(f"{BASE_URL}/pledges/{self.pledge_id}", json=update_data)
        self.assertEqual(response.status_code, 200)

        # Verify update
        response = requests.get(f"{BASE_URL}/pledges/{self.pledge_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "fulfilled")

        # Delete the pledge
        response = requests.delete(f"{BASE_URL}/pledges/{self.pledge_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/pledges/{self.pledge_id}")
        self.assertEqual(response.status_code, 404)

        # Reset pledge_id since we've deleted it
        self.pledge_id = None

    # -------------------- Special Endpoint Tests --------------------

    def test_donations_by_program(self):
        """Test getting donations by program"""
        # Create necessary test data
        response = requests.post(f"{BASE_URL}/donors/", json=self.donor_data)
        self.assertEqual(response.status_code, 200)
        self.donor_id = response.json()["id"]

        response = requests.post(f"{BASE_URL}/programs/", json=self.program_data)
        self.assertEqual(response.status_code, 200)
        self.program_id = response.json()["id"]

        # Create a donation
        donation_data = {
            "donor_id": self.donor_id,
            "program_id": self.program_id,
            "amount": 500.0,
            "donation_date": str(date.today()),
            "payment_method": "credit_card",
            "transaction_id": "TX123456",
            "is_tax_deductible": True,
            "notes": "Test donation"
        }

        response = requests.post(f"{BASE_URL}/donations/", json=donation_data)
        self.assertEqual(response.status_code, 200)
        self.donation_id = response.json()["id"]

        # Test the endpoint
        response = requests.get(f"{BASE_URL}/programs/{self.program_id}/donations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_unfulfilled_pledges(self):
        """Test getting unfulfilled pledges"""
        # Create necessary test data
        response = requests.post(f"{BASE_URL}/donors/", json=self.donor_data)
        self.assertEqual(response.status_code, 200)
        self.donor_id = response.json()["id"]

        response = requests.post(f"{BASE_URL}/programs/", json=self.program_data)
        self.assertEqual(response.status_code, 200)
        self.program_id = response.json()["id"]

        # Create a pledge
        pledge_data = {
            "donor_id": self.donor_id,
            "program_id": self.program_id,
            "amount": 1000.0,
            "pledge_date": str(date.today()),
            "fulfillment_date": None,
            "status": "pending",
            "amount_fulfilled": 0.0,
            "notes": "Test pledge"
        }

        response = requests.post(f"{BASE_URL}/pledges/", json=pledge_data)
        self.assertEqual(response.status_code, 200)
        self.pledge_id = response.json()["id"]

        # Test the endpoint
        response = requests.get(f"{BASE_URL}/pledges/unfulfilled")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_tax_receipt_generation(self):
        """Test generating tax receipts for a year"""
        # Create necessary test data
        response = requests.post(f"{BASE_URL}/donors/", json=self.donor_data)
        self.assertEqual(response.status_code, 200)
        self.donor_id = response.json()["id"]

        response = requests.post(f"{BASE_URL}/programs/", json=self.program_data)
        self.assertEqual(response.status_code, 200)
        self.program_id = response.json()["id"]

        # Create a donation
        donation_data = {
            "donor_id": self.donor_id,
            "program_id": self.program_id,
            "amount": 500.0,
            "donation_date": str(date.today()),
            "payment_method": "credit_card",
            "transaction_id": "TX123456",
            "is_tax_deductible": True,
            "notes": "Test donation"
        }

        response = requests.post(f"{BASE_URL}/donations/", json=donation_data)
        self.assertEqual(response.status_code, 200)
        self.donation_id = response.json()["id"]

        # Test the endpoint
        current_year = datetime.now().year
        response = requests.post(f"{BASE_URL}/tax_receipts/generate/{current_year}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()