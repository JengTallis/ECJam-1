from django.db import models
# Create your models here.


class Record(models.Model):

    time = models.TimeField(auto_now_add=True)
    value = models.IntegerField()

    @staticmethod
    def getAllRecords():
        result = [(r.value, r.time) for r in Record.objects.all()]
        return result
