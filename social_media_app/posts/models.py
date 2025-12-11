import uuid
from django.db import models
from django.conf import settings

# Function to generate a unique filename for uploaded images
def get_unique_image_filename(instance, filename):
    ext = filename.split('.')[-1].lower()  # Convert to lowercase to handle extension case sensitivity
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return f"uploads/{unique_filename}"

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=get_unique_image_filename, null=True, blank=True)
    
    # ManyToMany through Like - this handles likes automatically
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Like',
        related_name='liked_posts',
        blank=True  # Allows posts with no likes
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    @property
    def like_count(self):
        """Helper property to get like count"""
        return self.likes.count()
    
    def is_liked_by(self, user):
        """Check if a specific user liked this post"""
        if not user.is_authenticated:
            return False
        return self.likes.filter(id=user.id).exists()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"