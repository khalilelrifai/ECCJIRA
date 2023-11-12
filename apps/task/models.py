from django.contrib.auth.models import User
from django.db.models import *


class Department(Model):
    id=AutoField(primary_key=True,editable=False)
    department = CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.department
    
class Role(Model):
    id=AutoField(primary_key=True,editable=False)
    title=CharField(max_length=50,null=True)

    def __str__(self):
        return self.title

    
class Employee(Model):
    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    department = ForeignKey(Department,on_delete=SET_NULL,null=True)



    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name


class Task(Model):
    STATUS_CHOICES= (
    ('On Hold', 'On Hold'),
    ('In Progress', 'In Progress'),
    ('Not Started', 'Not Started'),
    ('Done', 'Done'),
    )
    id=AutoField(primary_key=True,editable=False)
    owner = ForeignKey(Employee,on_delete=SET_NULL,null=True)
    status=CharField(max_length=50,choices=STATUS_CHOICES,default='On Hold')
    title = CharField(max_length=200)
    created_date = DateTimeField(auto_now_add=True)
    target_date = DateField()
    remarks = TextField(blank=True)
    reviews = TextField(blank=True)
    category = ForeignKey(Role, on_delete=SET_NULL,null=True)
    assigned_to = ManyToManyField(Employee, related_name='tasks')
    concern_company = CharField(max_length=200)


    def __str__(self):
        return str(self.owner)

    # class Meta:
    #     permissions=[('can_view_submitted_reports','Can View Submitted Reports'),('can_view_journalists_profiles','Can View Journalists Profiles'),(('can_view_all','Can View Journalists ALL'))]
