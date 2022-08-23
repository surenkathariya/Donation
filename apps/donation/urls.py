from django.urls import path

from apps.donation.views import About, AddDonor, Contact, Gallery, Logout, Services, SignUp, donor_delete, donor_update, home, SignIn, SignOut, predict, welcome

app_name = 'donation'

urlpatterns = [

    path('', home, name='home'),
    path('about', About, name ='about'),
    path('services', Services, name ='services'),
    path('gallery', Gallery, name ='gallery'),
    path('contact', Contact, name ='contact'),


    path('signup', SignUp, name='signup'),
    path('signin', SignIn, name='signin'),
    path('add_donor/', AddDonor, name='add_donor'),
    path('logout/', SignOut, name='logout'),
    path('welcome', welcome, name='welcome'),
    path('donor_update/donor/<int:id>', donor_update, name='donor_update'),
    path('donor_delete/donor/<int:id>', donor_delete, name='donor_delete'),

    path('logout', Logout, name='logout'),
    path('logout', Logout, name='logout'),
    path('predict/',predict,name="predict"),
    # path('predict/result/', result, name='result'),

]

