from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
)

from .forms import AcademicFeeForm, FeeCategoryForm
from .models import AcademicFee, FeeCategory


class FinanceAccessMixin:
    allowed_roles = RoleGroups.FINANCE


class FeeCategoryListView(FinanceAccessMixin, BaseListView):
    model = FeeCategory
    list_display = ("name", "description")
    page_title = "Catégories de frais"
    create_url_name = "fees:category_create"
    detail_url_name = "fees:category_detail"
    update_url_name = "fees:category_update"
    delete_url_name = "fees:category_delete"


class FeeCategoryCreateView(FinanceAccessMixin, BaseCreateView):
    model = FeeCategory
    form_class = FeeCategoryForm
    success_url_name = "fees:category_list"
    success_message = "Catégorie ajoutée."


class FeeCategoryDetailView(FinanceAccessMixin, BaseDetailView):
    model = FeeCategory


class FeeCategoryUpdateView(FinanceAccessMixin, BaseUpdateView):
    model = FeeCategory
    form_class = FeeCategoryForm
    success_url_name = "fees:category_list"
    success_message = "Catégorie mise à jour."


class FeeCategoryDeleteView(FinanceAccessMixin, BaseDeleteView):
    model = FeeCategory
    success_url_name = "fees:category_list"


class AcademicFeeListView(FinanceAccessMixin, BaseListView):
    model = AcademicFee
    list_display = ("category", "year", "semester", "amount")
    page_title = "Frais académiques"
    create_url_name = "fees:academic_fee_create"
    detail_url_name = "fees:academic_fee_detail"
    update_url_name = "fees:academic_fee_update"
    delete_url_name = "fees:academic_fee_delete"


class AcademicFeeCreateView(FinanceAccessMixin, BaseCreateView):
    model = AcademicFee
    form_class = AcademicFeeForm
    success_url_name = "fees:academic_fee_list"
    success_message = "Frais académique ajouté."


class AcademicFeeDetailView(FinanceAccessMixin, BaseDetailView):
    model = AcademicFee


class AcademicFeeUpdateView(FinanceAccessMixin, BaseUpdateView):
    model = AcademicFee
    form_class = AcademicFeeForm
    success_url_name = "fees:academic_fee_list"
    success_message = "Frais académique mis à jour."


class AcademicFeeDeleteView(FinanceAccessMixin, BaseDeleteView):
    model = AcademicFee
    success_url_name = "fees:academic_fee_list"
