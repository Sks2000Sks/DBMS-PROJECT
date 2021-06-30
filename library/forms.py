from django.forms import fields
from library.models import Review
from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

class ReaderUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),error_messages={'required': 'Enter a valid password of length more than 4'},min_length=4)
    '''def clean(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("The given username is already registered")
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise forms.ValidationError("Password length should not be less than 4 characters")
        return self.cleaned_data '''

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

class ReaderForm(forms.ModelForm):
    class Meta:
        model=models.Reader
        fields=['isfaculty','dept','head_shot']

class Reader_PnoForm(forms.ModelForm):
    pnumber = forms.CharField(min_length=10,max_length=10)
    def cleanaa(self):
        pnumber = self.cleaned_data['pnumber']
        if len(pnumber)!=10:
            raise forms.ValidationError("Invalid phone number Enter valid Phone Number")
        return self.cleaned_data
    class Meta:
        model=models.Reader_Pno
        fields=['pnumber']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields='__all__'

class Book_CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Book_Category
        fields=['category']
#
class Book_AuthorForm(forms.ModelForm):
    class Meta:
        model=models.Book_Author
        fields=['author']

class PublisherForm(forms.ModelForm):
    class Meta:
        model=models.Publisher
        fields=['pname','pid','year']

class PublishedByForm(forms.ModelForm):
    class Meta:
        model=models.PublishedBy
        fields=['isbn']

        
class StaffForm(forms.ModelForm):
    
    class Meta:
        model=models.Staff
        fields=['head_shot']

class StaffUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),error_messages={'required': 'Enter a valid password of length more than 4'},min_length=4)
    def cleana(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("The given username is already registered")
        password = self.cleaned_data.get('password')
        if len(password) < 4:
            raise forms.ValidationError("Password length should not be less than 4 characters")
        return self.cleaned_data



    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

class KeepsTrackForm(forms.ModelForm):
    class Meta:
        model=models.KeepsTrack
        fields='__all__'
        


class MaintainsForm(forms.ModelForm):
    class Meta:
        model=models.Maintains
        fields='__all__'

class IssuedToForm(forms.ModelForm):

    class Meta:
        model=models.IssuedTo
        fields='__all__'

class LoginForm(forms.Form):
   username = forms.CharField(max_length = 100,)
   password = forms.CharField(widget=forms.PasswordInput())

class ReviewForm(forms.ModelForm):

    def cleanb(self):
        if (models.Book.objects.filter(isbn=self.cleaned_data['isbn']).exists())!=True:
            raise forms.ValidationError("The given book does not exist in library")
        return self.cleaned_data


    class Meta:
        model = models.Review
        fields = [
            'isbn',
            'review'
        ]

