

from django.contrib import admin

from .models import *

# class VehicleAdmin(admin.ModelAdmin):
#     list_display =  ('id',)


class TripAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'driver', 'starting_location',
                    'destination', 'created_at', 'status')
    search_fields = ('vehicle__license_plate', 'driver__fullname',
                     'starting_location', 'destination')
    list_filter = ('status',)


admin.site.register(Trip, TripAdmin)

admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(QrCode)
admin.site.register(Security)
