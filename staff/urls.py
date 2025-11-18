from django.urls import path

from . import views

app_name = "staff"

urlpatterns = [
    path("", views.CourseAssignmentListView.as_view(), name="assignment_list"),
    path("create/", views.CourseAssignmentCreateView.as_view(), name="assignment_create"),
    path("<int:pk>/", views.CourseAssignmentDetailView.as_view(), name="assignment_detail"),
    path("<int:pk>/update/", views.CourseAssignmentUpdateView.as_view(), name="assignment_update"),
    path("<int:pk>/delete/", views.CourseAssignmentDeleteView.as_view(), name="assignment_delete"),
]

