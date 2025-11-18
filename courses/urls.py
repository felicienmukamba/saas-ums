from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course_list"),
    path("create/", views.CourseCreateView.as_view(), name="course_create"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course_update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
    path("offerings/", views.CourseOfferingListView.as_view(), name="offering_list"),
    path("offerings/create/", views.CourseOfferingCreateView.as_view(), name="offering_create"),
    path("offerings/<int:pk>/", views.CourseOfferingDetailView.as_view(), name="offering_detail"),
    path("offerings/<int:pk>/update/", views.CourseOfferingUpdateView.as_view(), name="offering_update"),
    path("offerings/<int:pk>/delete/", views.CourseOfferingDeleteView.as_view(), name="offering_delete"),
]

