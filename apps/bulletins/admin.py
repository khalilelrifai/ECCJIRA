from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Bulletin)
admin.site.register(Editor)
admin.site.register(Producer)
admin.site.register(Director)
admin.site.register(Anchor)
admin.site.register(PA)