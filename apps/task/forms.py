from django import forms

from .models import *
from django.contrib.auth.models import Group, Permission, User


from django import forms

class CreateTaskForm(forms.ModelForm):


    class Meta:
        model = Task
        fields = ['title', 'remarks', 'status', 'target_date', 'reviews', 'concern_company']
        widgets = {
            'title': forms.Textarea(attrs={'rows': '1','required':True}),
            'concern_company': forms.TextInput(attrs={'rows': '1'}),
            'remarks': forms.Textarea(attrs={'rows': '4'}),
            'reviews': forms.Textarea(attrs={'rows': '4'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        
        

        
class DetailTaskForm(forms.ModelForm):
    class Meta:
        fields=['task','remarks']
        widgets = { 
            'owner':forms.TextInput(attrs={'disabled':True}),
            'task': forms.Textarea(attrs={'rows':'2','disabled':True}),
            'remarks': forms.Textarea(attrs={'rows':'4','disabled':True}),
        }
        
        





# class TaskFilterForm(forms.Form):
#     department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department', required=False)
#     employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label='Select Employee', required=False)
#     job_title = forms.ModelChoiceField(queryset=Job_title.objects.all(), empty_label='Select Job Title', required=False)
#     search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search by text'}), required=False)

#     def filter_task(self):
#         department = self.cleaned_data.get('department')
#         employee = self.cleaned_data.get('employee')
#         job_title = self.cleaned_data.get('job_title')
#         search = self.cleaned_data.get('search')

#         task = Task.objects.all()

#         if department:
#             tasks = task.filter(owner__job_title__department=department)

#         if employee:
#             tasks = task.filter(owner=employee)

#         if job_title:
#             tasks = task.filter(owner__job_title=job_title)

#         if search:
#             tasks = task.filter(
#                 Q(remarks__icontains=search) |
#                 Q(owner__user__first_name__icontains=search) |
#                 Q(owner__user__last_name__icontains=search) 

#             )

#         reports = reports.filter(status='Approved').order_by('-created_at')

#         return reports
    
    


# class SearchFilterForm(forms.Form):
#     search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search by text'}), required=False)

#     def filter_reports(self):
#         search = self.cleaned_data.get('search')

#         reports = Report.objects.all()

#         if search:
#             reports = reports.filter(
#                 Q(remarks__icontains=search) |
#                 Q(owner__user__first_name__icontains=search) |
#                 Q(owner__user__last_name__icontains=search) 

#             )

#         reports = reports.order_by('-created_at')

#         return reports










#     # def __init__(self, *args, **kwargs):
#     #    user = kwargs.pop('user')
#     #    super(CreateReportForm, self).__init__(*args, **kwargs)
#     #    self.fields['task_type'].queryset = Task_type.objects.filter(user=user)
        
        
        




# # class DriverForm(forms.ModelForm):
# #     class Meta:
# #         model = Driver
# #         fields='__all__'
# #         widgets = { 
# #             'dob': forms.DateInput(attrs={'type':'date'}),
# #             'address':forms.Textarea(attrs={'rows':'4'}),
# #         }

# # class SecurityForm(forms.ModelForm):
# #     class Meta:
# #         model = Security
# #         fields='__all__'
# #         widgets = { 
# #             'dob': forms.DateInput(attrs={'type':'date'}),
# #             'address':forms.Textarea(attrs={'rows':'4'}),
# #         }
        
# # class AssetForm(forms.ModelForm):
# #     class Meta:
# #         model = Asset
# #         fields='__all__'
# #         widgets = { 
# #             'reg_date': forms.DateInput(attrs={'type':'date'}),
# #             'ren_date': forms.DateInput(attrs={'type':'date'})
# #         }
# #         labels = {
# #             'reg_date': ('Registeration Date'),
# #             'ren_date': ('Renewal Date'),
# #         }
        
        
# # class TripForm(forms.ModelForm):
# #     class Meta:
# #         model = Trip
# #         fields='__all__'
            
        
