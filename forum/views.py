from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def course_forum(request, course_id):
    try:
        # retrieve course with given id joined by the current user
        course = request.user.courses_enrolled.get(id=course_id)
    except:
        # user is not a student of the course or course does not exit
        return HttpResponseForbidden()
    return render(request, 'forum/course_forum.html', {'course':course})