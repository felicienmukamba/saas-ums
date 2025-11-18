from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import json

from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
    RolePermissionMixin,
)
from core.forms import AcademicYearForm, DepartmentForm, FacultyForm, SemesterForm, PromotionForm
from core.models import AcademicYear, Department, Faculty, Semester, Promotion


class RectorateAccessMixin:
    allowed_roles = RoleGroups.MANAGEMENT


class DashboardView(RolePermissionMixin, TemplateView):
    template_name = "core/dashboard.html"
    allowed_roles = RoleGroups.ALL_STAFF


# Quick Add Views for nested forms
@method_decorator(csrf_exempt, name='dispatch')
class QuickAddAcademicYearView(BaseCreateView, RolePermissionMixin):
    model = AcademicYear
    form_class = AcademicYearForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'year',
            'model_name': 'Année académique'
        }, request=request)
        return JsonResponse({'form_html': form_html})

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({
            "success": True,
            "id": instance.pk,
            "name": str(instance),
            "value": instance.pk,
        })

    def form_invalid(self, form):
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'year',
            'model_name': 'Année académique'
        }, request=self.request)
        return JsonResponse({
            "success": False,
            "errors": form.errors,
            "form_html": form_html,
        }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class QuickAddFacultyView(BaseCreateView, RolePermissionMixin):
    model = Faculty
    form_class = FacultyForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'faculty',
            'model_name': 'Faculté'
        }, request=request)
        return JsonResponse({'form_html': form_html})

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({
            "success": True,
            "id": instance.pk,
            "name": str(instance),
            "value": instance.pk,
        })

    def form_invalid(self, form):
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'faculty',
            'model_name': 'Faculté'
        }, request=self.request)
        return JsonResponse({
            "success": False,
            "errors": form.errors,
            "form_html": form_html,
        }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class QuickAddDepartmentView(BaseCreateView, RolePermissionMixin):
    model = Department
    form_class = DepartmentForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'department',
            'model_name': 'Département'
        }, request=request)
        return JsonResponse({'form_html': form_html})

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({
            "success": True,
            "id": instance.pk,
            "name": str(instance),
            "value": instance.pk,
        })

    def form_invalid(self, form):
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'department',
            'model_name': 'Département'
        }, request=self.request)
        return JsonResponse({
            "success": False,
            "errors": form.errors,
            "form_html": form_html,
        }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class QuickAddSemesterView(BaseCreateView, RolePermissionMixin):
    model = Semester
    form_class = SemesterForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'semester',
            'model_name': 'Semestre'
        }, request=request)
        return JsonResponse({'form_html': form_html})

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({
            "success": True,
            "id": instance.pk,
            "name": str(instance),
            "value": instance.pk,
        })

    def form_invalid(self, form):
        form_html = render_to_string('core/quick_add_form.html', {
            'form': form,
            'field_name': 'semester',
            'model_name': 'Semestre'
        }, request=self.request)
        return JsonResponse({
            "success": False,
            "errors": form.errors,
            "form_html": form_html,
        }, status=400)


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


class PromotionListView(RectorateAccessMixin, BaseListView):
    model = Promotion
    list_display = ("name", "code", "department")
    page_title = "Promotions"
    create_url_name = "core:promotion_create"
    detail_url_name = "core:promotion_detail"
    update_url_name = "core:promotion_update"
    delete_url_name = "core:promotion_delete"


class PromotionCreateView(RectorateAccessMixin, BaseCreateView):
    model = Promotion
    form_class = PromotionForm
    success_url_name = "core:promotion_list"
    success_message = "Promotion créée."

class PromotionDetailView(RectorateAccessMixin, BaseDetailView):
    model = Promotion

class PromotionUpdateView(RectorateAccessMixin, BaseUpdateView):
    model = Promotion
    success_url_name = "core:promotion_list"
    success_message = "Promotion mise à jour."


class PromotionDeleteView(RectorateAccessMixin, BaseDeleteView):
    model = Promotion
    success_url_name = "core:promotion_list"

