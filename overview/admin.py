from django.contrib import admin
#
from .models import Booking
#
# # with that Bookings are shown in the admin page
admin.site.register(Booking)
