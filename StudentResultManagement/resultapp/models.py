from django.db import models

# Create your models here.
class Class(models.Model):
    class_name=models.CharField(max_length=50)
    class_numeric=models.IntegerField()
    section=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.class_name} - Section {self.section}"

class Subject(models.Model):
    subject_name=models.CharField(max_length=50)
    subject_code=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} - {self.subject_code}"

class Student(models.Model):
    GENDER_CHOICES=(('Male','Male'),('Female','Female')) # first value is database value and second value is display value
    name=models.CharField(max_length=50)
    roll_id=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES)
    dob=models.CharField(max_length=50)
    student_class=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    registration_date=models.DateTimeField(auto_now_add=True)
    updation_date=models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=1)

    def __str__(self):
        return self.name

class SubjectCombination(models.Model):
    student_class=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.student_class} - {self.subject}"

class Result(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    student_class=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    marks=models.IntegerField()
    posting_date=models.DateTimeField(auto_now_add=True)
    updation_date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}"

class Notice(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=500)
    posting_date=models.DateTimeField(auto_now_add=True)
    updation_date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title