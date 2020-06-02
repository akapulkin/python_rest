from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

STATUS_CHOICES = (('new', 'New'),
                  ('started', 'Started'),
                  ('done', 'Done'))


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name='Birthdate')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Department(models.Model):
    head_of_department = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                           related_name='head_of_department', null=True)
    name = models.CharField(max_length=256, verbose_name='Name of department', unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    project_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256, verbose_name='Project name', unique=True)
    start_date = models.DateField(verbose_name='Start date', null=True)
    end_date = models.DateField(verbose_name='End date', null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    executor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256, verbose_name='Task name')
    start_date = models.DateField(verbose_name='Start date', null=True)
    end_date = models.DateField(verbose_name='End date', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, verbose_name='Status')

    def __str__(self):
        return self.name


def task_post_save_receiver(sender, instance, *args, **kwargs):
    project = instance.project
    min_start_date_task = Task.objects.filter(project=project).order_by('start_date').first()
    max_end_date_task = Task.objects.filter(project=project).order_by('-end_date').first()
    project.start_date = min_start_date_task.start_date
    project.end_date = max_end_date_task.end_date
    project.save()


post_save.connect(task_post_save_receiver, sender=Task)
