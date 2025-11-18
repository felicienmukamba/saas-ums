from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
)


class RoleGroups:
    """
    Regroupe les rôles métiers utilisés dans le système LMD.
    Chaque tuple représente un périmètre fonctionnel cohérent.
    """

    MANAGEMENT = ("ADMIN", "RECTORAT")
    ACADEMIC = ("ADMIN", "RECTORAT", "ACADEMIC", "PROFESSOR")
    FINANCE = ("ADMIN", "RECTORAT", "FINANCE")
    SUPPORT = ("ADMIN", "RECTORAT", "STAFF")
    ALL_STAFF = ("ADMIN", "RECTORAT", "ACADEMIC", "PROFESSOR", "FINANCE", "STAFF")
    STUDENTS = ("STUDENT",)


class RolePermissionMixin(LoginRequiredMixin):
    """
    Vérifie que l'utilisateur authentifié appartient aux rôles attendus.
    `allowed_roles` peut être redéfini sur chaque vue.
    """

    allowed_roles: tuple[str, ...] | None = RoleGroups.ALL_STAFF

    def has_role_permission(self) -> bool:
        if self.allowed_roles is None:  # aucune restriction
            return True
        user = self.request.user
        if getattr(user, "is_superuser", False):
            return True
        user_role = getattr(user, "role", None)
        return user_role in self.allowed_roles

    def dispatch(self, request, *args, **kwargs):
        if not self.has_role_permission():
            raise PermissionDenied("Vous n'avez pas les autorisations nécessaires.")
        return super().dispatch(request, *args, **kwargs)


class CrudSuccessUrlMixin:
    """
    Provides a `get_success_url` implementation that relies on a configured
    `success_url_name`. Subclasses simply declare `success_url_name` instead
    of overriding `get_success_url` repeatedly.
    """

    success_url_name: str | None = None

    def get_success_url(self):
        if not self.success_url_name:
            raise ValueError("Define `success_url_name` on the CRUD view.")
        return reverse_lazy(self.success_url_name)


class BaseListView(RolePermissionMixin, ListView):
    """
    Opinionated base `ListView` that prepares context with table meta-data so
    templates can stay generic across apps.
    """

    template_name = "generic/list.html"
    page_title: str | None = None
    list_display: list[str] | tuple[str, ...] | None = None
    create_url_name: str | None = None
    detail_url_name: str | None = None
    update_url_name: str | None = None
    delete_url_name: str | None = None

    def get_list_display(self):
        if self.list_display:
            return list(self.list_display)
        return [
            field.name
            for field in self.model._meta.fields  # type: ignore[attr-defined]
            if field.name not in ("id",)
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_names = self.get_list_display()
        model = self.model  # type: ignore[attr-defined]
        headers = [model._meta.get_field(name).verbose_name.title() for name in field_names]
        rows = [
            {"pk": obj.pk, "values": [getattr(obj, name) for name in field_names]}
            for obj in context["object_list"]
        ]
        context.update(
            {
                "page_title": self.page_title or model._meta.verbose_name_plural.title(),
                "headers": headers,
                "rows": rows,
                "create_url_name": self.create_url_name,
                "detail_url_name": self.detail_url_name,
                "update_url_name": self.update_url_name,
                "delete_url_name": self.delete_url_name,
                "has_actions": any(
                    [
                        self.detail_url_name,
                        self.update_url_name,
                        self.delete_url_name,
                    ]
                ),
            }
        )
        return context


class BaseFormView(RolePermissionMixin, CrudSuccessUrlMixin, SuccessMessageMixin):
    template_name = "generic/form.html"
    page_title: str | None = None
    success_message = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model  # type: ignore[attr-defined]
        default_title = (
            f"{self.action_label} {model._meta.verbose_name.title()}"  # type: ignore[attr-defined]
            if hasattr(self, "action_label")
            else model._meta.verbose_name.title()
        )
        context["page_title"] = self.page_title or default_title
        return context


class BaseCreateView(BaseFormView, CreateView):
    action_label = "Créer"


class BaseUpdateView(BaseFormView, UpdateView):
    action_label = "Mettre à jour"


class BaseDetailView(RolePermissionMixin, DetailView):
    template_name = "generic/detail.html"
    page_title: str | None = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model  # type: ignore[attr-defined]
        instance = context["object"]
        fields = [
            (field.verbose_name.title(), getattr(instance, field.name))
            for field in model._meta.fields  # type: ignore[attr-defined]
        ]
        context.update(
            {
                "page_title": self.page_title
                or f"Détails {model._meta.verbose_name.title()}",
                "fields": fields,
                "extra_actions": self.get_extra_actions(),
            }
        )
        return context

    def get_extra_actions(self):
        """
        Permet aux vues détaillées de fournir des actions contextuelles
        (téléchargements PDF, raccourcis métier, etc.).
        """
        return []


class BaseDeleteView(RolePermissionMixin, CrudSuccessUrlMixin, DeleteView):
    template_name = "generic/confirm_delete.html"
    page_title: str | None = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model  # type: ignore[attr-defined]
        context["page_title"] = self.page_title or f"Confirmer la suppression"
        context["object_name"] = str(context["object"])
        context["model_verbose_name"] = model._meta.verbose_name.title()
        return context

