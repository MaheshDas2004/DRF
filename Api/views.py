from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from students.models import Students
from . serializers import StudentSerializers, EmployeeSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from Employees.models import Employee
from django.http import Http404
from rest_framework import mixins,generics,viewsets

from Blogs.serializers import BlogSerializer,CommentSerializer
from Blogs.models import Blog,Comment

from . paginations import CustomPagination
# Create your views here.
# Function Based views
@api_view(['GET','POST'])
def studentsView(request):
    # Manual serilization: Taking the query set and converting it into a list is not recommended, thats where serializers come for complex data to convert it into json and xml readable format
    
    # students=Students.objects.all()
    # students_list=list(students.values())
    # return JsonResponse(students_list,safe=False)

    # Reading all users (showing all the users present in database)
    if request.method=="GET":
        students=Students.objects.all()
        serializer=StudentSerializers(students,many=True)#here data is students 
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # Creating a new user 
    elif request.method=='POST':
        serializer=StudentSerializers(data=request.data)#accepting the incoming data through request.data which creates a new data
        if serializer.is_valid():#checking if its valid or not
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def single_studentsView(request,id):
    try:
        student=Students.objects.get(id=id)
    except Students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Showing data of a single user
    if request.method=='GET':
        serializer=StudentSerializers(student)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # Updating the user 
    elif request.method=='PUT':
        serializer= StudentSerializers(student,data=request.data)#takes existing student and updates with new data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# API Creation manually without mixins
"""
class Employees(APIView):
    def get(self,request):
        employees=Employee.objects.all()
        serializer=EmployeeSerializers(employees,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=EmployeeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Single_Employee(APIView):
    def get_employee(self,id):
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            raise Http404
    def get(self,request,id):
        employee=self.get_employee(id)
        serializer=EmployeeSerializers(employee)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,requset,id):
        employee=self.get_employee(id)
        serializer=EmployeeSerializers(employee,data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,requset,id):
        employee=self.get_employee(id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


# Using mixins:"Mixins DRF me chhoti-chhoti ready-made classes hoti hain jo GET, POST, PUT, DELETE jaise kaam asaani se karne deti hain bina pura code likhe."Ye tumhare views me CRUD functionality add karte hain reusability aur simplicity ke liye."
"""
class Employees(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    #variables ka name by default hota ha cant change the name
    queryset=Employee.objects.all()
    serializer_class= EmployeeSerializers

    def get(self,request):
        return self.list(request)
    
    def post(self,requset):
        return self.create(requset)
    
class Single_Employee(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class= EmployeeSerializers

    def get(self,request,pk):# yahan pr pk hi by default use hoga manual apis me ham koi bhi naam daal skte ha but mixins me by default pk use krna padta ha
        return self.retrieve(request,pk)
    
    def put(self,requset,pk):
        return self.update(requset,pk)
    
    def delete(self,request,pk):
        return self.destroy(request,pk)
"""


# using Genrics :"Django REST Framework ke generics ready-made views hote hain jo common CRUD operations ke liye code aur short kar dete hain."Inme sab kuch built-in hota hai — tumhe sirf queryset aur serializer_class dena hota hai.

# can use "generics.ListCreateAPIView" for implementing create and update all at once
"""
class Employees(generics.CreateAPIView,generics.ListAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializers

# can use combination of 3 api views instead of using 3,  "generics.RetrieveUpdateDestroyAPIView"
class Single_Employee(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializers
    lookup_field='pk'
"""


# Using viewsets:"ViewSet ek DRF class hai jo ek hi jagah se multiple actions (GET, POST, PUT, DELETE) handle kar leta hai.""Ye routing ke liye routers ka use karta hai, jisse tumhara URL config bhi automatic ho jaata hai."
"""
class EmployeeViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset=Employee.objects.all()
        serializer=EmployeeSerializers(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer=EmployeeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        serializer=EmployeeSerializers(employee)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def update(self,request,pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        serializer=EmployeeSerializers(employee,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializers
    pagination_class=CustomPagination

class BlogsView(generics.ListCreateAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer

class CommentsView(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer

class DetailedBlogsView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    lookup_field='pk'

class DetailedCommentsView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='pk'






