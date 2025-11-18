from django.views.generic import TemplateView

from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
    RolePermissionMixin,
)
from .forms import AcademicYearForm, DepartmentForm, FacultyForm, SemesterForm
from .models import AcademicYear, Department, Faculty, Semester


class DashboardView(RolePermissionMixin, TemplateView):
    template_name = "core/dashboard.html"
    allowed_roles = RoleGroups.ALL_STAFF


class RectorateAccessMixin:
    allowed_roles = RoleGroups.MANAGEMENT


class AcademicYearListView(RectorateAccessMixin, BaseListView):
    model = AcademicYear
    list_display = ("name", "code")
    page_title = "Années académiques"
    create_url_name = "core:academic_year_create"
    detail_url_name = "core:academic_year_detail"
    update_url_name = "core:academic_year_update"
    delete_url_name = "core:academic_year_delete"


class AcademicYearCreateView(RectorateAccessMixin, BaseCreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    success_url_name = "core:academic_year_list"
    success_message = "Année académique créée."


class AcademicYearDetailView(RectorateAccessMixin, BaseDetailView):
    model = AcademicYear


class AcademicYearUpdateView(RectorateAccessMixin, BaseUpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    success_url_name = "core:academic_year_list"
    success_message = "Année académique mise à jour."


class AcademicYearDeleteView(RectorateAccessMixin, BaseDeleteView):
    model = AcademicYear
    success_url_name = "core:academic_year_list"


class SemesterListView(RectorateAccessMixin, BaseListView):
    model = Semester
    list_display = ("name", "code")
    page_title = "Semestres"
    create_url_name = "core:semester_create"
    detail_url_name = "core:semester_detail"
    update_url_name = "core:semester_update"
    delete_url_name = "core:semester_delete"


class SemesterCreateView(RectorateAccessMixin, BaseCreateView):
    model = Semester
    form_class = SemesterForm
    success_url_name = "core:semester_list"
    success_message = "Semestre créé."


class SemesterDetailView(RectorateAccessMixin, BaseDetailView):
    model = Semester


class SemesterUpdateView(RectorateAccessMixin, BaseUpdateView):
    model = Semester
    form_class = SemesterForm
    success_url_name = "core:semester_list"
    success_message = "Semestre mis à jour."


class SemesterDeleteView(RectorateAccessMixin, BaseDeleteView):
    model = Semester
    success_url_name = "core:semester_list"


class FacultyListView(RectorateAccessMixin, BaseListView):
    model = Faculty
    list_display = ("name", "code")
    page_title = "Facultés"
    create_url_name = "core:faculty_create"
    detail_url_name = "core:faculty_detail"
    update_url_name = "core:faculty_update"
    delete_url_name = "core:faculty_delete"


class FacultyCreateView(RectorateAccessMixin, BaseCreateView):
    model = Faculty
    form_class = FacultyForm
    success_url_name = "core:faculty_list"
    success_message = "Faculté créée."


class FacultyDetailView(RectorateAccessMixin, BaseDetailView):
    model = Faculty


class FacultyUpdateView(RectorateAccessMixin, BaseUpdateView):
    model = Faculty
    form_class = FacultyForm
    success_url_name = "core:faculty_list"
    success_message = "Faculté mise à jour."


class FacultyDeleteView(RectorateAccessMixin, BaseDeleteView):
    model = Faculty
    success_url_name = "core:faculty_list"


class DepartmentListView(RectorateAccessMixin, BaseListView):
    model = Department
    list_display = ("name", "code", "faculty")
    page_title = "Départements"
    create_url_name = "core:department_create"
    detail_url_name = "core:department_detail"
    update_url_name = "core:department_update"
    delete_url_name = "core:department_delete"


class DepartmentCreateView(RectorateAccessMixin, BaseCreateView):
    model = Department
    form_class = DepartmentForm
    success_url_name = "core:department_list"
    success_message = "Département créé."


class DepartmentDetailView(RectorateAccessMixin, BaseDetailView):
    model = Department


class DepartmentUpdateView(RectorateAccessMixin, BaseUpdateView):
    model = Department
    form_class = DepartmentForm
    success_url_name = "core:department_list"
    success_message = "Département mis à jour."


class DepartmentDeleteView(RectorateAccessMixin, BaseDeleteView):
    model = Department
    success_url_name = "core:department_list"
