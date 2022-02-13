from turtle import Turtle
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
import os
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default.jpg",upload_to="profile_pics")

    class Meta:
        verbose_name_plural = "Profiles"

    def save(self,*args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
    
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f"{self.user.username}"
    

class Subject(models.Model):
    subject = models.CharField(max_length=100,null=False)
    image = models.ImageField(default="default.jpg",upload_to="subject_pics",null=False)
    description = models.CharField(max_length=100,null=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,max_length=100,null=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Subjects"

    def save(self,*args, **kwargs):
        super(Subject, self).save(*args, **kwargs)
    
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f"{self.subject}"

class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE,max_length=100,null=False)
    subject = models.ManyToManyField(Subject)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Students"

    def __str__(self):
        if self.student.first_name not in  [""," ",None]:
            return f"{self.student.get_full_name()}"
        return f"{self.student.username}"

class Activity(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,max_length=1000)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,max_length=1000,null=False)
    title = models.CharField(max_length=1000,null=False)
    description =  models.CharField(max_length=1000,null=False)
    is_multiple_choice = models.BooleanField(default=True)
    is_deployed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.title}"

class File(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,max_length=100,null=False)
    title = models.CharField(max_length=1000,null=False)
    description =  models.CharField(max_length=1000,null=False)
    file = models.FileField(upload_to="files",null=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Files"

    def __str__(self):
        return f"{self.title}"

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(File,self).delete(*args,**kwargs)



class MultipleQuestion(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,max_length=500)
    question = RichTextUploadingField(max_length=1000, null=False)
    choice_a = models.CharField(max_length=500,null=False)
    choice_b = models.CharField(max_length=500,null=False)
    choice_c = models.CharField(max_length=500,null=False)
    choice_d = models.CharField(max_length=500,null=False)
    ans = models.CharField(max_length=5,null=False)
    ans_exp = models.CharField(max_length=500,null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Multiple Questions"

    def __str__(self):
        return f"Question-{self.id}"

class QuestionandAnswer(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    question = RichTextUploadingField(max_length=1000, null=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Questions and Answers"

    def __str__(self):
        return f"QuestionandAnswer-{self.id}"

class ImageSheet(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student  = models.ForeignKey(User, on_delete=models.CASCADE,max_length=100)
    answer = models.ImageField(upload_to="users_answers")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Images Sheet"

    def __str__(self):
        return f"Image-{self.id}"
    
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.answer.name))
        super(ImageSheet,self).delete(*args,**kwargs)

class Score(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student  = models.ForeignKey(User, on_delete=models.CASCADE,max_length=100,null=False)
    score    = models.IntegerField(null=True)
    total    = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Scores"
    def __str__(self):
        return f"Student-{self.student.get_full_name()}"