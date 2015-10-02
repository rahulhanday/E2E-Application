from django.db import models
from django.contrib.auth.models import User


class Details(models.Model):
    '''
        User details model
    '''
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50)
    user = models.OneToOneField(User)

    class Meta:
        ordering = ['user']
        verbose_name_plural = "Details"


class GlobalConfig(models.Model):

    """
        global configuration table
    """

    name = models.CharField(max_length=10, default="token_exp")
    value = models.TextField(default="60")

    class Meta:
        verbose_name_plural = "Global Config"
