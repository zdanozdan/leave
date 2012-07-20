# This Python file uses the following encoding: utf-8

import logging
from django.contrib import messages
from django.shortcuts import redirect
#from django.shortcuts import render_to_response, get_object_or_404
#from django.http import HttpResponse, HttpResponseRedirect
#from django.core.urlresolvers import reverse

#from django.contrib.auth.forms import AuthenticationForm
#from django.template import RequestContext


def user_allowed(funct):
    def wrapped(request, user_id, *args, **kwargs):
        if request.user.id == int(user_id) or request.user.is_superuser:
            return funct(request,user_id,*args,**kwargs)
        else:
            messages.add_message(request,messages.ERROR, 'Nie posiadasz uprawnień. Zaloguj sie na swoje konto')
            return redirect('django.contrib.auth.views.login')
    return wrapped
