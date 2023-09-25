from django.db import models

# Create your models here.
class Info(models.Model):
    #title
    name = models.TextField()
    professionalType = models.TextField()
    attitudeType = models.TextField()
    isVerify = models.TextField()
    hospital = models.TextField()
    position = models.TextField()
    department = models.TextField()
    province = models.TextField()
    city = models.TextField()
    address = models.TextField()
    longtitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    avatarUrl = models.TextField()
    contacts = models.TextField()
    comments = models.TextField()
    source = models.TextField() 
    status = models.TextField(default='active')


    experience = models.TextField(null=True)
    info = models.TextField(null=True)
    nickname = models.TextField(null=True)
    contact = models.TextField(null=True)
    # status: 
    #   active = will show
    #   pending = won't show, waiting for verification
    #   deleted = won't show

    def __str__(self):
        #return the task title
        return self.name