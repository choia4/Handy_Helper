
from django.db import models
import re
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        errors = {}
        user = Users.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "first name should be over 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name']= "last name should be over 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email"
        elif user != None and len(user) > 0:
            errors["email"] = "email associated to account already exists"
        if len(postData['password']) < 8:
            errors['password'] = "password should be at least 8 characters"
        if postData['password'] != postData['confirm'] or len(postData['password']) == 0:
            errors['confirm'] = "password does not match confirmation password"
        return errors
    def login_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        user = Users.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email"
        elif len(user) == 0:
            errors['email'] = "there is no email associated to this account"
        if len(postData['password']) < 8:
            errors['password'] = "password should be at least 8 characters"
        elif postData['password'] != user.values()[0]['password']:
            errors['password'] = 'password is incorrect' 
        return errors
    def job_validator(self, postData):
        errors = {}
        if len(postData['description']) < 3:
            errors['destination'] = "description must be at least 3 characters long"
        if len(postData['title']) < 3:
            errors['title'] = 'the title of the job must be at least 3 characters long'
        if len(postData['location']) < 3:
            errors['location'] = 'the location of the job must be at least 3 characters long'
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Jobs(models.Model):
    job = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    assigned_to = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_in_job = models.ForeignKey('Users', related_name="user_in_job", on_delete=models.CASCADE)
    users_in_jobs = models.ManyToManyField('Users', related_name="users_in_jobs")
    objects = UserManager()

class Categories(models.Model):
    name = models.CharField(max_length = 255, default="None")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories_in_job = models.ForeignKey('Jobs', related_name="categories_in_job", on_delete=models.CASCADE)
    objects = UserManager()
