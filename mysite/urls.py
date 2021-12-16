from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from courses.views import CourseListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('students.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', CourseListView.as_view(), name='all_course_list'),
    path('course/', include('courses.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('courses.api.urls')),
    path('forum/', include('forum.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)