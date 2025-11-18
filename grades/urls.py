from django.urls import path

from . import views

app_name = "grades"

urlpatterns = [
    path("", views.GradeListView.as_view(), name="grade_list"),
    path("create/", views.GradeCreateView.as_view(), name="grade_create"),
    path("<int:pk>/", views.GradeDetailView.as_view(), name="grade_detail"),
    path("<int:pk>/update/", views.GradeUpdateView.as_view(), name="grade_update"),
    path("<int:pk>/delete/", views.GradeDeleteView.as_view(), name="grade_delete"),
    path("proclamations/pdf/", views.ProclamationListPDFView.as_view(), name="proclamations_pdf"),
]

