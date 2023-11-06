from django.contrib.auth.models import User
from django.db.models import *


class Department(Model):
    id=AutoField(primary_key=True,editable=False)
    department = CharField(max_length=50,null=True)
    def __str__(self):
        return self.department
    
class Job_title(Model):
    id=AutoField(primary_key=True,editable=False)
    title=CharField(max_length=50,null=True)
    department = ForeignKey(Department,on_delete=SET_NULL,null=True)
    def __str__(self):
        return self.title

class Task_type(Model):
    id=AutoField(primary_key=True,editable=False)
    job_title=ForeignKey(Job_title,on_delete=CASCADE,null=True)
    type = CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.type
    
class Employee(Model):
    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    job_title = ForeignKey(Job_title,on_delete=SET_NULL,null=True)


    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name


class Report(Model):
    STATUS_CHOICES= (
    ('On Hold', 'On Hold'),
    ('In Progress', 'In Progress'),
    ('Not Started', 'Not Started'),
    ('Done', 'Done'),
    )
    id=AutoField(primary_key=True,editable=False)
    owner = ForeignKey(Employee,on_delete=SET_NULL,null=True)
    task=TextField(null=True)
    created_at=DateTimeField(auto_now_add=True)
    status=CharField(max_length=50,choices=STATUS_CHOICES,default='On Hold')
    remarks=TextField(null=True)


    def __str__(self):
        return str(self.owner)

    # class Meta:
    #     permissions=[('can_view_submitted_reports','Can View Submitted Reports'),('can_view_journalists_profiles','Can View Journalists Profiles'),(('can_view_all','Can View Journalists ALL'))]
