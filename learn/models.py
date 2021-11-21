from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg",upload_to="profile_pics")

    class Meta:
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"{self.user.username}"
    

class Subject(models.Model):
    subject = models.CharField(max_length=100,null=False)
    image = models.ImageField(default="default.jpg",upload_to="subject_pics",null=False)
    description = models.CharField(max_length=100,null=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,max_length=100,null=False)

    class Meta:
        verbose_name_plural = "subjects"

    def __str__(self):
        return f"{self.subject}"

class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE,max_length=100,null=False)
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE,max_length=100,null=True)


    class Meta:
        verbose_name_plural = "students"

    def __str__(self):
        if self.student.first_name == "":
            return f"{self.student.username}"
        return f"{self.student.first_name} {self.student.last_name}"