from django.db import models
from tgbot.models import User

class TaskManager(models.Manager):     
   def users_tasks(self, user):
      return self.get_queryset().filter(user=user).order_by('priority').all()


class Tasks(models.Model):
   title = models.CharField(max_length=50)
   status = models.BooleanField(default=False)
   priority = models.IntegerField(default=3)
   user = models.ForeignKey(User, on_delete=models.CASCADE)

   objects = TaskManager()

