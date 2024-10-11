from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.EmployeeView.as_view(), name='employee-list-create'),
    path('admins/', views.AdminView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', views.EmployeeView.as_view(), name='employee-retrieve-update-delete'),
    path('tasks/', views.TaskView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskView.as_view(), name='task-retrieve-update-delete'),
    path('plots/', views.PlotView.as_view(), name='plot-list-create'),
    path('plots/<int:pk>/', views.PlotView.as_view(), name='plot-retrieve-update-delete'),
    path('items/', views.ItemView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', views.ItemView.as_view(), name='item-retrieve-update-delete'),
    path('employee-tasks/', views.EmployeeTaskView.as_view(), name='employee-task'),
    path('employee-tasks/<int:pk>/', views.EmployeeTaskView.as_view(), name='employee-task-id'),
    path('timer/', views.TaskHandlerView.as_view(), name="time-handler"),
    path('choose-task/', views.choose_task, name="choose_task"),
    path('login/', views.sign_in, name="login"),
    path('generate-report/', views.generate_report, name="generate-report")
]
