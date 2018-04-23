from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from .forms import PasswordResetForm
from . import views

app_name="coreExtend"

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(
        template_name='coreExtend/login.html',
        extra_context={'account_settings': True,}),
        name='login'
    ),
    # Password Change
    url(r'^account/password/$', auth_views.password_change, {
        'template_name': 'coreExtend/account/password_change_form.html',
        'post_change_redirect': 'coreExtend:password_change_done',
        'extra_context': {'account_settings': True,},
    }, name='password_change'),

    # Password Change Done
    url(r'^account/password/done/$', auth_views.password_change_done, {
        'template_name': 'coreExtend/account/password_change_done.html',
        'extra_context': {'account_settings': True,},
    }, name='password_change_done'),

    # Password reset
    url(r'^password_reset/$', auth_views.password_reset, {
          'template_name': 'coreExtend/account/password_reset/form.html',
          'email_template_name': 'coreExtend/account/password_reset/email.txt',
          'subject_template_name': 'coreExtend/account/password_reset/email_subject.txt',
          'password_reset_form': PasswordResetForm,
          'post_reset_redirect' : 'coreExtend:password_reset_done',
        }, name='password_reset'
    ),

    # Password Reset Done
    url(r'^password_reset/done/$', auth_views.password_reset_done, {
        'template_name': 'coreExtend/account/password_reset/done.html',
    }, name='password_reset_done'),

    # Password Reset confirm
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {
            'template_name': 'coreExtend/account/password_reset/confirm.html',
        }, name='password_reset_confirm',),

    # Password reset complete
    url(r'^password_reset/complete/$', auth_views.password_reset_complete, {
        'template_name': 'coreExtend/account/password_reset/complete.html',
    }, name='password_reset_complete'),

    url(r'^logout/$', views.logout_user, name='Logout'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^account/$', views.EditAccount, name='AccountSettings'),
]
