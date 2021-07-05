from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class DafLearned(models.Model):
    study_plan = models.ForeignKey('StudyPlan', on_delete=models.CASCADE, related_name='dafim')
    masechet_name = models.CharField(max_length=60)
    page_number = models.IntegerField()
    chazara = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)
    index_in_list_dafs = models.IntegerField()

    def __str__(self):
        return str(self.page_number) + " " + str(self.chazara)
    # isLearningPage1 = models.BooleanField()
    # isLearningPage2 = models.BooleanField()



class StudyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    typeOfStudy = models.CharField(max_length=30)
    wantChazara = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.typeOfStudy

