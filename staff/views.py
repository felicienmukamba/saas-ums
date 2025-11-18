from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
)

from .forms import CourseAssignmentForm
from .models import CourseAssignment


class AcademicAccessMixin:
    allowed_roles = RoleGroups.ACADEMIC


class CourseAssignmentListView(AcademicAccessMixin, BaseListView):
    model = CourseAssignment
    list_display = ("course_offering", "teacher", "assignment_role")
    page_title = "Attributions de cours"
    create_url_name = "staff:assignment_create"
    detail_url_name = "staff:assignment_detail"
    update_url_name = "staff:assignment_update"
    delete_url_name = "staff:assignment_delete"


class CourseAssignmentCreateView(AcademicAccessMixin, BaseCreateView):
    model = CourseAssignment
    form_class = CourseAssignmentForm
    success_url_name = "staff:assignment_list"
    success_message = "Attribution créée."


class CourseAssignmentDetailView(AcademicAccessMixin, BaseDetailView):
    model = CourseAssignment


class CourseAssignmentUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = CourseAssignment
    form_class = CourseAssignmentForm
    success_url_name = "staff:assignment_list"
    success_message = "Attribution mise à jour."


class CourseAssignmentDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = CourseAssignment
    success_url_name = "staff:assignment_list"
