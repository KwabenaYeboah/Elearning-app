from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (StudentSignUpView, StudentEnrollCourseView,
                    StudentCourseListView, StudentCourseDetailView,)

urlpatterns = [
    path('signup/', StudentSignUpView.as_view(), name='student_signup'),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/detail/<pk>/', cache_page(60 * 10) (StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/detail/<pk>/<module_id>/', cache_page(60 * 10) (StudentCourseDetailView.as_view()),
         name='student_course_detail_module'),
]
