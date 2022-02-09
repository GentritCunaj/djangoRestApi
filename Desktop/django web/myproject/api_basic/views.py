
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Task
from .serializers import TaskSerializer
import datetime
from .form import TaskForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer

# Create your views here.
@api_view(['GET','POST'])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT',"DELETE"])
def task_detail(request,pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def today_func(request):
     # filter objects created today
    if request.method == "GET":
        tasks = Task.objects.all()
        today_var = datetime.date.today()  # date representing today's date
        qs = Task.objects.filter(date__gt= today_var)
        serializer = TaskSerializer(instance=qs,many=True)

        template_name = "report.html"
        return render(request,template_name,{"profiles":serializer.data})


    elif request.method == "POST":

        today_var = datetime.date.today()
        qs = Task.objects.filter(date__gt= today_var)
        serializer = TaskSerializer(instance=qs, many=True)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def all_tasks(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,many=True)
        context = {"context":serializer.data}
        return render(request,"home.html",context)



def createTask(request):
    form = TaskForm()
    if request.method == "POST":

        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/task")

    context = {"form":form}
    return render(request,'create.html',context)


def updateTask(request,pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect("/task")
    context = {"form":form}
    return render(request,'update.html',context)