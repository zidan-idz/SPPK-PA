from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def public_home_view(request):
    """Public landing page - accessible without login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'public_home.html')


@login_required
def dashboard_view(request):
    """Dashboard for authenticated users"""
    return render(request, 'home.html')
