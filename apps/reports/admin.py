

from django.contrib import admin

from .models import Department, Employee, Job_title, Report, Task_type


class RAdmin(admin.ModelAdmin):

    list_display =['id','owner','task_type','created_at']

admin.site.register(Report,RAdmin)
admin.site.register(Employee)
admin.site.register(Task_type)
admin.site.register(Department)
admin.site.register(Job_title)

