from django.urls import path

from . import views

app_name = "enrollment"

urlpatterns = [
    path("", views.EnrollmentListView.as_view(), name="enrollment_list"),
    path("create/", views.EnrollmentCreateView.as_view(), name="enrollment_create"),
    path("<int:pk>/", views.EnrollmentDetailView.as_view(), name="enrollment_detail"),
    path("<int:pk>/update/", views.EnrollmentUpdateView.as_view(), name="enrollment_update"),
    path("<int:pk>/delete/", views.EnrollmentDeleteView.as_view(), name="enrollment_delete"),
    path("choices/", views.SecondaryChoiceListView.as_view(), name="secondary_choice_list"),
    path("choices/create/", views.SecondaryChoiceCreateView.as_view(), name="secondary_choice_create"),
    path("choices/<int:pk>/", views.SecondaryChoiceDetailView.as_view(), name="secondary_choice_detail"),
    path("choices/<int:pk>/update/", views.SecondaryChoiceUpdateView.as_view(), name="secondary_choice_update"),
    path("choices/<int:pk>/delete/", views.SecondaryChoiceDeleteView.as_view(), name="secondary_choice_delete"),
    path("documents/", views.DocumentListView.as_view(), name="document_list"),
    path("documents/create/", views.DocumentCreateView.as_view(), name="document_create"),
    path("documents/<int:pk>/", views.DocumentDetailView.as_view(), name="document_detail"),
    path("documents/<int:pk>/update/", views.DocumentUpdateView.as_view(), name="document_update"),
    path("documents/<int:pk>/delete/", views.DocumentDeleteView.as_view(), name="document_delete"),
    path("<int:pk>/fiche/pdf/", views.EnrollmentRegistrationPDFView.as_view(), name="enrollment_registration_pdf"),
    path("<int:pk>/bulletin/pdf/", views.EnrollmentBulletinPDFView.as_view(), name="enrollment_bulletin_pdf"),
]

