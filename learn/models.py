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
    student = models.OneToOneField(User, on_delete=models.CASCADE,max_length=100,null=False)
    subject1 = models.ForeignKey(Subject, related_name="subject_1", on_delete=models.SET_NULL,max_length=100,null=True)
    subject2 = models.ForeignKey(Subject, related_name="subject_2", on_delete=models.SET_NULL,max_length=100,null=True)
    subject3 = models.ForeignKey(Subject, related_name="subject_3", on_delete=models.SET_NULL,max_length=100,null=True)
    subject4 = models.ForeignKey(Subject, related_name="subject_4", on_delete=models.SET_NULL,max_length=100,null=True)
    subject5 = models.ForeignKey(Subject, related_name="subject_5", on_delete=models.SET_NULL,max_length=100,null=True)
    subject6 = models.ForeignKey(Subject, related_name="subject_6", on_delete=models.SET_NULL,max_length=100,null=True)
    subject7 = models.ForeignKey(Subject, related_name="subject_7", on_delete=models.SET_NULL,max_length=100,null=True)
    subject8 = models.ForeignKey(Subject, related_name="subject_8", on_delete=models.SET_NULL,max_length=100,null=True)


    class Meta:
        verbose_name_plural = "students"

    def __str__(self):
        if self.student.first_name == "":
            return f"{self.student.username}"
        return f"{self.student.first_name} {self.student.last_name}"