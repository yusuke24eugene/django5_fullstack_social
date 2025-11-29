import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Function to generate a unique file name for profile pictures
def user_profile_picture_path(instance, filename):
    # Generate a unique UUID for the file name
    ext = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{ext}'
    # Return the path where the file will be uploaded
    return os.path.join('profile_pics/', str(instance.id), unique_filename)

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField()
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.username
    
    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()