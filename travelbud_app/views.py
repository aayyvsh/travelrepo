from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.db.models import Q
from .models import User, Trip 

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    validationErrors = User.objects.regValidator(request.POST)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    hashedPw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(name = request.POST['name'], username = request.POST['uname'], password = hashedPw)
    request.session['loggedInUserID'] = newuser.id

    return redirect("/trips")

def trips(request):
    if 'loggedInUserID' not in request.session:
        return redirect("/")
    loggedInUser = User.objects.get(id = request.session['loggedInUserID'])
    context = {
        'loggedinuser': loggedInUser,
        'alltrips': Trip.objects.all(),
        'mytrips': Trip.objects.filter(user = loggedInUser) | Trip.objects.filter(joiners = loggedInUser),
        'othertrips': Trip.objects.exclude(Q(user = loggedInUser) | Q(joiners = loggedInUser))
    }
    return render(request, "trips.html", context)

def login(request):
    loginErrors = User.objects.loginValidator(request.POST)
    if len(loginErrors)>0:
        for key, value in loginErrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        loggedinuser = User.objects.filter(username = request.POST['uname'])
        loggedinuser = loggedinuser[0]
        request.session['loggedInUserID'] = loggedinuser.id
        return redirect("/trips")

def logout(request):
    request.session.clear()
    return redirect("/")

def addtrip(request):

    return render(request, "addtrip.html")

def createtrip(request):
    print(request.POST)
    tripErrors = User.objects.tripValidator(request.POST)
    if len(tripErrors)>0:
        for key, value in tripErrors.items():
            messages.error(request, value)
        return redirect ("/trips/add")
    loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
    newtrip = Trip.objects.create(destination = request.POST['dest'], user = loggedinuser, description = request.POST['desc'], travelfrom = request.POST['tdfrom'], travelto = request.POST['tdto'])
    print(newtrip)
    return redirect("/trips")

def jointrip(request, tripID):
    loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
    jointrip = Trip.objects.get(id = tripID)
    loggedinuser.trip_joiners.add(jointrip)
    return redirect("/trips")

def location(request, tripID):
    context = {
        "place": Trip.objects.get(id = tripID)
    }
    return render(request, "location.html", context)