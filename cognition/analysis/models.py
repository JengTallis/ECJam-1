from django.db import models
from django.utils import timezone
from datetime import datetime
import pytz
# Create your models here.


class Record(models.Model):

    time = models.DateTimeField(default=timezone.now)
    value = models.IntegerField()
    _latest = None

    @staticmethod
    def getAllRecords():
        result = [(r.time.astimezone(), r.value)
                  for r in Record.objects.all()]
        return result

    @staticmethod
    def getRecords(begin, end):
        begin = Record._parse(begin)
        end = Record._parse(end, 2)
        print(begin, end)
        result = [(Record._format(r.time.astimezone()), r.value) for r in
                  Record.objects.filter(time__range=[begin, end])]
        return result

    @staticmethod
    def _format(date):
        return date.strftime("%Y-%m-%d") + "T" + date.strftime("%H:%M:%S")

    @staticmethod
    def _parse(s, add=0):
        date = s["date"]
        dates = date.split("-")
        hour = s["hour"]
        minute = s["minute"]
        tz = pytz.timezone("Asia/Hong_Kong")
        d = datetime(int(dates[0]), int(dates[1]),
                     int(dates[2]) + add, int(hour), int(minute), tzinfo=tz)
        d = d.astimezone(timezone.utc)
        return d

    @staticmethod
    def addRecord(value):
        r = Record()
        r.value = value
        r.save()
        _latest = r

    @staticmethod
    def getLatest():
        return _latest.value


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
