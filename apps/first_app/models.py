from __future__ import unicode_literals
from django.db import models
import re
import bcrypt 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def user_val(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = 'You must enter a first name!'
        if len(postData['last_name']) < 2:
            errors["last_name"] = 'You must enter a last name!'
        if len(postData['email']) < 1:
            errors["email"] = 'You must enter an email!'
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = 'You must use proper email syntax!'
        if len(User.objects.filter(email = postData['email'])):
            errors["email"] = 'Email already exists'
        if len(postData['password']) < 8:
            errors["password"] = 'Your password must be at least 8 characters!'
        if postData['password_conf'] != postData['password']:
            errors["password_conf"] = 'Your passwords must match!'
        return errors

    def edit_val(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = 'You must enter a first name!'
        if len(postData['last_name']) < 1:
            errors["last_name"] = 'You must enter a last name!'
        if len(postData['email']) < 1:
            errors["first_name"] = 'You must enter an email!'
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = 'You must use proper email syntax!'
        if len(User.objects.filter(email = postData['email'])):
            errors["email"] = 'Email already exists'
        return errors

    def login_val(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors["first_name"] = 'You must enter an email!'
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = 'You must use proper email syntax!'
        if len(User.objects.filter(email = postData['email'])):
            errors["email"] = 'Email already exists'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_val(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors["author"] = 'Author must have at least 3 characters!'
        if len(postData['quote']) < 3:
            errors["quote"] = 'Quote must have at least 10 characters!'
        return errors

    
class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name="quotes")
    objects = QuoteManager()

class Like(models.Model):
    liked_message = models.ForeignKey(Quote, related_name="likes")
    liker = models.ForeignKey(User, related_name="liked_messages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)