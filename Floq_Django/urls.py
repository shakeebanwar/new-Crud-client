"""Floq_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf.urls import url
# Default views
from django.contrib import admin
from users import views as user_views
# My apps view
from overview.views import overview_view#, overview_user_view, overview_not_indicated_view, overview_office_view, overview_search_view

from users.views import registration_view, login_view, logout_view, user_profile_view, activate, login_success_view#, registration_teammembers_view

from organization.views import organization_profile_view, office_profile_view, organization_setup_view, \
    team_invitation_view, office_setup_view, BirdAddView, team_profile_view
# Password reset views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registration_view, name='register'),
    # path('register_team/<str:organization_intive_link_end>/', registration_teammembers_view, name='register-team'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login_success/', login_success_view, name='login_success'),
    path('organization_setup/', organization_setup_view, name='organization_setup'),
    path('office_setup/', office_setup_view, name='office_setup'),
    path('team_invitation/', team_invitation_view, name='team_invitation'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user_profile/', user_profile_view, name='user_profile'),
    path('organization_profile/', organization_profile_view, name='organization_profile'),
    path('team_profile/', team_profile_view, name='team_profile'),
    path('office_profile/', office_profile_view, name='office_profile'),
    path('add/', BirdAddView, name="add_bird"),
    # TODO fix login with social auth (not priority rightnow)
    # path('accounts/', include('allauth.urls')),
    path('overview/', overview_view, name='overview'),
    path('overview/<int:year>/<int:month>/<int:day>/', overview_view, name='overview'),
    # path('overview/<int:year>/<int:month>/<int:day>/you', overview_user_view, name='overview-you'),
    # path('overview/<int:year>/<int:month>/<int:day>/not_indicated', overview_not_indicated_view,
    #      name='overview-not-indicated'),
    # path('overview/<int:year>/<int:month>/<int:day>/office/<int:office_id_from_filter>', overview_office_view, name='overview-office'),
    # path('overview/<int:year>/<int:month>/<int:day>/search/<int:user_id>', overview_search_view,
    #      name='overview-search'),

    # re_path(r'^overview/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', overview_view, name='overview'),
    path('', include('landingpage.urls')),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
