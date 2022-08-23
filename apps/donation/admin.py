from django.contrib import admin

from apps.donation.models import  CustomUser, Donor, Predict

admin.site.register(Donor)
admin.site.register(CustomUser)
admin.site.register(Predict)

