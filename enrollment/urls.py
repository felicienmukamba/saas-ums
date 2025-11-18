from django.urls import path

from enrollment import views
app_name = "enrollment"

urlpatterns = [
    # Demandes d'inscription (publiques - pas besoin de login)
    path("request/", views.EnrollmentRequestCreateView.as_view(), name="request_create"),
    path("request/<int:pk>/success/", views.EnrollmentRequestSuccessView.as_view(), name="request_success"),
    
    # Gestion des demandes (chargés d'inscription)
    path("requests/", views.EnrollmentRequestListView.as_view(), name="request_list"),
    path("requests/<int:pk>/", views.EnrollmentRequestDetailView.as_view(), name="request_detail"),
    path("requests/<int:pk>/approve/", views.EnrollmentRequestApproveView.as_view(), name="request_approve"),
    path("requests/<int:pk>/reject/", views.EnrollmentRequestRejectView.as_view(), name="request_reject"),
    
    # Inscription directe par chargé
    path("direct/", views.DirectEnrollmentCreateView.as_view(), name="direct_create"),
    
    # Inscriptions (CRUD standard)
    path("", views.EnrollmentListView.as_view(), name="enrollment_list"),
    path("create/", views.EnrollmentCreateView.as_view(), name="enrollment_create"),
    path("<int:pk>/", views.EnrollmentDetailView.as_view(), name="enrollment_detail"),
    path("<int:pk>/update/", views.EnrollmentUpdateView.as_view(), name="enrollment_update"),
    path("<int:pk>/delete/", views.EnrollmentDeleteView.as_view(), name="enrollment_delete"),
    
    # PDF
    path("<int:pk>/fiche/pdf/", views.EnrollmentRegistrationPDFView.as_view(), name="registration_pdf"),
    path("<int:pk>/bulletin/pdf/", views.EnrollmentBulletinPDFView.as_view(), name="bulletin_pdf"),
    
    # SecondaryChoice
    path("secondary-choices/", views.SecondaryChoiceListView.as_view(), name="secondary_choice_list"),
    path("secondary-choices/create/", views.SecondaryChoiceCreateView.as_view(), name="secondary_choice_create"),
    path("secondary-choices/<int:pk>/", views.SecondaryChoiceDetailView.as_view(), name="secondary_choice_detail"),
    path("secondary-choices/<int:pk>/update/", views.SecondaryChoiceUpdateView.as_view(), name="secondary_choice_update"),
    path("secondary-choices/<int:pk>/delete/", views.SecondaryChoiceDeleteView.as_view(), name="secondary_choice_delete"),
    
    # Documents
    path("documents/", views.DocumentListView.as_view(), name="document_list"),
    path("documents/create/", views.DocumentCreateView.as_view(), name="document_create"),
    path("documents/<int:pk>/", views.DocumentDetailView.as_view(), name="document_detail"),
    path("documents/<int:pk>/update/", views.DocumentUpdateView.as_view(), name="document_update"),
    path("documents/<int:pk>/delete/", views.DocumentDeleteView.as_view(), name="document_delete"),
]
