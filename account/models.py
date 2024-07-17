from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.timesince import timesince
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    GENDER_TYPES = (
        ("woman", 'женщина'),
        ("man", 'мужчина'),
    )
    bio = models.TextField('Описание', max_length=500, blank=True, null=True)
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)
    gender = models.CharField("Пол", choices=GENDER_TYPES, max_length=10, default='man')
    tel = models.CharField('Телефон', max_length=12, blank=True, null=True)
    

    def __str__(self):
        return f'{self.username}: {self.first_name} - {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


