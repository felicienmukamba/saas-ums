from django.urls import path

from . import views

app_name = "assessments"

urlpatterns = [
    path("types/", views.AssessmentTypeListView.as_view(), name="type_list"),
    path("types/create/", views.AssessmentTypeCreateView.as_view(), name="type_create"),
    path("types/<int:pk>/", views.AssessmentTypeDetailView.as_view(), name="type_detail"),
    path("types/<int:pk>/update/", views.AssessmentTypeUpdateView.as_view(), name="type_update"),
    path("types/<int:pk>/delete/", views.AssessmentTypeDeleteView.as_view(), name="type_delete"),
    path("weightings/", views.AssessmentWeightingListView.as_view(), name="weighting_list"),
    path("weightings/create/", views.AssessmentWeightingCreateView.as_view(), name="weighting_create"),
    path("weightings/<int:pk>/", views.AssessmentWeightingDetailView.as_view(), name="weighting_detail"),
    path("weightings/<int:pk>/update/", views.AssessmentWeightingUpdateView.as_view(), name="weighting_update"),
    path("weightings/<int:pk>/delete/", views.AssessmentWeightingDeleteView.as_view(), name="weighting_delete"),
]

