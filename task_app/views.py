from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from task_app import tasks
import celery

@csrf_exempt
def get_task_status(request):
	"""
	View responsible to expose the task status through API
	"""
	if request.method == "POST":
		if request.POST.get("task_id"):
			try:
				status=celery.result.AsyncResult(request.POST["task_id"]).status
				return JsonResponse({"ok":True,"status":status})
			except Exception as e:
				return JsonResponse({"ok":False,"message":str(e)},status=500)
		return JsonResponse({"ok":False,"message":"task_id key is missing"},status=406)
	return JsonResponse({"ok":False,"message":"Only POST method allowed"},status=405)


@csrf_exempt
def stop_task(request):
	"""
	View responsible to expose the task stop control through API
	"""
	if request.method == "POST":
		if request.POST.get("task_id"):
			try:
				celery.task.control.revoke(request.POST["task_id"], terminate=True)
				status=celery.result.AsyncResult(request.POST["task_id"]).status
				return JsonResponse({"ok":True,"status":"REVOKED"})
			except Exception as e:
				return JsonResponse({"ok":False,"message":str(e)},status=500)
		return JsonResponse({"ok":False,"message":"task_id key is missing"},status=406)
	return JsonResponse({"ok":False,"message":"Only POST method allowed"},status=405)


@csrf_exempt
def upload_data_file(request):
	from .models import HistoricRuns
	if request.method == "POST":
		if request.FILES['file']:
			try:
				task = tasks.upload_data_to_db.delay(request.FILES['file'].temporary_file_path())
				task = HistoricRuns(task_id=task.id,status="PENDING")
				task.save()
				return JsonResponse({"ok":True,"task_id":task.task_id})
			except Exception as e:
				return JsonResponse({"ok":False,"message":str(e)},status=500)
		return JsonResponse({"ok":False,"message":"file key is missing"},status=406)
	return JsonResponse({"ok":False,"message":"Only POST method allowed"},status=405)


@csrf_exempt
def export_data(request):
	from .models import HistoricRuns
	if request.method == "POST":
		try:
			task = tasks.export_data_to_file.delay()
			task = HistoricRuns(task_id=task.id,status="PENDING")
			task.save()
			return JsonResponse({"ok":True,"task_id":task.task_id})
		except Exception as e:
			return JsonResponse({"ok":False,"message":str(e)},status=500)
	return JsonResponse({"ok":False,"message":"Only POST method allowed"},status=405)


@csrf_exempt
def create_team_in_bulk(request):
	from .models import HistoricRuns
	if request.method == "POST":
		if request.FILES['file']:
			try:
				task = tasks.upload_team_to_db.delay(request.FILES['file'].temporary_file_path())
				task = HistoricRuns(task_id=task.id,status="PENDING")
				task.save()
				return JsonResponse({"ok":True,"task_id":task.task_id})
			except Exception as e:
				return JsonResponse({"ok":False,"message":str(e)},status=500)
		return JsonResponse({"ok":False,"message":"file key is missing"},status=406)
	return JsonResponse({"ok":False,"message":"Only POST method allowed"},status=405)
