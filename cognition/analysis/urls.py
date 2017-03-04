from django.conf.urls import url
from .views import viewHistory, submitPicture, submitAttendance, viewAttendance, addUser

urlpatterns = [
    url(r"post", submitPicture, name="submitPicture"),
    url(r"confused", viewHistory, name="viewHistory"),
    url(r"postAttendance", submitAttendance, name="submitAttendance"),
    url(r"attendance", viewAttendance, name="viewAttendance"),
    url(r"add", addUser, name="addUser")
]
