from django.core.management.base import BaseCommand
from core.models import GlobalContact
import random
import faker

class Command(BaseCommand):
    """
    Create a Django management command to generate random global contacts.

    runby: 'python manage.py generate_global_contacts'
    """
    help = 'Generate random global contacts'

    def handle(self, *args, **kwargs):
        """
        Generate and create random GlobalContact entries.
        
        Parameters:
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.
        """
        fake = faker.Faker()
        
        for i in range(10):  # Number of contacts to generate
            name = fake.first_name()
            phone_number=str(random.randint(100000000, 999999999))
            email=f'{name}@example.com'

            # Create the GlobalContact entry
            GlobalContact.objects.get_or_create(
                name=name,
                phone_number=phone_number,
                email=email
            )
        
        self.stdout.write(self.style.SUCCESS('Global contacts generated successfully'))
