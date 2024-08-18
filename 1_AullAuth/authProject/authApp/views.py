from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render


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