from django.urls import path
from .views import FaceUserListCreateView

urlpatterns = [
    path('credentials/', FaceUserListCreateView.as_view(), name='faceuser-list-create'),
]
