from django.contrib import admin
from .models import *

class notes_admin(admin.ModelAdmin):
    list_display = ('user','title','discription')

class homework_admin(admin.ModelAdmin):
    list_display = ('user','subject','title','description','due','is_finished')

class todo_admin(admin.ModelAdmin):
    list_display = ('user','title','is_finished')

admin.site.register(Notes,notes_admin)
admin.site.register(Homework,homework_admin)
admin.site.register(Todo,todo_admin)
# Register your models here.





