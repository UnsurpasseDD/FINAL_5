from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate 
from .form import SignupForm 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.template.loader import render_to_string 
from .token import account_activation_token 
from django.contrib.auth.models import User 
from django.core.mail import EmailMessage
from .models import BaseRegisterForm
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model
# Create your views here.


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
        uid = force_text(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.') 
    else: 
        return HttpResponse('Activation link is invalid!') 



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/ind.html'


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def uprade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')