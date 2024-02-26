from django.shortcuts import redirect, render
from django.contrib import messages, auth
from .models import Account
from.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id

#verification email
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            

            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
                        
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()
            #messages.success(request, 'We have sent you a verification email to your email adress')
            return redirect('/account/login/?command=verification&email ='+email)
    else:
        form = RegistrationForm()

    
    context={
        'form':form,
    }
    return render(request, 'accounts/register.html', context)
    
def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email, password = password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exist = CartItem.objects.filter( cart= cart).exists()
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart = cart)
                    #getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                        #get cart items from the user to access the product variations
                        cart_item = CartItem.objects.filter(user = user)
                        ex_var_list =[]
                        id=[]
                        for item in cart_item:
                            existing_variation = item.variation.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)

                        cart_item = CartItem.objects.filter(user = user)
                        ex_var_list =[]
                        id=[]
                        for item in cart_item:
                            existing_variation = item.variation.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)

                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id = item_id)
                                item.quantity +=1
                                item.user = user
                                item.save() 
                            else:
                                cart_item = CartItem.objects.filter(cart= cart)
                                
                                for item in cart_item:
                                   item.user = user
                                   item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials!')
            redirect('login')

    return render(request, 'accounts/signin.html')


@login_required(login_url = 'login')
def Logout(request):
    auth.logout(request)
    messages.success(request, 'You are Logged out')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError, ValueError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account is activated")
        return redirect('login')
    else:
        messages.error(request, 'invalid Activation Link')
        return redirect('register')
    
@login_required(login_url='login')
def Dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__iexact = email)

#reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
                        
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')

        else:
            messages.error(request, "Account does not exist!")
            return redirect('forgotPassword')
    return render(request, 'accounts/forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError, ValueError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'please reset your password')
        return redirect('reset_password')
    
    else:
        messages.error(request, 'This link is expired')
        return redirect('login')
    
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['create_password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset successful")
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')