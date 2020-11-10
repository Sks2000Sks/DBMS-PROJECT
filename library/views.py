from django.shortcuts import render
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from datetime import datetime,timedelta,date
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def staffclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/staffclick.html')


def staffsignup_view(request):
    form1=forms.StaffForm()
    mydict={'form1':form1}
    if request.method=='POST':
        form1=forms.StaffForm(request.POST)
        if form1.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
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
            f3.userid=user
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
            f2.isbn=u1.isbn
            f3.isbn=u1.isbn
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
            obj=models.IssuedTo()
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
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.Reader.objects.filter(userid=ib.user.id))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].userid,books[i].title,books[i].isbn,issdate,expdate,fine)
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
    student=models.Reader.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedTo.objects.filter(isbn=student[0].userid)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].userid,student[0].dept,book.title,book.isbn)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
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
