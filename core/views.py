from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
    RolePermissionMixin,
)

from core.models import (
    AcademicYear,
    Department,
    Faculty,
    Semester,
    Promotion
)

from core.forms import (
    AcademicYearForm,
    DepartmentForm,
    FacultyForm,
    SemesterForm,
    PromotionForm
)


# ============================================================
# ACCESS MIXIN (toujours simple)
# ============================================================

class RectorateAccessMixin:
    allowed_roles = RoleGroups.MANAGEMENT



# ============================================================
# Dashboard
# ============================================================

class DashboardView(TemplateView):
    template_name = "core/dashboard.html"
    allowed_roles = RoleGroups.ALL_STAFF


# ============================================================
# Landing Page
# ============================================================

class LandingPageView(TemplateView):
    template_name = "core/landing.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)


# ============================================================
# QUICK ADD VIEWS - FIXED MRO ORDER
# ============================================================

@method_decorator(csrf_exempt, name='dispatch')
class QuickAddAcademicYearView(BaseCreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': self.form_class(), 'field_name': 'year', 'model_name': 'Année académique'},
            request=request
        )
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
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': form, 'field_name': 'year', 'model_name': 'Année académique'},
            request=self.request
        )
        return JsonResponse({"success": False, "errors": form.errors, "form_html": form_html}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class QuickAddFacultyView(BaseCreateView):
    model = Faculty
    form_class = FacultyForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': self.form_class(), 'field_name': 'faculty', 'model_name': 'Faculté'},
            request=request
        )
        return JsonResponse({'form_html': form_html})

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({"success": True, "id": instance.pk, "name": str(instance), "value": instance.pk})

    def form_invalid(self, form):
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': form, 'field_name': 'faculty', 'model_name': 'Faculté'},
            request=self.request
        )
        return JsonResponse({"success": False, "errors": form.errors, "form_html": form_html}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class QuickAddDepartmentView(BaseCreateView):
    model = Department
    form_class = DepartmentForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': self.form_class(), 'field_name': 'department', 'model_name': 'Département'},
            request=request
        )
        return JsonResponse({'form_html': form_html})

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({"success": True, "id": instance.pk, "name": str(instance), "value": instance.pk})

    def form_invalid(self, form):
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': form, 'field_name': 'department', 'model_name': 'Département'},
            request=self.request
        )
        return JsonResponse({"success": False, "errors": form.errors, "form_html": form_html}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class QuickAddSemesterView(BaseCreateView):
    model = Semester
    form_class = SemesterForm
    allowed_roles = RoleGroups.MANAGEMENT

    def get(self, request, *args, **kwargs):
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': self.form_class(), 'field_name': 'semester', 'model_name': 'Semestre'},
            request=request
        )
        return JsonResponse({'form_html': form_html})

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({"success": True, "id": instance.pk, "name": str(instance), "value": instance.pk})

    def form_invalid(self, form):
        form_html = render_to_string(
            'core/quick_add_form.html',
            {'form': form, 'field_name': 'semester', 'model_name': 'Semestre'},
            request=self.request
        )
        return JsonResponse({"success": False, "errors": form.errors, "form_html": form_html}, status=400)


# ============================================================
# CRUD VIEWS (ALL FIXED MRO)
# ============================================================

class AcademicYearListView(BaseListView):
    model = AcademicYear
    list_display = ("name", "code")
    page_title = "Années académiques"
    create_url_name = "core:academic_year_create"
    detail_url_name = "core:academic_year_detail"
    update_url_name = "core:academic_year_update"
    delete_url_name = "core:academic_year_delete"


class AcademicYearCreateView(BaseCreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    success_url_name = "core:academic_year_list"
    success_message = "Année académique créée."


class AcademicYearDetailView(BaseDetailView):
    model = AcademicYear


class AcademicYearUpdateView(BaseUpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    success_url_name = "core:academic_year_list"
    success_message = "Année académique mise à jour."


class AcademicYearDeleteView(BaseDeleteView):
    model = AcademicYear
    success_url_name = "core:academic_year_list"


class SemesterListView(BaseListView):
    model = Semester
    list_display = ("name", "code")
    page_title = "Semestres"
    create_url_name = "core:semester_create"
    detail_url_name = "core:semester_detail"
    update_url_name = "core:semester_update"
    delete_url_name = "core:semester_delete"


class SemesterCreateView(BaseCreateView):
    model = Semester
    form_class = SemesterForm
    success_url_name = "core:semester_list"
    success_message = "Semestre créé."


class SemesterDetailView(BaseDetailView):
    model = Semester


class SemesterUpdateView(BaseUpdateView):
    model = Semester
    form_class = SemesterForm
    success_url_name = "core:semester_list"
    success_message = "Semestre mis à jour."


class SemesterDeleteView(BaseDeleteView):
    model = Semester
    success_url_name = "core:semester_list"


class FacultyListView(BaseListView):
    model = Faculty
    list_display = ("name", "code")
    page_title = "Facultés"
    create_url_name = "core:faculty_create"
    detail_url_name = "core:faculty_detail"
    update_url_name = "core:faculty_update"
    delete_url_name = "core:faculty_delete"


class FacultyCreateView(BaseCreateView):
    model = Faculty
    form_class = FacultyForm
    success_url_name = "core:faculty_list"
    success_message = "Faculté créée."


class FacultyDetailView(BaseDetailView):
    model = Faculty


class FacultyUpdateView(BaseUpdateView):
    model = Faculty
    form_class = FacultyForm
    success_url_name = "core:faculty_list"
    success_message = "Faculté mise à jour."


class FacultyDeleteView(BaseDeleteView):
    model = Faculty
    success_url_name = "core:faculty_list"


class DepartmentListView(BaseListView):
    model = Department
    list_display = ("name", "code", "faculty")
    page_title = "Départements"
    create_url_name = "core:department_create"
    detail_url_name = "core:department_detail"
    update_url_name = "core:department_update"
    delete_url_name = "core:department_delete"


class DepartmentCreateView(BaseCreateView):
    model = Department
    form_class = DepartmentForm
    success_url_name = "core:department_list"
    success_message = "Département créé."


class DepartmentDetailView(BaseDetailView):
    model = Department


class DepartmentUpdateView(BaseUpdateView):
    model = Department
    form_class = DepartmentForm
    success_url_name = "core:department_list"
    success_message = "Département mis à jour."


class DepartmentDeleteView(BaseDeleteView):
    model = Department
    success_url_name = "core:department_list"


class PromotionListView(BaseListView):
    model = Promotion
    list_display = ("name", "code", "department")
    page_title = "Promotions"
    create_url_name = "core:promotion_create"
    detail_url_name = "core:promotion_detail"
    update_url_name = "core:promotion_update"
    delete_url_name = "core:promotion_delete"


class PromotionCreateView(BaseCreateView):
    model = Promotion
    form_class = PromotionForm
    success_url_name = "core:promotion_list"
    success_message = "Promotion créée."


class PromotionDetailView(BaseDetailView):
    model = Promotion


class PromotionUpdateView(BaseUpdateView):
    model = Promotion
    success_url_name = "core:promotion_list"
    success_message = "Promotion mise à jour."


class PromotionDeleteView(BaseDeleteView):
    model = Promotion
    success_url_name = "core:promotion_list"
