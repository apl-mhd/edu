from django.db import models

# Create your models here.


class District(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class College(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
