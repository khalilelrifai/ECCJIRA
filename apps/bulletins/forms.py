from django import forms
from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView

from .models import *


class BulletinForm(forms.ModelForm):
    
    class Meta:
        model = Bulletin
        fields =('type','time','editors','resources','producers')
