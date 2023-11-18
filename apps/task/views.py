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
    

    if department_id :
        try:
            filtered_employees = Employee.objects.filter(department_id=department_id).values('id', 'user__first_name', 'user__last_name')
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
        form = CreateTaskForm()
        if Group.objects.filter(name='Admin').exists() and request.user.groups.filter(name='Admin').exists():
            form.fields['remarks'].disabled = 'disabled'
        else:
            form.fields['reviews'].disabled = 'disabled'
        department = get_object_or_404 (Department,employee__user=self.request.user)
        print(department)
        roles = Role.objects.all()

        context = {
            'form':form,
            'department': department,
            'roles': roles,
        }
        return render(request, self.template_name, context)



    def post(self, request):
        form = CreateTaskForm(request.POST)
        current_employee = get_object_or_404(Employee, user=request.user)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)
        
        data = form.save(commit=False)
        data.owner_id = Employee.objects.get(user=self.request.user).id
    
        # Retrieve other POST data
        department = request.POST.get('department')
        role = request.POST.get('role')
        assigned_to = request.POST.getlist('assigned_to')
        
        # Update 'data' with additional form fields and POST data
        if Group.objects.filter(name='User').exists() and request.user.groups.filter(name='User').exists():
            assigned_to = [current_employee]

            data.department_id = department
            data.role_id = role
            data.category_id =role


            
        data.department = current_employee.department
        data.save()
        data.assigned_to.add(*assigned_to)
        # Assign selected employees to the task
        return redirect(self.success_url)




    

class TaskListView(LoginRequiredMixin, View):
    template_name = 'task/task_list.html'
    paginate_by = 5


    def get(self, request):
        employee = Employee.objects.get(user=self.request.user)
        strval = request.GET.get("search", False)
        
        if request.user.is_authenticated:
            if strval:
                query = Q(remarks__icontains=strval)
                query.add(Q(owner__user__first_name__icontains=strval), Q.OR)
                query.add(Q(owner__user__last_name__icontains=strval), Q.OR)
                query.add(Q(owner__user=self.request.user), Q.AND)
                task_list = Task.objects.filter(query).select_related().order_by('-created_date')
            else:
                # Check if the user is in the admin group
                if Group.objects.filter(name='Admin').exists() and request.user.groups.filter(name='Admin').exists():
                    # If admin, display all tasks in the department
                    task_list = Task.objects.filter(owner__department=employee.department).order_by('-created_date')
                else:
                    # If not admin, display tasks based on ownership or assignment
                    task_list = Task.objects.filter(
                        Q(owner__user=self.request.user) | Q(assigned_to=employee)
                    ).order_by('-created_date').distinct()
                
                
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the task instance being updated
        task = self.get_object()

        # Get the department and role associated with the task
        department = task.owner.department
        role = task.category

        # Add extra context
        context['roles'] = Role.objects.all()
        context['department'] = department
        context['selected_role'] = role

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Edit the attributes of the widgets
        if Group.objects.filter(name='Admin').exists() and self.request.user.groups.filter(name='Admin').exists():
            form.fields['remarks'].disabled = 'disabled'
        else:
            form.fields['reviews'].disabled = 'disabled'

        return form
    
    
   
    
class DashboardView(View):
    template_name = 'task/main.html'

    def get_context_data(self):
        # Fetch data for your dashboard
        user = self.request.user
        is_admin = user.groups.filter(name='Admin').exists()
        last_month_start = timezone.now() - timedelta(days=30)
        last_week_start = timezone.now() - timedelta(weeks=1)
        team_members = Employee.objects.filter(department=user.employee.department).exclude(id=user.id)
        employee = Employee.objects.get(user=self.request.user)
        last_assigned_tasks = Task.objects.filter(
                Q(assigned_to=employee ) & Q(created_date__gte=last_week_start)
        ).order_by('-created_date').distinct()
        if is_admin:
            # User is in admin group, can see all stats
            
            total_tasks = Task.objects.filter(created_date__gte=last_month_start).count()
            completed_tasks = Task.objects.filter(status='Done', created_date__gte=last_month_start).count()
            inprogress_tasks = Task.objects.filter(status='In Progress', created_date__gte=last_month_start).count()
            in_progress = Task.objects.filter(status='In Progress')

        else:
            # User is a normal user, can only see their own stats
            q=(Q(assigned_to=employee ) | Q(owner__user=user)) & Q(created_date__gte=last_month_start)
            total_tasks = Task.objects.filter(q).count()
            completed_tasks = Task.objects.filter(Q(status = 'Done') & q ).count()
            inprogress_tasks = Task.objects.filter(Q(status = 'In Progress') & q).count()
            in_progress = Task.objects.filter(status='In Progress', owner__user=user)



 
        
        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'inprogress_tasks': inprogress_tasks,
            'in_progress': in_progress,
            'team_members':team_members,
            'last_assigned':last_assigned_tasks,
            # Add more data as needed
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
