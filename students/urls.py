from django.urls import path

from .views import StudentSignUpView, StudentEnrollCourseView

urlpatterns = [
    path('signup/', StudentSignUpView.as_view(), name='student_signup'),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
]
