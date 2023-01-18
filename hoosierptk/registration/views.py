from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm
from django.contrib.auth import logout as lt


# Create SignUp View
def SignUp(request):
    context = {}
    form = UserCreationForm(request.POST or None)  # use Django user creation form

    if request.method == "POST":  # check if request method is POST
        if form.is_valid():  # check if form is valid
            new_user = form.save()  # save new user (if POST and valid form)
            login(request, new_user)  # login the new user automatically
            return redirect("registration:update_profile")  # redirect new user to update profile page

    context.update({
        "form": form,
        "title": "SignUp",
    })  # update context dictionary to send form to the template

    return render(request, "registration/signup.html", context)


# Create SignIn View
def SignIn(request):
    context = {}
    form = AuthenticationForm(request, data=request.POST)  # use Django authentication form

    if request.method == "POST":  # check if request method is POST
        if form.is_valid():  # check if form is valid
            user = form.cleaned_data.get("username")  # get user-enterred username
            password = form.cleaned_data.get("password")  # get user-enterred password

            # authenticate user-enterred information
            user = authenticate(username=user, password=password)
            if user is not None:  # check if the user is valid (successfully authenticated)
                login(request, user)  # login the user automatically
                return redirect("forums:home")  # redirect user to home page

    context.update({
        "form": form,
        "title": "SignIn",
    })  # update context dictionary to send form to the template

    return render(request, "registration/signin.html", context)


# Create Update Profile View
@login_required  # make sure user is signed in / authenticated (can use loginrequiredmixin instead?)
def update_profile(request):
    context = {}
    user = request.user  # get the authenticated user
    form = UpdateProfileForm(request.POST, request.FILES)  # uploading picture/files = request.FILES

    if request.method == "POST":  # check if request method is POST
        if form.is_valid():  # check if form is valid
            update_profile = form.save(commit=False)  # create an instance of the user-submitted form
            update_profile.user = user  # update the profile of the authenticated user
            update_profile.save()  # save the manually updated form
            return redirect("forums:home") # redirect user to home page

    context.update({
        "form": form,
        "title": "Update Profile",
    })  # update context dictionary to send form to the template

    return render(request, "registration/update.html", context)


# Create Logout View
@login_required  # make sure user is signed in / authenticated
def logout(request):
    lt(request)  # log the user out with Django logout function
    return redirect("forums:home")  # redirect user to home page