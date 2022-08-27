from ast import Return
from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from apps import donation
from apps.donation.apps import DonationConfig
from apps.donation.forms import CustomUserForm, DonorForm, PredictForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.donation.models import CustomUser, Donor, Predict

# Data manipulation
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns


# Data Visualization
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import matplotlib.ticker as mticker

# Data Classification
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import confusion_matrix, classification_report

# predict import
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier


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

def QRCode(request):
    return render(request, 'pages/qr_code.html')


def SignUp(request):
    if (request.method == "POST"):
        context = dict()
        form = CustomUserForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            login(request, user)
            context['message'] = messages.success(
                request, "Sign up Successfully...!!!", )
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
                request, "Log in Successfully...!!!", )
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
                request, "Donate Successfully...!!!", )
            return HttpResponseRedirect("/")
    else:
        form = DonorForm()
    return render(request, "pages/donor_home.html", {'form': form})


def SignOut(request):
    context = dict()
    logout(request)
    context['message'] = messages.success(
                request, "Sign out Successfully...!!!", )
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
                request, "Update Successfully...!!!", )
            return HttpResponseRedirect('/')
    else:
        donor = Donor.objects.get(id=id)
        form = DonorForm(instance=donor)

    context = {
        'form': form,
    }

    return render(request, 'pages/donor_update.html', context)


def Logout(request):
    context = dict()
    context['message'] = messages.success(
                request, "Log out successfully...!!!", )
    logout(request)
    return redirect('/')


def donor_delete(request, id):
    context = dict()
    try:
        donor = Donor.objects.get(id=id)
        donor.delete()
        context['message'] = messages.success(
            request, "Donation Sucessfully deleted", )
    except donor.DoesNotExist:
        context['message'] = messages.error(
            request,
            "Item doesn't exist", )
    return redirect("/")


def predict(request):
    context = dict()
    if request.user.is_authenticated:
        email = request.user.email

    if (request.method == "POST"):
        form = PredictForm(request.POST)
        Tshirt = pd.read_csv("Tshirt_Sizing_Dataset.csv")

        val1 = float(request.POST['height'])
        val2 = float(request.POST['weight'])

        X = Tshirt.drop("T Shirt Size", axis=1)
        y = Tshirt["T Shirt Size"]

        labelencoder_y = LabelEncoder()
        y = labelencoder_y.fit_transform(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
        classifier.fit(X_train, y_train)
        size = classifier.predict([[val1, val2]])
        print(f"size {size}")
        result1 = ""
        if size == [0]:
            result1 = "Large Size"
        else:
            result1 = "Small Size"
        print(type(size))

        messages.success(
            request,
            f"{ email } :  {result1} ",
        )
        context['message'] = messages.success(
                request, "Pridected Sucessfully...!!!", )
     
        if (form.is_valid()):
          
            user = request.user
            ins = Predict(user = user, height=val1, weight=val2, size= result1, )
            ins.save()
            
            return HttpResponseRedirect("/")
    else:
        form = PredictForm()

    context = {
        'form': form
    }
    return render(request, 'pages/predict.html', context)
