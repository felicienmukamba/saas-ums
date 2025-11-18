from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.StudentListView.as_view(), name="student_list"),
    path("create/", views.StudentCreateView.as_view(), name="student_create"),
    path("<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("<int:pk>/update/", views.StudentUpdateView.as_view(), name="student_update"),
    path("<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("addresses/", views.AddressListView.as_view(), name="address_list"),
    path("addresses/create/", views.AddressCreateView.as_view(), name="address_create"),
    path("addresses/<int:pk>/", views.AddressDetailView.as_view(), name="address_detail"),
    path("addresses/<int:pk>/update/", views.AddressUpdateView.as_view(), name="address_update"),
    path("addresses/<int:pk>/delete/", views.AddressDeleteView.as_view(), name="address_delete"),
    path("contacts/", views.ContactListView.as_view(), name="contact_list"),
    path("contacts/create/", views.ContactCreateView.as_view(), name="contact_create"),
    path("contacts/<int:pk>/", views.ContactDetailView.as_view(), name="contact_detail"),
    path("contacts/<int:pk>/update/", views.ContactUpdateView.as_view(), name="contact_update"),
    path("contacts/<int:pk>/delete/", views.ContactDeleteView.as_view(), name="contact_delete"),
    path("diplomas/", views.DiplomaListView.as_view(), name="diploma_list"),
    path("diplomas/create/", views.DiplomaCreateView.as_view(), name="diploma_create"),
    path("diplomas/<int:pk>/", views.DiplomaDetailView.as_view(), name="diploma_detail"),
    path("diplomas/<int:pk>/update/", views.DiplomaUpdateView.as_view(), name="diploma_update"),
    path("diplomas/<int:pk>/delete/", views.DiplomaDeleteView.as_view(), name="diploma_delete"),
    path("parents/", views.ParentListView.as_view(), name="parent_list"),
    path("parents/create/", views.ParentCreateView.as_view(), name="parent_create"),
    path("parents/<int:pk>/", views.ParentDetailView.as_view(), name="parent_detail"),
    path("parents/<int:pk>/update/", views.ParentUpdateView.as_view(), name="parent_update"),
    path("parents/<int:pk>/delete/", views.ParentDeleteView.as_view(), name="parent_delete"),
    path("sponsors/", views.SponsorListView.as_view(), name="sponsor_list"),
    path("sponsors/create/", views.SponsorCreateView.as_view(), name="sponsor_create"),
    path("sponsors/<int:pk>/", views.SponsorDetailView.as_view(), name="sponsor_detail"),
    path("sponsors/<int:pk>/update/", views.SponsorUpdateView.as_view(), name="sponsor_update"),
    path("sponsors/<int:pk>/delete/", views.SponsorDeleteView.as_view(), name="sponsor_delete"),
    path("support/", views.StudentSponsorListView.as_view(), name="student_sponsor_list"),
    path("support/create/", views.StudentSponsorCreateView.as_view(), name="student_sponsor_create"),
    path("support/<int:pk>/", views.StudentSponsorDetailView.as_view(), name="student_sponsor_detail"),
    path("support/<int:pk>/update/", views.StudentSponsorUpdateView.as_view(), name="student_sponsor_update"),
    path("support/<int:pk>/delete/", views.StudentSponsorDeleteView.as_view(), name="student_sponsor_delete"),
    path("<int:pk>/etat-sortie/pdf/", views.StudentExitCertificatePDFView.as_view(), name="student_exit_pdf"),
]

