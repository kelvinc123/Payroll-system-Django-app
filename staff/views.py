from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def help(request):
    return render(request, 'staff/help.html')
