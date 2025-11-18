from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("academic-years/", views.AcademicYearListView.as_view(), name="academic_year_list"),
    path("academic-years/create/", views.AcademicYearCreateView.as_view(), name="academic_year_create"),
    path("academic-years/<int:pk>/", views.AcademicYearDetailView.as_view(), name="academic_year_detail"),
    path("academic-years/<int:pk>/update/", views.AcademicYearUpdateView.as_view(), name="academic_year_update"),
    path("academic-years/<int:pk>/delete/", views.AcademicYearDeleteView.as_view(), name="academic_year_delete"),
    path("semesters/", views.SemesterListView.as_view(), name="semester_list"),
    path("semesters/create/", views.SemesterCreateView.as_view(), name="semester_create"),
    path("semesters/<int:pk>/", views.SemesterDetailView.as_view(), name="semester_detail"),
    path("semesters/<int:pk>/update/", views.SemesterUpdateView.as_view(), name="semester_update"),
    path("semesters/<int:pk>/delete/", views.SemesterDeleteView.as_view(), name="semester_delete"),
    path("faculties/", views.FacultyListView.as_view(), name="faculty_list"),
    path("faculties/create/", views.FacultyCreateView.as_view(), name="faculty_create"),
    path("faculties/<int:pk>/", views.FacultyDetailView.as_view(), name="faculty_detail"),
    path("faculties/<int:pk>/update/", views.FacultyUpdateView.as_view(), name="faculty_update"),
    path("faculties/<int:pk>/delete/", views.FacultyDeleteView.as_view(), name="faculty_delete"),
    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path("departments/create/", views.DepartmentCreateView.as_view(), name="department_create"),
    path("departments/<int:pk>/", views.DepartmentDetailView.as_view(), name="department_detail"),
    path("departments/<int:pk>/update/", views.DepartmentUpdateView.as_view(), name="department_update"),
    path("departments/<int:pk>/delete/", views.DepartmentDeleteView.as_view(), name="department_delete"),
]

