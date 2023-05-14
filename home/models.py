from django.db import models


class email_verify(models.Model):
    user = models.CharField(max_length=2000)
    token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)


class JOBS(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    csv = models.FileField(upload_to="download", blank=True, null=True)
    user = models.CharField(max_length=300)
    progress = models.CharField(max_length=300)
    emails = models.TextField()
