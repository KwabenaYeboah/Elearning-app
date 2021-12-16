from django.urls import path
from .views import course_forum

urlpatterns = [
    path('<int:course_id>/', course_forum, name='course_forum'),
]