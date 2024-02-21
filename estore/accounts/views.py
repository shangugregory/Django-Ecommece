from django.shortcuts import render

from .models import Account
from.forms import RegistrationForm

# Create your views here.
def Register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name = first_name, last_name= last_name, email = email, username = username, password= password)
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationForm()

    
    context={
        'form':form,
    }
    return render(request, 'home/register.html', context)
    
def Login(request):
    return render(request, 'home/signin.html')