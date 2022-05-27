from django.contrib import admin
from .models import Training, Exercise, UserExercises


class  TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date',)



admin.site.register(Training, TrainingAdmin)
admin.site.register(Exercise)
admin.site.register(UserExercises)
# Register your models here.
