from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime,timedelta

class Reader(models.Model):
    userid=models.CharField(max_length=50,primary_key=True)
    email=models.EmailField()
    isfaculty=models.BooleanField()
    dept=models.CharField(max_length=50)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)

    def __str__(self):
        return "Reader"+self.userid+' '+self.fname+' '+self.lname

class Reader_Pno(models.Model):
    userid=models.ForeignKey(Reader,on_delete=models.CASCADE)
    pnumber=models.CharField(max_length=10)

    def __str__(self):
        return "Reader_Pno"+self.userid+' '+self.pnumber

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
    fsname=models.CharField(max_length=30)
    lsname=models.CharField(max_length=30)
    sid=models.CharField(max_length=30,primary_key=True)
    

    def __str__(self):
        return "Staff"+self.sid+' '+self.fsname+' '+self.lsname

class KeepsTrack(models.Model):
    sid=models.ForeignKey(Staff,on_delete=models.CASCADE)
    userid=models.ForeignKey(Reader,on_delete=models.CASCADE)

    def __str__(self):
        return "KeepsTrack"+self.sid+' '+self.userid

class PublishedBy(models.Model):
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    pid=models.ForeignKey(Publisher,on_delete=models.CASCADE)

    def __str__(self):
        return "PublishedBy"+self.isbn+' '+self.pid


class Maintains(models.Model):
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    sid=models.ForeignKey(Staff,on_delete=models.CASCADE)

    def __str__(self):
        return "Maintains"+self.isbn+' '+self.pid

def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedTo(models.Model):
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    userid=models.ForeignKey(Reader,on_delete=models.CASCADE)
    fine=models.IntegerField()
    issuedate=models.DateField(auto_now=True)
    returndate=models.DateField(default=get_expiry)

    def __str__(self):
        return "IssuedTo"+self.userid

class Authenticate(models.Model):
    userid=models.ForeignKey(Reader,on_delete=models.CASCADE)
    sid=models.ForeignKey(Staff,on_delete=models.CASCADE)
    password=models.CharField(max_length=30)
    loginid=models.CharField(max_length=30,primary_key=True)
   