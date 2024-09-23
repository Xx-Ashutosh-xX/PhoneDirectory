from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from .models import SpamReport, GlobalContact

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens.
    Adds additional user information to the token payload.
    """
    @classmethod
    def get_token(cls, user):
        """
        Override method to include custom claims in the JWT token.
        
        Parameters:
        - user: The user instance for which the token is being created.
        
        Returns:
        - A JWT token with additional claims.
        """
        token = super().get_token(user)
        token['name'] = user.name
        return token

    def validate(self, attrs):
        """
        Validate the credentials and return token data if valid.
        
        Parameters:
        - attrs: The credentials provided in the request (e.g., phone_number and password).
        
        Returns:
        - A dictionary containing the validated token and user data if credentials are valid.
        
        Raises:
        - serializers.ValidationError: If the credentials are invalid.
        """
        phone_number = attrs.get("phone_number", None)
        password = attrs.get("password", None)
        
        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.check_password(password):
            # Validate the token and return user data along with the token
            data = super().validate(attrs)
            data.update({'user_id': user.id, 'name': user.name})
            return data
        else:
            # Raise an error if credentials are invalid
            raise serializers.ValidationError("Invalid credentials")


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Handles serialization and deserialization of user data.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        """
        Create a new user instance with the provided validated data.
        
        Parameters:
        - validated_data: The validated user data.
        
        Returns:
        - The created user instance.
        """
        user = User(
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password']) # Set hashed password
        user.save()
        return user
    
class GlobalContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the GlobalContact model.
    Handles serialization and deserialization of global contact data.
    """
    class Meta:
        model = GlobalContact
        fields = ['name', 'phone_number', 'email']
    
class SpamReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the SpamReport model.
    Handles serialization and deserialization of spam report data.
    """
    phone_number = serializers.CharField(max_length=15)

    class Meta:
        model = SpamReport
        fields = ['phone_number']
