from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Course
from .forms import ModuleFormSet

class UserMixin(object):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(instructor=self.request.user)

class UserEditMixin(object):
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

class UserCourseMixin(UserMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('course_list')

class UserCourseEditMixin(UserCourseMixin, UserEditMixin):
    template_name = 'courses/course_create_update.html'

class CourseListView(UserCourseMixin, ListView):
    template_name = 'courses/course_list.html'
    permission_required ='courses.view_course'
    context_object_name = 'courses'

class CourseCreateView(UserCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(UserCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(UserCourseMixin, DeleteView):
    template_name = 'courses/course_delete.html'
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/module_formset.html'
    course = None
    
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk,
                                        instructor=request.user)
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course, 
                                        'formset':formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('course_list')
        return self.render_to_response({'course':self.course, 
                                        'formset':formset})