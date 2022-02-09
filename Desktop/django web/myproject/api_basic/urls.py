from django.urls import path
from .views import task_list,task_detail,today_func,all_tasks,createTask,updateTask

urlpatterns = [
    path('task/',task_list),
    path('detail/<int:pk>/',task_detail),
    path('today/',today_func),
    path('all_tasks/',all_tasks),
    path('createTask/',createTask),
    path('updateTask/<int:pk>',updateTask)

]