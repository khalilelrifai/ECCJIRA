

from django.contrib import admin

from .models import Department, Employee, Role, Task




admin.site.register(Task)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Role)

