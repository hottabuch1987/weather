from django.db import models
from account.models import User


class City(models.Model):
    name = models.CharField("Город", max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_count = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name + ' - ' + str(self.user) + ' - ' + str(self.search_count)


    class Meta:
        verbose_name = 'История поиска'
        verbose_name_plural = 'История поиска'
        ordering = ['-timestamp']