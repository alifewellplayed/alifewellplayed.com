from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import cache
from django.template import RequestContext

from .forms import AccountModelForm, UserCreationForm
from .models import Account

def register(request):
    if not settings.ALLOW_NEW_REGISTRATIONS:
        messages.error(request, "The admin of this service is not allowing new registrations.")
        return redirect(settings.SITE_URL)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Thanks for registering. You are now logged in.')
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return redirect(settings.SITE_URL)
    else:
        form = UserCreationForm()

    return render(request, 'coreExtend/register.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect(settings.SITE_URL)

@login_required
def EditAccount(request):
    account = get_object_or_404(Account, username=request.user)
    if request.method == 'POST':
        f = AccountModelForm(request.POST or None, request.FILES, instance=account)
        if f.is_valid():
            f.save()
            messages.add_message(
                request, messages.INFO, 'Changes saved.')
            return redirect('coreExtend:AccountSettings')
    else:
        f = AccountModelForm(instance=account)
        variables = {'form': f, 'user': account, 'account_settings': True,}
    return render(request, 'coreExtend/account/settings.html', variables)
