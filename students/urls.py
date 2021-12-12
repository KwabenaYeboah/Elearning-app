from django.urls import path

from .views import (StudentSignUpView, StudentEnrollCourseView,
                    StudentCourseListView, StudentCourseDetailView,)

urlpatterns = [
    path('signup/', StudentSignUpView.as_view(), name='student_signup'),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/detail/<pk>/', StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/detail/<pk>/<module_id>/', StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),
]
