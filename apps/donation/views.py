from ast import Return
from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from apps import donation
from apps.donation.apps import DonationConfig
from apps.donation.forms import CustomUserForm, DonorForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.donation.models import Donor

# Data manipulation
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
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


def predict(request):
        # Loading the data 
#     df = pd.read_csv('final_test.csv')

#     # Cleaning data 
#     df.dropna(inplace=True)

#     # Removing age outliers
#     df = df[df['age'] > 9]
#     df = df[df['age'] < 90]
#     # Overview of data
#     sns.pairplot(data=df, hue='size', height=7)
# # getting the unique sizes present in the dataset and turning the string labels into int labels 
#     SizeChart = [];
#     for label in df['size']:
#         if label == 'XXS':
#             SizeChart.append(1)
#         if label == 'S':
#             SizeChart.append(2)
#         if label == 'M':
#             SizeChart.append(3)
#         if label == 'L':
#             SizeChart.append(4)
#         if label == 'XL':
#             SizeChart.append(5)
#         if label == "XXL":
#             SizeChart.append(6)
#         if label == "XXXL":
#             SizeChart.append(7)
        
#     df['SizeLabels'] = SizeChart
#     SizeTicks = ['XXS','S', 'M', 'L', 'XL', 'XXL', 'XXXL']

# # dropping the size column with strings for ease of Visualizarion
#     plt_df = df.drop('size',axis=1)
#     plt_colnames = ['Weight (kg)', 'Age (Years)','Height (cm)','Size Labels']
#     plt_df.columns = plt_colnames

#     pre_df = df.drop("size", axis=1)
# # Preping the data
#     Features = pre_df.drop('SizeLabels', axis = 1)

#     # seperating out the labels
#     labels = pre_df['SizeLabels']

#     # Generating test set and training set (trainf)
#     trainingFeatures, testingFeatures, trainingLabels, testingLabels = train_test_split(Features, labels, test_size = .2, random_state=42)

#     # now we gonna set up a scale for the values!
#     scaler = StandardScaler()

#     # Scaling the features after splitting them
#     trainingFeatures = scaler.fit_transform(trainingFeatures)
#     testingFeatures = scaler.transform(testingFeatures)


#     # KNeighboors Classifer
#     from sklearn.neighbors import KNeighborsClassifier 
#     # These are used to keep track of the best score obtained by the model
#     BestN = 0
#     prev = 0
#     accuracy = []

#     for x in range(80,150,5):
#         # Declare a model
#         model = KNeighborsClassifier(n_neighbors=x, metric='manhattan', weights='uniform') 

#         # Fit the model
#         model.fit(trainingFeatures, trainingLabels)

#         # Trying to predict the model
#         score = model.score(testingFeatures,testingLabels) * 100
#         # Iteritive testing for nieghbors score
#         if score > prev:
#             prev = score
#             BestN = x
#         # Creating meterics to identify optimal neighbors
#         accuracy.append(score)

#     # For model comparision
#     clusterScore = (np.mean(accuracy))

#     # Multiple Linear Regression
#     from sklearn.linear_model import LinearRegression

#     # Declare Model
#     model = LinearRegression()

#     # Fit Model
#     model.fit(trainingFeatures, trainingLabels)

#     # Scoring the model --- 69%
#     regressionScore = (model.score(testingFeatures,testingLabels)) * 100


# # Graph comparing the model effectness (95% reflection on the graph!)
#     Y = [clusterScore*.95, regressionScore*.95]
#     X = ["Neighbors" , "Regression"]
#     sns.barplot(y=Y, x=X)
#     plt.show()
#     print("Neighbors method averaged a score of: " + clusterScore.astype(str) + "\n\n")
#     print("Regression method average a score of: " + regressionScore.astype(str))

    return render(request,"pages/predict.html")
