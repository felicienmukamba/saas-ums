from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
)

from .forms import AssessmentTypeForm, AssessmentWeightingForm
from .models import AssessmentType, AssessmentWeighting


class AcademicAccessMixin:
    allowed_roles = RoleGroups.ACADEMIC


class AssessmentTypeListView(AcademicAccessMixin, BaseListView):
    model = AssessmentType
    list_display = ("name", "is_major")
    page_title = "Types d'évaluation"
    create_url_name = "assessments:type_create"
    detail_url_name = "assessments:type_detail"
    update_url_name = "assessments:type_update"
    delete_url_name = "assessments:type_delete"


class AssessmentTypeCreateView(AcademicAccessMixin, BaseCreateView):
    model = AssessmentType
    form_class = AssessmentTypeForm
    success_url_name = "assessments:type_list"
    success_message = "Type d'évaluation créé."


class AssessmentTypeDetailView(AcademicAccessMixin, BaseDetailView):
    model = AssessmentType


class AssessmentTypeUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = AssessmentType
    form_class = AssessmentTypeForm
    success_url_name = "assessments:type_list"
    success_message = "Type d'évaluation mis à jour."


class AssessmentTypeDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = AssessmentType
    success_url_name = "assessments:type_list"


class AssessmentWeightingListView(AcademicAccessMixin, BaseListView):
    model = AssessmentWeighting
    list_display = ("course_offering", "assessment_type", "weight_percentage")
    page_title = "Pondérations"
    create_url_name = "assessments:weighting_create"
    detail_url_name = "assessments:weighting_detail"
    update_url_name = "assessments:weighting_update"
    delete_url_name = "assessments:weighting_delete"


class AssessmentWeightingCreateView(AcademicAccessMixin, BaseCreateView):
    model = AssessmentWeighting
    form_class = AssessmentWeightingForm
    success_url_name = "assessments:weighting_list"
    success_message = "Pondération créée."


class AssessmentWeightingDetailView(AcademicAccessMixin, BaseDetailView):
    model = AssessmentWeighting


class AssessmentWeightingUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = AssessmentWeighting
    form_class = AssessmentWeightingForm
    success_url_name = "assessments:weighting_list"
    success_message = "Pondération mise à jour."


class AssessmentWeightingDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = AssessmentWeighting
    success_url_name = "assessments:weighting_list"
