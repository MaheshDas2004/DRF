from django.shortcuts import render
from django.http import JsonResponse
from students.models import Students
from . serializers import StudentSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
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





