from django.shortcuts import render,redirect
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from datetime import datetime,timedelta,date
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
import os
import face_recognition
import cv2 
import numpy



""" def facedect(loc):
        cam = cv2.VideoCapture(0)   
        s, img = cam.read()
        if s:    
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'pages')
                loc=(str(MEDIA_ROOT)+loc)
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
                print(check)
                if check[0]:
                        return True
                else :
                        return False    
 """
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')




def staffclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/staffclick.html')


def staffsignup_view(request):
    form1=forms.StaffUserForm()
    form2=forms.StaffForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StaffUserForm(request.POST)
        form2=forms.StaffForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('stafflogin')
    return render(request,'library/staffsignup.html',context=mydict)


def studentsignup_view(request):
    form1=forms.ReaderUserForm()
    form2=forms.ReaderForm()
    form3=forms.Reader_PnoForm()
    mydict={'form1':form1,'form2':form2,'form3':form3}
    if request.method=='POST':
        form1=forms.ReaderUserForm(request.POST)
        form2=forms.ReaderForm(request.POST)
        form3=forms.Reader_PnoForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            f2.save()
            f3=form3.save(commit=False)
            f3.userid=f2
            f3.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)

def is_staff(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_staff(request.user):
        return render(request,'library/staffafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')

def stafflogin(request):
    if request.method =="POST":
                form =forms.LoginForm(request.POST)
                if form.is_valid():
                        username=request.POST['username']
                        password=request.POST['password']
                        user = authenticate(request,username=username,password=password)
                        if user is not None:
                                """  face=models.Staff.objects.get(user_id=user.id)
                                if facedect(face.head_shot.url): """
                                login(request,user)
                                messages.success(request, "Successfully Logged In")
                                return redirect('afterlogin')
                        else:
                                messages.error(request, "Invalid credentials! Please try again")
                                return render(request,'library/loginfail.html')       
                return render(request,'library/loginfail.html')
    else:
                form = forms.LoginForm()
                return render(request,"library/stafflogin.html",{"form": form})  

""" def loginfail(request):
    return render(request,'loginfail.html',{}) """

def studentlogin(request):
    if request.method =="POST":
                form =forms.LoginForm(request.POST)
                if form.is_valid():
                        username=request.POST['username']
                        password=request.POST['password']
                        user = authenticate(username=username,password=password)
                        if user is not None:
                            """ face=models.Reader.objects.get(user_id=user.id)
                            if facedect(face.head_shot.url): """
                            login(request,user)
                            messages.success(request, "Successfully Logged In")
                            return redirect('afterlogin')
                        else:
                                messages.error(request, "Invalid credentials! Please try again")
                                return redirect('library/loginfail.html')    
                return redirect('library/loginfail.html')    
    else:
                form = forms.LoginForm()
                return render(request,"library/studentlogin.html",{"form": form}) 


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def addbook_view(request):
    form1=forms.BookForm()
    form2=forms.Book_AuthorForm()
    form3=forms.Book_CategoryForm()
    mydict={'form1':form1,'form2':form2,'form3':form3}
    if request.method=='POST':
        form1=forms.BookForm(request.POST)
        form2=forms.Book_AuthorForm(request.POST)
        form3=forms.Book_CategoryForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            u1=form1.save()
            f2=form2.save(commit=False)
            f3=form3.save(commit=False)
            f2.isbn=u1
            f3.isbn=u1
            u1.save()
            f2.save()
            f3.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',context=mydict)

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def viewbook_view(request):
    book1=models.Book.objects.all()
    book2=models.Book_Author.objects.all()
    book3=models.Book_Category.objects.all()
    mydict={'book1':book1,'book2':book2,'book3':book3}
    return render(request,'library/viewbook.html',context=mydict)

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def issuebook_view(request):
    form=forms.IssuedToForm()
    if request.method=='POST':
        form=forms.IssuedToForm(request.POST)
        if form.is_valid():
            obj=form.save()
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedTo.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.returndate.day)+'-'+str(ib.returndate.month)+'-'+str(ib.returndate.year)
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        books=list(models.Book.objects.filter(isbn=ib.isbn.isbn))
        students=list(models.Reader.objects.filter(user_id=ib.userid.id))
        i=0
        for i in books:
            t=(students[i].get_name,students[i].getuserid,books[i].title,books[i].isbn,issdate,expdate,fine)
            i=i+1
            li.append(t)
    return render(request,'library/viewissuedbook.html',{'li':li})



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def viewstudent_view(request):
    students=models.Reader.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    #student=models.Reader.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedTo.objects.filter(userid=request.user.id)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user.username,book.title,book.isbn)
            li1.append(t)
        
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.returndate.day)+'-'+str(ib.returndate.month)+'-'+str(ib.returndate.year)
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)
    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})
