from django.contrib import admin

from learningapp.models import DafLearned, StudyPlan

admin.site.register([StudyPlan, DafLearned])