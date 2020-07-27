from django.db import models

# Create your models here.
class HistoricRuns(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	task_id = models.CharField(max_length=36)
	status = models.CharField(max_length=10)

class SampleModelForData(models.Model):
	batch_id = models.ForeignKey(HistoricRuns,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()
	gender = models.CharField(max_length=1)


class SampleModelForTeam(models.Model):
	batch_id = models.ForeignKey(HistoricRuns,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()
	gender = models.CharField(max_length=1)
