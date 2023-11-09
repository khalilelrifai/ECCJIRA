from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import *

from .forms import *
from .models import *


def get_filtered_employees(request):
    department_id = request.GET.get('department')
    role_id = request.GET.get('role')

    if department_id and role_id:
        try:
            filtered_employees = Employee.objects.filter(department_id=department_id, role_id=role_id).values('id', 'user__first_name', 'user__last_name')
            # Filter the employees based on the department and role

            employees_list = list(filtered_employees)
            return JsonResponse(employees_list, safe=False)
        except Employee.DoesNotExist:
            return JsonResponse([], safe=False)
    else:
        return JsonResponse([], safe=False)


class CreateTask(LoginRequiredMixin,View):
    success_url = reverse_lazy('task:main')
    template_name = 'task/task_form.html'

    def get(self, request):
        form = CreateTaskForm
        departments = Department.objects.all()
        roles = Role.objects.all()

        context = {
            'form':form,
            'departments': departments,
            'roles': roles,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateTaskForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.owner_id = Employee.objects.get(user=self.request.user).id
        
            # Retrieve other POST data
            department = request.POST.get('department')
            role = request.POST.get('role')
            assigned_to = request.POST.getlist('assigned_to')
            
            # Update 'data' with additional form fields and POST data
            data.department_id = department
            data.role_id = role
            data.category_id =role

            data.save()
            data.assigned_to.add(*assigned_to)
            # Assign selected employees to the task
            return redirect(self.success_url)

        context = {'form': form}
        return render(request, self.template_name, context)




    

class TaskListView(LoginRequiredMixin, View):
    template_name = 'task/task_list.html'
    paginate_by = 10


    def get(self, request):
        department = Department.objects.all().values_list('department', flat=True)
        strval = request.GET.get("search", False)
        
        if request.user.is_authenticated:
            if strval:
                query = Q(remarks__icontains=strval)
                query.add(Q(owner__user__first_name__icontains=strval), Q.OR)
                query.add(Q(owner__user__last_name__icontains=strval), Q.OR)
                query.add(Q(owner__user=self.request.user), Q.AND)
                task_list = Task.objects.filter(query).select_related().order_by('-created_date')
            else:
                task_list = Task.objects.filter(owner__user=self.request.user).order_by('-created_date')
                
            paginator = Paginator(task_list, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {

                'page_obj':page_obj,
                'search': strval,
            }

            return render(request, self.template_name, context)


class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('task:list')


class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    template_name= "task/task_detail.html"
    
    # def get_context_data(self, **kwargs) :
    #     context = super().get_context_data(**kwargs)
    #     context['group'] = User.objects.filter(groups__name__contains='admin')
    #     return context
     

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy('task:list')
    template_name = 'task/task_form.html'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     x = get_object_or_404 (Job_title,employee__user=self.request.user)
    #     context['job_title'] = x
    #     context['department'] = x.department
    #     context['form'].fields['task_type'].queryset = Task_type.objects.filter(job_title_id=x.id)
    #     return context


# class ReportDeleteView(LoginRequiredMixin,DeleteView):
#     model = Report
#     success_url = reverse_lazy('reports:list')
    
    
class DirectorView(LoginRequiredMixin, View):
    paginate_by = 10
    template_name = 'task/director_list.html'

    def get(self, request):
        search_value = request.GET.get('search')
 
        form = SearchFilterForm(request.GET or None)
        form.fields['search'].initial = search_value
        x = get_object_or_404(Job_title, employee__user=self.request.user)
        
        if form.is_valid():
            task_list = form.filter_task().exclude(owner__user=request.user)
            task_list = task_list.filter(task_type__job_title=x)
        else:
            task_list = Task.objects.filter(task_type__job_title=x).exclude(owner__user=request.user).order_by('-created_at')
        
        
        
        paginator = Paginator(task_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'form': form,
            
        }
        

        return render(request, self.template_name, context)

        
           
        
# class HRView(LoginRequiredMixin, View):
#     template_name = 'reports/hr.html'
#     paginate_by = 10
#     def get(self, request):
#         form = ReportFilterForm(request.GET or None)
#         department = Department.objects.all().values_list('department', flat=True)
#         report_list = Report.objects.filter(status='Approved').order_by('-created_at')

#         if form.is_valid():
#             report_list = form.filter_reports()
            
#         paginator = Paginator(report_list, self.paginate_by)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
        

#         context = {'form': form, 'page_obj': page_obj, 'department': department}
#         return render(request, self.template_name, context)
    
# class ProfileView(LoginRequiredMixin,ListView):
#     model=Report
#     template_name='reports/profile.html'
    

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get('pk')
#         reports=Report.objects.filter(owner_id=pk).order_by('-created_at')
        
#       # Retrieve last week's records
#         last_week_start = timezone.now() - timedelta(weeks=1)
#         last_week_reports = Report.objects.filter(owner_id=pk, created_at__gte=last_week_start).count()
#         context['week'] = last_week_reports

#         # Retrieve last month's records
#         last_month_start = timezone.now() - timedelta(days=30)
#         last_month_reports = Report.objects.filter(owner_id=pk, created_at__gte=last_month_start).count()
#         context['month'] = last_month_reports

#         # Retrieve today's records
#         today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
#         today_reports = Report.objects.filter(owner_id=pk, created_at__gte=today_start).count()
#         context['today'] = today_reports
#         context['report_list']=reports
#         context['name'] = reports.first().owner.fullname if reports.exists() else None
#         return context
        
 

# def approve(request,pk):
#     Report.objects.filter(id=pk).update(status='Approved')
#     return redirect('reports:director')
    

    
    
    
