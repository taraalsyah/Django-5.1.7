from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Called just before a social login is processed.
        You can add custom checks or redirects here.
        """
        email = sociallogin.account.extra_data.get('email')
        domain = email.split('@')[-1]

        # Example: Only allow company emails
        if domain != "mycompany.com":
            # You can raise an error or redirect
            return redirect('/access-denied/')
        
        return super().pre_social_login(request, sociallogin)
