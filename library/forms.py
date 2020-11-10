from django import forms
from django.contrib.auth.models import User
from . import models
#d
class ReaderUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','password']
#d
class ReaderForm(forms.ModelForm):
    class Meta:
        model=models.Reader
        fields=['isfaculty','dept']
#d
class Reader_PnoForm(forms.ModelForm):
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
        fields='__all__'

#d
class StaffForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','password']

class KeepsTrackForm(forms.ModelForm):
    class Meta:
        model=models.KeepsTrack
        fields='__all__'
        
class PublishedByForm(forms.ModelForm):
    class Meta:
        model=models.PublishedBy
        fields='__all__'

class MaintainsForm(forms.ModelForm):
    class Meta:
        model=models.Maintains
        fields='__all__'

class IssuedToForm(forms.ModelForm):
    class Meta:
        model=models.IssuedTo
        fields='__all__'

