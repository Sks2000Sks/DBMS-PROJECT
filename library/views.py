from django.shortcuts import render
from . import forms,models
from django.http import HttpResponseRedirect
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
    form2=forms.AuthenticateForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StaffForm(request.POST)
        form2=forms.StaffForm(request.POST)
        if form1.is_valid() and form2.is_valid:
            form1.save()
            form2.save()
            return HttpResponseRedirect('stafflogin')
    return render(request,'library/staffsignup.html',context=mydict)




def studentsignup_view(request):
    form1=forms.ReaderForm()
    form2=forms.Reader_PnoForm()
    form3=forms.AuthenticateForm()
    mydict={'form1':form1,'form2':form2,'form3':form3}
    if request.method=='POST':
        form1=forms.ReaderForm(request.POST)
        form2=forms.Reader_PnoForm(request.POST)
        form3=forms.AuthenticateForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            form3.save()


        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)


