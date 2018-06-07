from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 64, unique = True)
    email = models.EmailField()
    password = models.CharField(max_length = 256)
    number_of_trackers = models.IntegerField( default= 0)

    def __str__(self):
        return self.username;

class TrackingCode(models.Model):
    code = models.IntegerField(unique = True,default=0)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True, blank =True)
    #req_headers= models.TextField(max_length= 2048)

    def __str__(self):
        return "code:%s" %(str(self.code))

class Log(models.Model):
    code = models.ForeignKey(TrackingCode , on_delete=models.CASCADE)
    first_hit = models.DateTimeField(auto_now_add=True)
    last_hit = models.DateTimeField(auto_now=True)
    #code = models.CharField( max_length = 256)
    req_headers= models.TextField(max_length= 2048)
    parsed_headers = models.TextField(max_length= 2048,null=True,blank=True)

    def __str__(self):
        return "LOG_%s" %(str(self.code))