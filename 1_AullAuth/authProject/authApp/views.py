from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render
from allauth.account.views import SignupView, LoginView


# class MySignupView(SignupView):
#     template_name = '/allauth/account/login.html'


# class MyLoginView(LoginView):
#     template_name = '/allauth/account/login.html'

def index_view(request):
    github_username = None
    
    if request.user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(
                user=request.user,
                provider="github",
            )
            github_username = social_account.extra_data.get("login")
        except SocialAccount.DoesNotExist:
            pass
    
    context = {
        "github_username": github_username
    }
        
    return render(
        request,
        "authApp/index.html",
        context,
    )
    
def dashboard_view(request):
    
    
    return render(
        request,
        "authApp/dashboard.html",
    )