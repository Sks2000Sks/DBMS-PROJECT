from django import forms
from django.contrib.auth.models import User
from library.models import *

class ReaderForm(forms.ModelForm):
    class Meta:
        model=Reader
        fields='__all__'

class Reader_PnoForm(forms.ModelForm):
    class Meta:
        model=Reader_Pno
        fields='__all__'

class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields='__all__'

class Book_CategoryForm(forms.ModelForm):
    class Meta:
        model=Book_Category
        fields='__all__'
#
class Book_AuthorForm(forms.ModelForm):
    class Meta:
        model=Book_Author
        fields='__all__'

class PublisherForm(forms.ModelForm):
    class Meta:
        model=Publisher
        fields='__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model=Staff
        fields='__all__'

class KeepsTrackForm(forms.ModelForm):
    class Meta:
        model=KeepsTrack
        fields='__all__'
        
class PublishedByForm(forms.ModelForm):
    class Meta:
        model=PublishedBy
        fields='__all__'

class MaintainsForm(forms.ModelForm):
    class Meta:
        model=Maintains
        fields='__all__'

class IssuedToForm(forms.ModelForm):
    class Meta:
        model=IssuedTo
        fields='__all__'

class AuthenticateForm(forms.ModelForm):
    class Meta:
        model=Authenticate
        fields='__all__'