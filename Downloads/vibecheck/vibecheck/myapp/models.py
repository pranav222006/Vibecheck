from django.db import models

class FAQ(models.Model):
    category = models.CharField(max_length=50)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    def __str__(self): return self.question

class ErrorCode(models.Model):
    code = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    explanation = models.TextField()
    fix = models.TextField()
    class Meta: ordering = ["code"]

class Ticket(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    source = models.CharField(max_length=20, default="form")
    status = models.CharField(max_length=20, default="open")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
