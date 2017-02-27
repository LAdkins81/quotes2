from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Quote, Favorite
from django.db.models import Count


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your views here.
def index(request):
    return render(request, 'quote/index.html')

def quotehome(request):
    user_id = request.session['id']
    exclude_quote = Favorite.objects.filter(user=user_id)
    context = {
    'quotes' : Quote.objects.all(),
    'users' : User.objects.all(),
    'favorite' : Favorite.objects.filter(user=user_id)
    }
    return render(request, 'quote/quotes.html', context)

def addquote(request):
    if len(request.POST['quote']) < 1 or len(request.POST['author']) < 1:
        messages.add_message(request, messages.ERROR, 'Invalid entry! You must enter text in both fields.')
        return redirect(reverse('quotes:quotehome'))
    else:
        Quote.objects.newquote(request.POST, request.session['id'])
        return redirect(reverse('quotes:quotehome'))

def user(request, id):
    context = {
    'quotes': Quote.objects.filter(user_id=id),
    'quotecount' : Quote.objects.filter(user_id=id).annotate(Count('id')),
    'user' : User.objects.filter(id=id)
    }
    return render(request, 'quote/user.html', context)

def favorite(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        quote = Quote.objects.get(id=request.POST['bob'])
        print request.POST['bob']
        Favorite.objects.create(quote=quote, user=user)
        return redirect(reverse('quotes:quotehome'))

def remove(request):
    if request.method == 'POST':
        fav_id = request.POST['id']
        Favorite.objects.filter(id=fav_id).delete()
        return redirect(reverse('quotes:quotehome'))

def logout(request):
    request.session.clear()
    return redirect('/')

def authenticate(request):
    if request.method == 'POST':
        user = User.objects.all()
        try:
            login = User.objects.login(request.POST['logemail'], request.POST['logpass'])
            request.session['user'] = login['name']
            request.session['id'] = login['id']
            return redirect(reverse('quotes:quotehome'))
        except:
            messages.add_message(request, messages.ERROR, 'Your username or password is incorrect.')
            return redirect('/')

def register(request):
    error_switch = False
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.add_message(request, messages.ERROR, 'Invalid entry! Please enter a valid email address!')
        error_switch = True

    if len(request.POST['name']) < 2:
        messages.add_message(request, messages.ERROR, 'First name must be longer than 2 letters.')
        error_switch = True
    elif not NAME_REGEX.match(request.POST['name']):
        messages.add_message(request, messages.ERROR, 'First name must contain only letters.')
        error_switch = True

    if len(request.POST['alias']) < 2:
        messages.add_message(request, messages.ERROR, 'Last name must be longer than 2 letters.')
        error_switch = True
    elif not NAME_REGEX.match(request.POST['alias']):
        messages.add_message(request, messages.ERROR, 'Alias must contain only letters.')
        error_switch = True

    if len(request.POST['password']) < 8:
        messages.add_message(request, messages.ERROR, 'Password must be longer than 8 characters.')
        error_switch = True

    if request.POST['confirmpass'] != request.POST['password']:
        messages.add_message(request, messages.ERROR, 'Passwords must match.')
        error_switch = True

    if error_switch == True:
        return redirect('/')

    else:
        if request.method == 'POST':
            newuser = User.objects.register(request.POST)
            request.session['user'] = newuser['name']
            request.session['id'] = newuser['id']
            return redirect(reverse('quotes:quotehome'))
