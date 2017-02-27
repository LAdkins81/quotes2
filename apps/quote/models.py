from __future__ import unicode_literals

from django.db import models
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    def register(self, info):
        pw = info['password']
        hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        user = User.objects.create(name=info['name'], alias=info['alias'], email=info['email'], password=hashed, birthday=info['dob'])
        return {'name' : user.name, 'id' : user.id}

    def login(self, email, password):
        user = User.objects.get(email=email)
        pw = password
        hashed = bcrypt.hashpw(pw.encode(), user.password.encode())
        if user.password == hashed:
            return {'name' : user.name, 'id' : user.id}

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=100)
    birthday = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=UserManager()

class QuoteManager(models.Manager):
    def newquote(self, info, quoteid):
        user = User.objects.get(id=quoteid)
        quoteinfo = Quote.objects.create(author=info['author'], quote=info['quote'], user=user)
        return {'quote' : quoteinfo.quote, 'author' : quoteinfo.author}

class Quote(models.Model):
    quote = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='user_quote')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=QuoteManager()

class Favorite(models.Model):
    quote = models.ForeignKey(Quote, related_name='favorite_quote')
    user = models.ForeignKey(User, related_name='user_favorite')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
