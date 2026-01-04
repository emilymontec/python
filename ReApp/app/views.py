from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def admin_view(request):
    return render(request, 'admin.html')