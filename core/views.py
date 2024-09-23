from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, CustomTokenObtainPairSerializer, GlobalContactSerializer, SpamReportSerializer
from .models import GlobalContact, SpamReport


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    view for obtaining JWT tokens.
    Uses the CustomTokenObtainPairSerializer to handle token generation.
    """
    serializer_class = CustomTokenObtainPairSerializer

class RegisterUser(generics.CreateAPIView):
    """
    View for user registration.
    Allows users to create a new account. Name and PhoneNo. required.
    Phone Number should be unique i.e not already registered
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
        
class UserSearchView(generics.GenericAPIView):
    """
    View for searching users or contacts.
    Allows authenticated users to search for users by name/phone number.

    If whole phone number is provided and is in registered user database it returns that user only.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)
        if query is None:
            return Response({"detail": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)
        

        user = User.objects.filter(phone_number=query).first()

        if user:
                # Serialize and return the user if found
                user_data = UserSerializer(user).data
                spam_count = SpamReport.objects.filter(phone_number=user.phone_number).first()
                user_data['spam_count'] = spam_count.spamCount if spam_count else 0
                return Response(user_data, status=status.HTTP_200_OK)

        # Search for contacts by name or phone_number in GlobalContact
        contacts = GlobalContact.objects.filter(
            Q(name__icontains=query) | Q(phone_number__icontains=query)
        )

        # Serialize contacts and add spam count information
        results = []
        for contact in contacts:
            spam_count = SpamReport.objects.filter(phone_number=contact.phone_number).first()
            contact_data = GlobalContactSerializer(contact).data
            contact_data['spam_count'] = spam_count.spamCount if spam_count else 0
            results.append(contact_data)

        return Response(results, status=status.HTTP_200_OK)

class ReportSpamView(generics.GenericAPIView):
    """
    View for reporting spam.
    Allows authenticated users to report a phone number as spam. Increase the spamCount of that number in record.
    """
    serializer_class = SpamReportSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Get or create the SpamReport for this phone number
            spam_report, created = SpamReport.objects.get_or_create(phone_number=phone_number)

            # Increment the spam count
            spam_report.spamCount += 1
            spam_report.save()

            return Response({
                "message": "Spam report successfully recorded.",
                "phone_number": phone_number,
                "spam_count": spam_report.spamCount
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)