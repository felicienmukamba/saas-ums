from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
)

from .forms import CourseForm, CourseOfferingForm
from .models import Course, CourseOffering


class AcademicAccessMixin:
    allowed_roles = RoleGroups.ACADEMIC


class CourseListView(AcademicAccessMixin, BaseListView):
    model = Course
    list_display = ("course_name", "course_code", "credits")
    page_title = "Cours"
    create_url_name = "courses:course_create"
    detail_url_name = "courses:course_detail"
    update_url_name = "courses:course_update"
    delete_url_name = "courses:course_delete"


class CourseCreateView(AcademicAccessMixin, BaseCreateView):
    model = Course
    form_class = CourseForm
    success_url_name = "courses:course_list"
    success_message = "Cours créé."


class CourseDetailView(AcademicAccessMixin, BaseDetailView):
    model = Course


class CourseUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Course
    form_class = CourseForm
    success_url_name = "courses:course_list"
    success_message = "Cours mis à jour."


class CourseDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Course
    success_url_name = "courses:course_list"


class CourseOfferingListView(AcademicAccessMixin, BaseListView):
    model = CourseOffering
    list_display = ("course", "academic_year", "semester", "department", "promotion_name")
    page_title = "Ouvertures de cours"
    create_url_name = "courses:offering_create"
    detail_url_name = "courses:offering_detail"
    update_url_name = "courses:offering_update"
    delete_url_name = "courses:offering_delete"


class CourseOfferingCreateView(AcademicAccessMixin, BaseCreateView):
    model = CourseOffering
    form_class = CourseOfferingForm
    success_url_name = "courses:offering_list"
    success_message = "Ouverture de cours créée."


class CourseOfferingDetailView(AcademicAccessMixin, BaseDetailView):
    model = CourseOffering


class CourseOfferingUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = CourseOffering
    form_class = CourseOfferingForm
    success_url_name = "courses:offering_list"
    success_message = "Ouverture de cours mise à jour."


class CourseOfferingDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = CourseOffering
    success_url_name = "courses:offering_list"
