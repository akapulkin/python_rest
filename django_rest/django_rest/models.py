from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name='Birthdate')
    # department = models.ForeignKey('Department', on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

#
# class Department(models.Model):
#     head_of_department = models.ForeignKey(Employee, on_delete=models.SET_NULL)
#     name = models.CharField(max_length=256, verbose_name='Name of department')
#
#     def __str__(self):
#         return self.name
