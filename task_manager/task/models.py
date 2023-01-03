from django.db import models

# Create your models here.
class Task(models.Model):

    task_id = models.IntegerField(primary_key=True, auto_created=True)
    end_data =  models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey('user.User', on_delete=models.PROTECT)
    

    def __str__(self):
        return str(self.id) + '_' + str(self.page_id)
