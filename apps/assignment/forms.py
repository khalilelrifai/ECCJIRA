from django import forms
from .models import *


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description')
        
        
class DetailForm(forms.ModelForm):
    class Meta:
        
        fields=['owner','title', 'description','uploaded_at','ftp_exists','upload_status']
        widgets = { 
            'owner':forms.TextInput(attrs={'disabled':True}),
            'title':forms.TextInput(attrs={'disabled':True}),
            'uploaded_at':forms.TextInput(attrs={'disabled':True}),
            'description': forms.Textarea(attrs={'rows':'4','disabled':True}),
            'ftp_exists':forms.TextInput(attrs={'disabled':True}),
            'upload_status':forms.TextInput(attrs={'disabled':True}),
        }
        