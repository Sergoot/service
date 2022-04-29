from django.contrib import admin
from .models import Training, Exercise


class  TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date',)



admin.site.register(Training, TrainingAdmin)
admin.site.register(Exercise)
# Register your models here.
