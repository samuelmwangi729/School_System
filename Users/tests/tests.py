from rest_framework.test import APITestCase
from Institutions.models import Institution
from Users.models import User

class UserTests(APITestCase):

    def setUp(self):
        print("creating the setup")
        # Create the institution before each test
        self.userInstitution = Institution.objects.create(
            name="Utumishi Girls Academy",
            subcounty="gilgil",
            county="nakuru",
            category="national",
            institutionType="boarding",
            studentGender="girls",
            is_sne=True
        )

    def test_create_user_successfully(self):
        user = User.objects.create_user(
            username="samuel123",
            first_name="Samuel",
            email="samuel@example.com",
            password="securepassword123",
            institution=self.userInstitution  # Pass the actual object, not .id
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, "Samuel")
        self.assertEqual(user.institution, self.userInstitution)
