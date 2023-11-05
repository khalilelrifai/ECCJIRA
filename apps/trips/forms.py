from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.db.models import Q

from .models import *


class CreateTripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ['vehicle', 'driver',
                  'starting_location', 'destination', 'note']

        widgets = {
            # 'owner':TextInput(attrs={'disabled':True}),
            'vehicle': forms.Select(attrs={}),
            'driver': forms.Select(attrs={}),
            'starting_location': forms.TextInput(attrs={'cols': '4'}),
            'destination': forms.TextInput(attrs={'cols': '4'}),
            'note': forms.Textarea(attrs={'rows': '4'}),
        }

        labels = {
            'vehicle': ('Available Cars'),
            'driver': ('Available Drivers'),


        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all vehicles that have only closed trips
        self.fields['vehicle'].queryset = Vehicle.objects.filter(
            ~Q(trip__status='Open') | Q(trip__isnull=True)).distinct()
        # Get all drivers that have only closed trips
        self.fields['driver'].queryset = Driver.objects.filter(
            ~Q(trip__status='Open') | Q(trip__isnull=True)).distinct()




class DetailTripForm(forms.ModelForm):
    class Meta:
        fields=['task_type','description']
        widgets = { 
            'owner':forms.TextInput(attrs={'disabled':True}),
            'task_type': forms.Select(attrs={'disabled':True}),
            'description': forms.Textarea(attrs={'rows':'4','disabled':True}),
        }
        
        
class TripFilterForm(forms.Form):
    driver_name = forms.ModelChoiceField(queryset=Driver.objects.all(), empty_label='Select Driver', required=False)
    from_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))

    def filter_trips(self):
        driver_name = self.cleaned_data.get('driver_name')
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')

        trips = Trip.objects.all()

        if driver_name:
            trips = trips.filter(driver=driver_name)

        if from_date and to_date:
            trips = trips.filter(created_at__range=[from_date, to_date])

        return trips