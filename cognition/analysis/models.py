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
    UID = models.TextField()
    name = models.TextField()

    @staticmethod
    def addUser(ID, name):
        user = User()
        user.UID = ID
        user.name = name
        user.save()

    @staticmethod
    def getAllUsers():
        result = {u.UID: u for u in User.objects.all()}

    def getName(self):
        return self.name


class Attendance(models.Model):
    completed = models.BooleanField()
    timestamp = models.TextField()
    users = models.ManyToManyField(User)

    @staticmethod
    def getAllAttendances():
        return [r.timestamp for r in Attendance.objects.all()]

    @staticmethod
    def getByTimestamp(i):
        return Attendance.objects.get(timestamp=i)

    def complete(self):
        self.completed = True
        self.save()

    def getTakenStudents(self):
        return [u.getName() for u in self.users_set.all()]

    def getUntakenStudents(self):
        untakens = User.objects.all() - self.users_set.all()
        result = [u.getName() for u in untakens]
        return result

    def addStudent(self, s):
        self.users_set.add(s)
        self.save()

    def hasTaken(self, user):
        return user in self.users_set.all()

    def hasCompleted(self):
        return self.completed


class Group(models.Model):
    groupID = models.TextField()

    def getID(self):
        return self.groupID
