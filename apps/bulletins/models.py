from django.contrib.auth.models import User
from django.db import models
from django.db.models import *


class Producer(models.Model):

    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    
    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name

class PA(models.Model):

    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name

class Director(models.Model):

    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name

class Editor(models.Model):

    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name

class Anchor(models.Model):

    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name
    
    

class Bulletin(models.Model):
    TYPE_CHOICES = (
        ('Mojaz', 'Mojaz'),
        ('Nashra', 'Nashra'),
    )
    TIME_CHOICES = (
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('20', '20'),
      
    )

    type = models.CharField(max_length=50, choices=TYPE_CHOICES,default='Mojaz')
    time = models.CharField(max_length=50, choices=TIME_CHOICES,default='14')
    created_at=models.DateTimeField(auto_now_add=True)
    resources = models.TextField(null=True)
    editors = models.ManyToManyField(Editor)
    producers = models.ManyToManyField(Producer)
    
