from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from users.forms import RegistrationForm, LoginForm, UserProfileUpdateForm
from users.models import Account

from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages


@login_required
def user_profile_view(request):
    return render(request, 'users/user_profile.html')


def registration_view(request):
    '''
    View used to register users
    '''
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            user.full_name = user.first_name +' '+ user.last_name
            user.save()

            # Send an email to the user with the token:
            current_site = get_current_site(request)
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Floq account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
            messages.info(request, 'You must confirm your email address before logging in.')
            return redirect('login')

        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'users/register.html', context)


User = get_user_model()


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    '''
    This function activates the user after he/she has confirmed the used email
    '''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend)
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login_success')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('register')


def logout_view(request):
    logout(request)
    return redirect('landingpage')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("login_success")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                request.session['userord']= user.pk
                login(request, user)
                messages.success(request, 'You are logged in now.')
                return redirect("login_success")

    else:
        form = LoginForm()

    context['login_form'] = form

    # print(form)
    return render(request, "users/login.html", context)

@login_required
def login_success_view(request):
    '''
    Redirects users based on they are allocated to an organization or not
    '''
    if request.user.organization == None:
        # user does not have a organization
        return redirect('organization_setup')
    else:
        return redirect("overview")

@login_required
def user_profile_view(request):
    '''
    Allows users to change their account settings
    :cvar
    '''

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "first_name": request.POST['first_name'],
                "last_name": request.POST['last_name'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = UserProfileUpdateForm(
            initial={
                "email": request.user.email,
                "last_name": request.user.last_name,
                "first_name": request.user.first_name,
            }
        )

    context['user_form'] = form
    return render(request, 'users/user_profile.html', context)
