from ast import Return
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from apps import donation
from apps.donation.apps import DonationConfig
from apps.donation.forms import CustomUserForm, DonorForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.donation.models import Donor


def home(request):
    return render(request, 'pages/home.html')


def About(request):
    return render(request, 'pages/about_us.html')


def Services(request):
    return render(request, 'pages/services.html')


def Gallery(request):
    return render(request, 'pages/gallery.html')


def Contact(request):
    return render(request, 'pages/contact_us.html')


def SignUp(request):
    if (request.method == "POST"):
        context = dict()
        form = CustomUserForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            login(request, user)
            context['message'] = messages.success(
            request, "Sign up sucessfully...!!!", )
            return redirect('donation:signin')
    else:
        form = CustomUserForm()
    return render(request, 'pages/login/signup.html', {'form': form})


def SignIn(request):
    context = dict()
    if (request.method == "POST"):
        form = AuthenticationForm(request, data=request.POST)
        if (form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            context['message'] = messages.success(
            request, "Sign in sucessfully...!!!", )
            if user is not None:
                login(request, user)
                return redirect("/")

    else:
        form = AuthenticationForm()
        return render(request, "pages/login/signin.html", {'form': form})


@login_required(login_url='/signup/')
def AddDonor(request):
    context = dict()
    if (request.method == "POST"):
        form = DonorForm(request.POST, request.FILES)
        if (form.is_valid()):
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            context['message'] = messages.success(
            request, "Log in sucessfully...!!!", )
            return HttpResponseRedirect("/")
    else:
        form = DonorForm()
    return render(request, "pages/donor_home.html", {'form': form})


def SignOut(request):
    logout(request)
    return HttpResponseRedirect('/')


def welcome(request):
    context = dict()
    if (request.user.is_authenticated):
        try:
            context['info'] = Donor.objects.get(user__id=request.user.id)
        except:
            pass

    return render(request, 'pages/welcome.html', context)


def donor_update(request, id):
    context = dict()
    if (request.method == "POST"):
        donor = Donor.objects.get(id=id)
        form = DonorForm(request.POST, request.FILES, instance=donor)
        if (form.is_valid()):
            form.save()
            context['message'] = messages.success(
            request, "Update sucessfully...!!!", )
            return HttpResponseRedirect('/')
    else:
        donor = Donor.objects.get(id=id)
        form = DonorForm(instance=donor)

    context = {
        'form': form,
    }

    return render(request, 'pages/donor_update.html', context)


def Logout(request):
    logout(request)
    return redirect('/')

def donor_delete(request, pk):
    context = dict()
    try:
        donor = donor.objects.get(id=pk)
        donor.delete()
        context['message'] = messages.success(
            request, "Item sucessfully deleted", )
    except donor.DoesNotExist:
        context['message'] = messages.error(
            request,
            "Item doesn't exist", )
    return redirect("/")
