from rest_framework.test import APITestCase
from Institutions.models import Institution
class InstitutionTests(APITestCase):
    #check if you can create the institutions
    def test_create_institution(self):
        institution = Institution.objects.create(
            name="Utumishi Girls Academy",
            subcounty="gilgil",
            county="nakuru",
            category="national",
            institutionType="boarding",
            studentGender="girls",
            is_sne=True
        )
        self.assertIsInstance(institution,Institution)
        self.assertEqual(institution.name,"Utumishi Girls Academy")