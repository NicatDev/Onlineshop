from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Code(models.Model):
    code = models.CharField(max_length = 300)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='code')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

