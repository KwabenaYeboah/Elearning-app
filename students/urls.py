from django.urls import path

from .views import StudentSignUpView

urlpatterns = [
    path('signup/', StudentSignUpView.as_view(), name='student_signup'),
]
