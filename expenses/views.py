from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
)

from .forms import ExpenseCategoryForm, ExpenseForm
from .models import Expense, ExpenseCategory


class FinanceAccessMixin:
    allowed_roles = RoleGroups.FINANCE


class ExpenseCategoryListView(FinanceAccessMixin, BaseListView):
    model = ExpenseCategory
    list_display = ("name", "description")
    page_title = "Catégories de dépense"
    create_url_name = "expenses:category_create"
    detail_url_name = "expenses:category_detail"
    update_url_name = "expenses:category_update"
    delete_url_name = "expenses:category_delete"


class ExpenseCategoryCreateView(FinanceAccessMixin, BaseCreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    success_url_name = "expenses:category_list"
    success_message = "Catégorie créée."


class ExpenseCategoryDetailView(FinanceAccessMixin, BaseDetailView):
    model = ExpenseCategory


class ExpenseCategoryUpdateView(FinanceAccessMixin, BaseUpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    success_url_name = "expenses:category_list"
    success_message = "Catégorie mise à jour."


class ExpenseCategoryDeleteView(FinanceAccessMixin, BaseDeleteView):
    model = ExpenseCategory
    success_url_name = "expenses:category_list"


class ExpenseListView(FinanceAccessMixin, BaseListView):
    model = Expense
    list_display = ("category", "year", "expense_date", "amount", "beneficiary")
    page_title = "Dépenses"
    create_url_name = "expenses:expense_create"
    detail_url_name = "expenses:expense_detail"
    update_url_name = "expenses:expense_update"
    delete_url_name = "expenses:expense_delete"


class ExpenseCreateView(FinanceAccessMixin, BaseCreateView):
    model = Expense
    form_class = ExpenseForm
    success_url_name = "expenses:expense_list"
    success_message = "Dépense enregistrée."


class ExpenseDetailView(FinanceAccessMixin, BaseDetailView):
    model = Expense


class ExpenseUpdateView(FinanceAccessMixin, BaseUpdateView):
    model = Expense
    form_class = ExpenseForm
    success_url_name = "expenses:expense_list"
    success_message = "Dépense mise à jour."


class ExpenseDeleteView(FinanceAccessMixin, BaseDeleteView):
    model = Expense
    success_url_name = "expenses:expense_list"
