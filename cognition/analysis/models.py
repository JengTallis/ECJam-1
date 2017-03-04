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


class User(models.Model):
    image = models.ImageField()
    name = models.TextField()

    @staticmethod
    def addUser(image, name):
        user = User()
        user.image = image
        user.name = name
        user.save()

    @staticmethod
    def getAllUsers():
        result = {u.name: u.image for u in User.objects.all()}


class Attendance(models.Model):
    completed = models.BooleanField()
    timestamp = model.TextField()
    users = model.ManyToManyField(User)

    @staticmethod
    def getAllAttendance():
        return [r.timestamp for r in Attendance.objects.all()]

    @staticmethod
    def getByTimestamp(i):
        return Attendance.objects.get(timestamp=i)

    def complete(self):
        self.completed = True
        self.save()

    def getTakenStudents(self):
        return self.users_set.all()

    def addStudent(self, s):
        self.users_set.add(s)
        self.save()
