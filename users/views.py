from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView

from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
)

from .forms import UserForm, LoginForm, ProfileEditForm, CustomPasswordChangeForm

User = get_user_model()


class RectorateAccessMixin:
    allowed_roles = RoleGroups.MANAGEMENT


class UserListView(RectorateAccessMixin, BaseListView):
    model = User
    list_display = ("email", "first_name", "last_name", "role", "is_active")
    page_title = "Utilisateurs"
    create_url_name = "users:user_create"
    detail_url_name = "users:user_detail"
    update_url_name = "users:user_update"
    delete_url_name = "users:user_delete"


class UserCreateView(RectorateAccessMixin, BaseCreateView):
    model = User
    form_class = UserForm
    success_url_name = "users:user_list"
    success_message = "Utilisateur créé."


class UserDetailView(RectorateAccessMixin, BaseDetailView):
    model = User


class UserUpdateView(RectorateAccessMixin, BaseUpdateView):
    model = User
    form_class = UserForm
    success_url_name = "users:user_list"
    success_message = "Utilisateur mis à jour."


class UserDeleteView(RectorateAccessMixin, BaseDeleteView):
    model = User
    success_url_name = "users:user_list"


# ====================================================================
# Authentication Views
# ====================================================================

class LoginView(View):
    template_name = "users/login.html"
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.get_full_name() or user.email}!")
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("core:dashboard")
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        messages.info(request, "Vous avez été déconnecté avec succès.")
        return redirect("users:login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, View):
    template_name = "users/profile_edit.html"
    form_class = ProfileEditForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect("users:profile")
        return render(request, self.template_name, {"form": form})


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = "users/change_password.html"
    form_class = CustomPasswordChangeForm

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été modifié avec succès.")
            return redirect("users:profile")
        return render(request, self.template_name, {"form": form})
