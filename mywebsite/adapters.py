from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render


User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        """
        Only allow linking, prevent signup from Google unless the user already exists.
        """
        
        if request.user.is_authenticated:
            print("User is authenticated, allowing linking.")
            return True  # Linking is allowed
        else:
            print("User not authenticated, checking if email exists.")
            # If user not logged in, block signup unless email exists
            email = sociallogin.account.extra_data.get('email')
            return User.objects.filter(email=email).exists()

    def pre_social_login(self, request, sociallogin):
        """
        This runs before a social login completes.
        If the Google account is not linked to an existing user,
        raise an error and block the login.
        """
        email = sociallogin.user.email
        provider = sociallogin.account.provider  # 'google' in this case
        
        
        google_email = sociallogin.account.extra_data.get('email')
        
        
        if request.user.is_authenticated:
            print("User is authenticated, checking linking rules.")
            current_user = request.user
            print(f"Current user email: {current_user.email}, Google email: {google_email}")
            
            # Rule 2: Prevent this Google account from being linked to another user
            if SocialAccount.objects.filter(provider='google', uid=sociallogin.account.uid).exclude(user=current_user).exists():
                raise ImmediateHttpResponse(
                    render(request, "authentication_error.html", {
                        "message": "This Google account is already linked to another user."
                    })
                )
                
            
            # Rule 3: Prevent the user from linking multiple Google accounts
            if SocialAccount.objects.filter(user=current_user, provider='google').exists():
                raise ImmediateHttpResponse(
                    render(request, "authentication_error.html", {
                        "message": "This Google account is already linked to your profile."
                    })
                )
            
            
            # Rule 1: Google email must match registered email
            if current_user.email.lower() != google_email.lower():
                raise ImmediateHttpResponse(
                    render(request, "authentication_error.html", {
                        "message": "The Google account email must match your registered email."
                    })
                )
                
            # ✅ If no errors, Allauth will proceed and link the account
            # At this point, the link is considered successful
            self.on_google_link_success(request, current_user, sociallogin)
            return  # Allow linking to proceed

        linked_exists = SocialAccount.objects.filter(
            user__email=email,
            provider=provider
        ).exists()

        print(f"Linked exists: {linked_exists} for email: {email} and provider: {provider}")
        if not linked_exists:
            # Block login
            raise ImmediateHttpResponse(
                    render(request, "authentication_error.html", {
                        "message": "This Google account is not linked to any users."
                    })
                )
    def on_google_link_success(self, request, user, sociallogin):
        """
        Handle actions after a Google account is successfully linked to a user.
        """
        # Example 1: Show a success message in the UI
        messages.success(request, f"Your Google account ({sociallogin.account.extra_data.get('email')}) has been successfully linked!")

        # Example 2: Logging for audit purposes
        print(f"[SUCCESS] User {user.username} ({user.email}) successfully linked Google account with UID: {sociallogin.account.uid}")

        # Example 3: Optional - trigger custom actions
        # For example, you could send an email notification
        # send_mail(
        #     "Google Account Linked",
        #     "Your Google account has been successfully linked to your profile.",
        #     "no-reply@mywebsite.com",
        #     [user.email]
        # )