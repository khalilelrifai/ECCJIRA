from django import forms

from .models import *


class CreateReportForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields=['task_type','description']
        
        widgets = { 
            # 'owner':TextInput(attrs={'disabled':True}),
            'task_type': forms.Select(attrs={}),
            'description': forms.Textarea(attrs={'rows':'4'}),
        }
        
        labels = {
            'owner': ('Name'),

        }
        
        
        
        
class DetailReportForm(forms.ModelForm):
    class Meta:
        fields=['task_type','description']
        widgets = { 
            'owner':forms.TextInput(attrs={'disabled':True}),
            'task_type': forms.Select(attrs={'disabled':True}),
            'description': forms.Textarea(attrs={'rows':'4','disabled':True}),
        }
        
        





class ReportFilterForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department', required=False)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label='Select Employee', required=False)
    job_title = forms.ModelChoiceField(queryset=Job_title.objects.all(), empty_label='Select Job Title', required=False)
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search by text'}), required=False)

    def filter_reports(self):
        department = self.cleaned_data.get('department')
        employee = self.cleaned_data.get('employee')
        job_title = self.cleaned_data.get('job_title')
        search = self.cleaned_data.get('search')

        reports = Report.objects.all()

        if department:
            reports = reports.filter(owner__job_title__department=department)

        if employee:
            reports = reports.filter(owner=employee)

        if job_title:
            reports = reports.filter(owner__job_title=job_title)

        if search:
            reports = reports.filter(
                Q(description__icontains=search) |
                Q(owner__user__first_name__icontains=search) |
                Q(owner__user__last_name__icontains=search) |
                Q(task_type__type__icontains=search)
            )

        reports = reports.filter(status='Approved').order_by('-created_at')

        return reports
    
    


class SearchFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search by text'}), required=False)

    def filter_reports(self):
        search = self.cleaned_data.get('search')

        reports = Report.objects.all()

        if search:
            reports = reports.filter(
                Q(description__icontains=search) |
                Q(owner__user__first_name__icontains=search) |
                Q(owner__user__last_name__icontains=search) |
                Q(task_type__type__icontains=search)
            )

        reports = reports.order_by('-created_at')

        return reports










    # def __init__(self, *args, **kwargs):
    #    user = kwargs.pop('user')
    #    super(CreateReportForm, self).__init__(*args, **kwargs)
    #    self.fields['task_type'].queryset = Task_type.objects.filter(user=user)
        
        
        




# class DriverForm(forms.ModelForm):
#     class Meta:
#         model = Driver
#         fields='__all__'
#         widgets = { 
#             'dob': forms.DateInput(attrs={'type':'date'}),
#             'address':forms.Textarea(attrs={'rows':'4'}),
#         }

# class SecurityForm(forms.ModelForm):
#     class Meta:
#         model = Security
#         fields='__all__'
#         widgets = { 
#             'dob': forms.DateInput(attrs={'type':'date'}),
#             'address':forms.Textarea(attrs={'rows':'4'}),
#         }
        
# class AssetForm(forms.ModelForm):
#     class Meta:
#         model = Asset
#         fields='__all__'
#         widgets = { 
#             'reg_date': forms.DateInput(attrs={'type':'date'}),
#             'ren_date': forms.DateInput(attrs={'type':'date'})
#         }
#         labels = {
#             'reg_date': ('Registeration Date'),
#             'ren_date': ('Renewal Date'),
#         }
        
        
# class TripForm(forms.ModelForm):
#     class Meta:
#         model = Trip
#         fields='__all__'
            
        
