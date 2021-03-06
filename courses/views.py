from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms.models import modelform_factory
from django.apps import apps
from students.forms import CourseEnrollForm
from django.core.cache import cache

from .models import Course, Module, Content, Subject
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

class InstructorCourseListView(UserCourseMixin, ListView):
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

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/course_content_form.html'
    
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['instructor', 'order',
                                                 'created','updated'])
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id,
                                        course__instructor=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, 
                                         instructor=request.user)
        return super().dispatch(request, module_id, model_name, id)
    
    # Execute this method when dispatch receives a GET request
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form':form, 'object':self.obj})
    
    # Execute this method when dispatch receives a POST request
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form (self.model, instance=self.obj,
                              data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.instructor = request.user
            obj.save()
            if not id:
                # new module content should be created
                Content.objects.create(module=self.module, content=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form':form, 'object':self.obj})
    
class ContentDeleteView(View):
    def post(self, request, id):
        obj = get_object_or_404(Content, id=id,
                                    module__course__instructor=request.user)
        module = obj.module
        obj.content.delete()
        obj.delete()
        return redirect('module_content_list', module.id)
    
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/module_content_list.html'
    
    def get(self, request, module_id):
        module = get_object_or_404 (Module, id=module_id,
                                    course__instructor=request.user)
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__instructor=request.user).update(order=order)
        return self.render_json_response({'saved':'OK'})
    
class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__instructor=request.user).update(order=order)
        return self.render_json_response({'saved':'OK'})

class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/student_course_list.html'
    
    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:   
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
        all_courses = Course.objects.annotate(total_modules=Count('modules'))
        
        # Optionally query by subject
        if subject:
            subject =get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subjects':subjects, 'subject':subject, 'courses':courses})

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/student_course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        return context
    