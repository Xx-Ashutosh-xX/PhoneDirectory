from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Provides methods for creating users.
    """
    def create_user(self, name, phone_number, password=None, email=None):
        """
        Creates and returns a regular user with a phone number.
        
        Parameters:
        - name: The name of the user.
        - phone_number: The phone number of the user.
        - password: The password for the user account.
        - email: Optional email address for the user.
        
        Returns:
        - The created user instance.
        
        Raises:
        - ValueError: If name or phone_number is not provided.
        """
        if not name:
            raise ValueError("Users must have a name")
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            name=name,
            phone_number=phone_number,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser and PermissionsMixin.
    Represents a user with a name, phone number, and optional email.
    """
    name = models.CharField(max_length=255,null = True)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)

    objects = UserManager() # Set the user manager

    USERNAME_FIELD = 'phone_number' # Defines the unique identifier for authentication
    REQUIRED_FIELDS = ['name'] # required when creating a user

    def __str__(self):
        """
        Returns the string representation of the user's Name.
        """
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Save the user instance and automatically add to GlobalContact, even if the phone number is present,
        as long as the name is different.
        """
        # Call the original save method to ensure the user is saved first
        super().save(*args, **kwargs)

        # Check if a GlobalContact with the same phone number and different name exists
        contact_exists = GlobalContact.objects.filter(phone_number=self.phone_number, name=self.name).exists()

        # If the contact with the same phone number and different name does not exist, create a new one
        if not contact_exists:
            GlobalContact.objects.create(
                name=self.name,
                phone_number=self.phone_number,
                email=self.email
            )



class GlobalContact(models.Model):
    """
    Model representing a global contact database.
    Stores contact details including name, phone number, and optional email.
    """
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)

    REQUIRED_FIELDS = ['name', 'phone_number']

class SpamReport(models.Model):
    """
    Model representing a report of spam.
    Stores the phone number and count of spam reports.
    """
    phone_number = models.CharField(max_length=10)
    spamCount = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['phone_number']
