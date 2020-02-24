from django.db import models
from django.contrib.auth.models import User

"""
Here I have defined an example class 'Mods'. Once the client is authenticated, it can request objects of 'Mods' class
and display it back on the client side.
"""


class Mods(models.Model):
    name = models.CharField(max_length=250)
    version = models.CharField(max_length=70)

    def __str__(self):
        return self.name + ' ' + self.version


class Subdivision(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Название подразделения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']


class Office(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Название офиса')
    address = models.CharField(max_length=150, db_index=True, verbose_name='Адрес офиса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Офис'
        verbose_name_plural = 'Офисы'
        ordering = ['name']


class JobPosition(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Название дожности')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, verbose_name='ФИО')
    phone_number = models.CharField(max_length=13, blank=True, verbose_name='Телефон')
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Подразделение')
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Офис')
    job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Должность')

    def __str__(self):
        return self.full_name

