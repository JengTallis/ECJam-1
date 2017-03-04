from django.conf.urls import url
from .views import viewHistory, submitPicture, alert

urlpatterns = [
    url(r"post", submitPicture, name="submitPicture"),
    url(r"confused", viewHistory, name="viewHistory"),
    url(r"alert", alert, name="alert")
#    url(r"postAttendance", submitAttendance, name="submitAttendance"),
#    url(r"attendance", viewAttendance, name="viewAttendance"),
#    url(r"add", addUser, name="addUser")
]
