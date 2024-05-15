from django.db import models

# Create your models here.

class logindb(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobile = models.IntegerField(null=True)
    gender = models.CharField(max_length=100, null=True)
    place= models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    image = models.ImageField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(logindb, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(logindb, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} - {self.timestamp}"


class updb(models.Model):
    username=models.CharField(max_length=100)
    image=models.ImageField(null=True)
    video=models.FileField(null=True, upload_to='video/')
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

class follow(models.Model):
    username=models.CharField(max_length=100)
    image = models.ImageField(null=True)
    followers=models.IntegerField(null=True)

class follows(models.Model):
    username=models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True)
    followers=models.IntegerField(null=True)

class like(models.Model):
    username=models.CharField(max_length=100)
    image = models.ImageField(null=True)
    likes = models.ImageField(null=True)

class postm(models.Model):
    username=models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    msg=models.CharField(max_length=100)
    image = models.ImageField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Status(models.Model):
    user = models.CharField(max_length=100)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='status_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


