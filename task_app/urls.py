from django.urls import path
from task_app.views import *

urlpatterns = [
    path('status/', get_task_status),
    path('stop/', stop_task),
    path('addData/', upload_data_file),
    path('addTeam/', create_team_in_bulk),
    path('exportData/', export_data),
]