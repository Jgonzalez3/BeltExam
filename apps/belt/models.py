# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime, date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class ValidationManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors["name1"] = "Name cannot be empty/blank"
        if len(postData['name']) < 2:
            errors["name2"] = "Name cannot be less than 2 characters"
        if postData['name'].isalpha() == False:
            errors["name3"] = "Name must be letters only"
        if len(postData['alias']) < 1:
            errors["alias1"] = "Alias cannot be empty/blank"
        if len(postData['alias']) < 2:
            errors["alias2"] = "Alias cannot be less than 2 characters"
        # Email check if registered below: regemail
        regemail = Users.objects.filter(email__contains=postData["email"])
        if len(regemail) > 0:
            errors["email"] = "Cannot use Email entered. Email already in use"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email, Re-Enter"
        ##Birthdate Validation
        date = unicode(datetime.now().strftime('%Y-%m-%d'))
        print "date", date
        print "birthdate", postData["birthdate"]
        if postData['birthdate'] >= date:
            errors["birthdate"] = "Birthdate cannot be in the future nor today"
        ##
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if postData["pw_confirm"] != postData["password"]:
            errors["pw_confirm"] = "Passwords Do Not Match"
        return errors

class LoginValidationManager(models.Manager):
    def login_validator(self, postData):
        loginerrors = {}
        allusers = Users.objects.all()
        if len(allusers) == 0:
            loginerrors["nousers"] = "No Current Users. Please Register"
        loginpassword = Users.objects.filter(email__contains=postData["loginemail"])
        for password in loginpassword:
            if bcrypt.checkpw(postData["loginpassword"].encode(), password.password.encode()) != True:
                loginerrors["loginpassword"] = "Password incorrect"
        loginemail = Users.objects.filter(email__contains=postData["loginemail"])
        for email in loginemail:
            if postData["loginemail"] != email.email:
                loginerrors["loginemail"] = "Email incorrect"
                print loginerrors
        return loginerrors

class QuoteValidationManager(models.Manager):
    def quote_validator(self, postData):
        quoteserrors = {}
        if len(postData['quoter']) < 4:
            quoteserrors["quoter"] = "Quote must be more than 3 characters"
        if len(postData['message']) < 11:
            quoteserrors["message"]
        return quoteserrors

class Users(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationManager()
    loginobjects = LoginValidationManager()
    def __repr__(self):
        return "<id={}> name={} alias={} email={} birthdate={} password={}>".format(self.id, self.name, self.alias, self.email, self.birthdate, self.password)

class Quotes(models.Model):
    quote = models.CharField(max_length=255)
    quoter = models.CharField(max_length=255)
    user = models.ForeignKey(Users, related_name="posted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quotesobjects = QuoteValidationManager()

class Faves(models.Model):
    userfave = models.ForeignKey(Users, related_name='userfave')
    favequote = models.ForeignKey(Quotes, related_name='favequote')
    objects = models.Manager()
    # def __repr__(self):
    #     return "<id={}> userfave={} likes this quote={}>".format(self.id, self.userfave.name, self.favequote.quote)
