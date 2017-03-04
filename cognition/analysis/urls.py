from django.conf.urls import url
from .views import viewHistory, submitPicture

urlpatterns = [
    url(r"post", submitPicture, name="submitPicture"),
    url(r"^$", viewHistory, name="viewHistory")
]