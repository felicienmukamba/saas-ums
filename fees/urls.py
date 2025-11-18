from django.urls import path

from . import views

app_name = "fees"

urlpatterns = [
    path("categories/", views.FeeCategoryListView.as_view(), name="category_list"),
    path("categories/create/", views.FeeCategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/", views.FeeCategoryDetailView.as_view(), name="category_detail"),
    path("categories/<int:pk>/update/", views.FeeCategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", views.FeeCategoryDeleteView.as_view(), name="category_delete"),
    path("", views.AcademicFeeListView.as_view(), name="academic_fee_list"),
    path("create/", views.AcademicFeeCreateView.as_view(), name="academic_fee_create"),
    path("<int:pk>/", views.AcademicFeeDetailView.as_view(), name="academic_fee_detail"),
    path("<int:pk>/update/", views.AcademicFeeUpdateView.as_view(), name="academic_fee_update"),
    path("<int:pk>/delete/", views.AcademicFeeDeleteView.as_view(), name="academic_fee_delete"),
]

