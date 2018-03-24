from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from .models import Users, Quotes, Faves
import bcrypt, re

def index(request):
    return render(request, "belt/index.html")

def register(request):
    if request.method =='POST':
        request.session["name"] = request.POST["name"]
    hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    print "hash1", hash1
    errors = Users.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/")
    else:
        user = Users.objects.create(name = request.POST["name"], alias = request.POST["alias"], email = request.POST["email"], birthdate = request.POST["birthdate"], password = hash1)
        user.save()
        reguser = Users.objects.filter(email__contains=request.POST["email"])
        for name in reguser:
            request.session["user_id"] = name.id
            # print "user_id ", request.session["user_id"]
        return redirect("/quotes")

def login(request):
    loginerrors = Users.loginobjects.login_validator(request.POST)
    user = Users.objects.filter(email__contains=request.POST["loginemail"])
    for name in user:
        request.session["user_id"] = name.id
        # print "user id ", request.session["user_id"]
        request.session["name"] = name.name
    if len(loginerrors):
        for tag, loginerror in loginerrors.iteritems():
            messages.error(request, loginerror, extra_tags=tag)
        return redirect("/")
    else:
        return redirect("/quotes")

def quotes(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        'quotes': Quotes.quotesobjects.all().exclude(user=Users.objects.filter(id=request.session["user_id"])), 
        'faves': Faves.objects.select_related('favequote').filter(userfave=Users.objects.get(id=request.session["user_id"]))
    }
    return render(request, "belt/quotes.html", context)

def addquote(request):
    if request.method =='POST':
        quoteserrors = Quotes.quotesobjects.quote_validator(request.POST)
        if len(quoteserrors):
            for tag, quoteserror in quoteserrors.iteritems():
                messages.error(request, quoteserror, extra_tags=tag)
            return redirect("/quotes")
        else:
            quotes = Quotes.quotesobjects.create(quote = request.POST["message"], quoter = request.POST["quoter"], user = Users.objects.get(id = int(request.session["user_id"])))
            quotes.save()
            return redirect("/quotes")

def addtomylist(request):
    if request.method == 'POST':
        faves = Faves.objects.create(userfave = Users.objects.get(id=request.session["user_id"]), favequote = Quotes.quotesobjects.get(id=int(request.POST["quoteid"])))
        faves.save()
    return redirect("/quotes")

def remove(request):
    update = Faves.objects.get(id = request.POST["faveid"])
    update.delete()
    return redirect("/quotes")

def user(request, id):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "name": Users.objects.get(id = id),
        "count": Quotes.quotesobjects.filter(user = Users.objects.get(id = id)).count(),
        "posts": Quotes.quotesobjects.filter(user = Users.objects.get(id = id))
    }
    return render(request, "belt/user.html", context)

def logout(request):
    if request.method == "POST":
        for key in request.session.keys():
            request.session.pop(key)
        return redirect("/")

