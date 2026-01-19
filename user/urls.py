from django.urls import path
from .views import RegisterView
from .views import AdminFetchFaceData
from .views import AdminSignupView
from .views import LoginView
from .views import ImagePostAPIView
from .views import track_visitor


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('admin/fetch-face/', AdminFetchFaceData.as_view(), name='admin-fetch-face'),
    path('admin-register/', AdminSignupView.as_view(), name='admin-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('images/', ImagePostAPIView.as_view()),
    path('track-visitor/', track_visitor, name='track-visitor'),

]


 