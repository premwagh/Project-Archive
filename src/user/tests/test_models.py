from django.test import TestCase
from user.models import User, PrimaryPhoneDevice

class UserTest(TestCase):
    """
    Test Cases for User Model.
    """
    def setUp(self):
        """
        Create User for every TestCase.
        """
        self.first_name = 'test'
        self.email = 'test@gmail.com'
        self.phone = '+919988776655'
        self.usr = User.objects.create(
            first_name = self.first_name,
            email = self.email,
            phone_number = self.phone
        )

    def tearDown(self):
        """
        Delete all User after execution of TestCases.
        """
        User.objects.all().delete()

    def test_user_creation(self):
        """
        Test case for creation of User model.
        """
        self.assertTrue(isinstance(self.usr, User))
        self.assertEqual(self.usr.__str__(),self.email)
        self.assertIsNotNone(self.usr)
        self.assertTrue(self.usr.phone_number.national_number, "9988776655")
        self.assertEqual(User.objects.get(first_name=self.first_name).email, self.email)
