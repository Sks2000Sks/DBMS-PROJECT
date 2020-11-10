from django.db import models
from django.contrib.auth.models import AbstractUser,User
from datetime import datetime,timedelta

class Reader(models.Model):
    isfaculty=models.BooleanField()
    dept=models.CharField(max_length=50)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return "Reader"+self.user.id+' '+self.user.first_name
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id

class Reader_Pno(models.Model):
    userid=models.ForeignKey(Reader,on_delete=models.CASCADE)
    pnumber=models.CharField(max_length=10)

    def __str__(self):
        return "Reader_Pno"+self.pnumber

class Book(models.Model): 
    isbn=models.CharField(max_length=30,primary_key=True,unique=True)
    copies= models.IntegerField()
    price= models.IntegerField()
    title=models.CharField(max_length=30) 
    edition=models.IntegerField()
    
    def __str__(self):
        return "Book"+ self.isbn+'['+self.title+']'

class Book_Category(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biographie'),
        ('history', 'History'),
        ]
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    def __str__(self):
        return "Book_Category"+self.category

class Book_Author(models.Model):
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    author=models.CharField(max_length=30)
    def __str__(self):
        return "Book_Author"+self.author


class Publisher(models.Model):
    pname=models.CharField(max_length=30)
    pid=models.CharField(max_length=30,primary_key=True)
    year=models.IntegerField()

    def __str__(self):
        return "Publisher"+self.pname+' '+self.pid

class Staff(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)   

    def __str__(self):
        return "Staff"+str(self.user.id)+' '+str(self.user.first_name)

class KeepsTrack(models.Model):
    sid=models.ForeignKey(Staff,on_delete=models.CASCADE)
    userid=models.ForeignKey(Reader,on_delete=models.CASCADE)

    def __str__(self):
        return "KeepsTrack"

class PublishedBy(models.Model):
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    pid=models.ForeignKey(Publisher,on_delete=models.CASCADE)

    def __str__(self):
        return "PublishedBy"+self.isbn+' '+self.pid


class Maintains(models.Model):
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    sid=models.ForeignKey(Staff,on_delete=models.CASCADE)

    def __str__(self):
        return "Maintains"

def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedTo(models.Model):
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    fine=models.IntegerField(default=0)
    issuedate=models.DateField(auto_now=True)
    returndate=models.DateField(default=get_expiry)

    def __str__(self):
        return "IssuedTo"+str(self.userid.id)

