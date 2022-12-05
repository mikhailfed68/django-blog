from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages

from users.forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрированы!')
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignUpForm()
        return render(
            request,
            'registration/signup.html',
            dict(form=form),
        )
