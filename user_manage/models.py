from django.db import models
from django.contrib.auth.models import User


class fileUpload(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(null=True)
    file_like = models.ManyToManyField(User,related_name='likes')
    

    def __str__(self):
        return self.user.username
 
class comment(models.Model):
    file = models.ForeignKey(fileUpload,related_name='comment', on_delete=models.SET_NULL, blank=True, null=True)
    from_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    body = models.TextField()

    def __str__(self):
        return self.body[:100]
        
class uploadExcel(models.Model):
    field_a = models.IntegerField()
    field_b = models.IntegerField()
    field_c = models.IntegerField()
    field_d = models.IntegerField()

    def __str__(self) :
        return 'File Added'
