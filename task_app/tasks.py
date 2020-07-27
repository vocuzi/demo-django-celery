from __future__ import absolute_import, unicode_literals
from django.db import transaction
import celery
from time import sleep
from csv import reader, writer
from task_app.models import SampleModelForData, HistoricRuns, SampleModelForTeam

class CallbackClass(celery.Task):
	def on_success(self, retval, task_id, args, kwargs):
		obj = HistoricRuns.objects.get(task_id=task_id)
		obj.status = celery.result.AsyncResult(task_id).status
		obj.save()
	def on_error(self, retval, task_id, args, kwargs):
		obj = HistoricRuns.objects.get(task_id=task_id)
		obj.status = celery.result.AsyncResult(task_id).status
		obj.save()


@celery.shared_task(bind=True,base=CallbackClass)
def upload_data_to_db(self,file):
	with transaction.atomic():
		file = open(file)
		read = reader(file)
		obj, created = HistoricRuns.objects.get_or_create(
			task_id=self.request.id,
			status=celery.result.AsyncResult(self.request.id).status
			)
		for row in read:
			sleep(5)
			ds = SampleModelForData(
				batch_id=obj,
				first_name=row[1],
				last_name=row[2],
				email=row[3],
				gender=row[4]
			)
			ds.save()
		
@celery.shared_task(bind=True,base=CallbackClass)
def upload_team_to_db(self,file):
	with transaction.atomic():
		file = open(file)
		read = reader(file)
		obj, created = HistoricRuns.objects.get_or_create(
			task_id=self.request.id,
			status=celery.result.AsyncResult(self.request.id).status
			)
		for row in read:
			sleep(5)
			ds = SampleModelForTeam(
				batch_id=obj,
				first_name=row[1],
				last_name=row[2],
				email=row[3],
				gender=row[4]
			)
			ds.save()

@celery.shared_task(bind=True,base=CallbackClass)
def export_data_to_file(self):
	with transaction.atomic():
		obj, created = HistoricRuns.objects.get_or_create(
			task_id=self.request.id,
			status=celery.result.AsyncResult(self.request.id).status
			)
		wrtr = writer(open(f"static/{self.request.id}.csv","w"))
		wrtr.writerow(['timestamp','first_name','last_name','email','gender'])
		ds = SampleModelForData.objects.all().values_list('timestamp','first_name','last_name','email','gender')
		for item in ds:
			wrtr.writerow(item)
			sleep(3)