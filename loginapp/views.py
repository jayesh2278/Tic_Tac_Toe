from django.shortcuts import render

# Create your views here.
import email
from django.shortcuts import render,redirect
from .forms import SignupForm,AuthenticationForm, loginform
from django.contrib.auth import login, authenticate  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes ,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model  
 
  
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form})    


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponseRedirect('login1/')
        #return HttpResponseRedirect('adrs/')  
    else:  
        return HttpResponse('Activation link is invalid!')  


def login1(request):
    if request.method == "POST":
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print(username)
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(username=User.objects.get(email=username).username, password=password)
            except:
                user = authenticate(username=username, password=password)    
            if user is not None:
                    login(request, user)

                ##### add page url after login

                    return redirect('chat/a')
                
            else:
                    return HttpResponse('You are now logged in as not user')
                    
        else:
           return HttpResponse('You are now logged in not valid ')

        #print(form)
        # if form.is_valid():
        #     email = request.POST['username']
        #     print(email) 
        #     raw_password = request.POST['password']
        #     print(raw_password) 

        #     try:
        #          account = authenticate(username=User.objects.get(email=username).username,password=password)
        #          if account is not None:
        #              login(request, user)
        #              return HttpResponse("ok with email")

        #     except:
        #          account = authenticate(username=username, password=password)
        #          if account is not None:
        #              login(request, account)
        #              return HttpResponse('ok with username')
        

    else:
        form = loginform()
        return render(request,'loginform.html',{"form":form})
