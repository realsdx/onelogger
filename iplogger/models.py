from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username
        and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        #always normalize username
        user = self.model(
            username=self.model.normalize_username(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        """
        Creates and saves a staffuser with the given username 
        and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.save(using = self._db)
        return user


    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username 
        and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length = 64, unique = True)
    email = models.EmailField(blank = True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    number_of_trackers = models.IntegerField( default= 0)

    active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] #USERNAME_FIELD and password are required by default
    
    objects = UserManager()


    def __str__(self):
        return self.username


    # get_full_name and get_short_name are not required in Django2.0
    def has_perm(self, perm , obj = None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        return self.staff


    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class TrackingCode(models.Model):
    code = models.CharField(max_length=16, default='N/A')
    redirect_uri = models.URLField(default="https://www.google.com")
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='codes', null=True, blank =True)

    def __str__(self):
        return "code:%s" %(str(self.code))

class Log(models.Model):
    code = models.ForeignKey(TrackingCode , on_delete=models.CASCADE)
    hit_count = models.IntegerField(default=0)
    first_hit = models.DateTimeField(auto_now_add=True)
    last_hit = models.DateTimeField(auto_now=True)
    headers_info = models.TextField(max_length= 2048)
    internal_ip = models.CharField(max_length=64, null=True, blank=True)
    parsed_headers_info = models.TextField(max_length= 2048,null=True,blank=True)

    def __str__(self):
        return "LOG_%s" %(str(self.code))