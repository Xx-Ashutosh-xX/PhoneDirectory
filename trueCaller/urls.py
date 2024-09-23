from django.contrib import admin
from django.urls import path, include
from core.views import RegisterUser, UserSearchView, CustomTokenObtainPairView, ReportSpamView

urlpatterns = [
    # URL pattern for obtaining JWT tokens.will return a token pair (access and refresh tokens) upon successful login.
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

     # URL pattern for user registration. By providing Name and Phone Number
    path('api/register/', RegisterUser.as_view(), name='register'),

    # URL pattern for searching users. This endpoint is used to search for users in Database with their name or phone number.
    path('api/search/', UserSearchView.as_view(), name='user-search'),

    # URL pattern for reporting spam. This endpoint allows users to report a number spam
    path('api/report-spam/', ReportSpamView.as_view(), name='report-spam'),
]

