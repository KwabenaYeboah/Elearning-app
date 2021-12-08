from django.urls import path

from .views import (CourseListView, CourseCreateView, 
                    CourseUpdateView, CourseDeleteView,
                    CourseModuleUpdateView)

urlpatterns = [
    path('your-courses/', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<pk>/module/', CourseModuleUpdateView.as_view(), name='course_module_update'),
    
]
