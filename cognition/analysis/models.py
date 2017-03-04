from django.db import models
from django.utils import timezone
# Create your models here.


class Record(models.Model):

    time = models.DateTimeField(default=timezone.now)
    value = models.IntegerField()

    @staticmethod
    def getAllRecords():
        result = [(r.time.astimezone(), r.value)
                  for r in Record.objects.all()]
        return result
