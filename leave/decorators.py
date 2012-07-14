# This Python file uses the following encoding: utf-8

import logging
from django.contrib import messages
from django.shortcuts import redirect

def user_allowed(funct):
    def wrapped(request, user_id, *args, **kwargs):
        if request.user.id == int(user_id):
            return funct(request,user_id,*args,**kwargs)
        else:
            messages.add_message(request,messages.ERROR, 'Nie posiadasz uprawnień. Zaloguj sie na swoje konto')
            return redirect('django.contrib.auth.views.login')
    return wrapped
