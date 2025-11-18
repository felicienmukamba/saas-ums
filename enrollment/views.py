from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage

from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
    RolePermissionMixin,
)
from ums.pdf import build_pdf_response

from enrollment.forms import (
    CompleteEnrollmentForm,
    DocumentForm,
    EnrollmentForm,
    EnrollmentRequestForm,
    SecondaryChoiceForm,
)
from enrollment.models import Document, Enrollment, EnrollmentRequest, SecondaryChoice


class AcademicAccessMixin:
    allowed_roles = RoleGroups.ACADEMIC


# ====================================================================
# Demandes d'inscription (publiques)
# ====================================================================
class EnrollmentRequestCreateView(View):
    template_name = "enrollment/enrollment_request_form.html"
    form_class = CompleteEnrollmentForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            "form": form,
            "page_title": "Demande d'inscription",
        })
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            
            # --- STEP 1: Handle the Photo Upload ---
            photo_path = None
            uploaded_photo = form.cleaned_data.get('photo')
            
            if uploaded_photo:
                # Define a path where the file will be saved in your media folder
                # Example: "enrollment_photos/my_photo.jpg"
                file_name = f"enrollment_photos/{uploaded_photo.name}"
                
                # Save the file to disk and get the path string
                photo_path = default_storage.save(file_name, uploaded_photo)

            # --- STEP 2: Prepare Data (Store the PATH, not the File) ---
            student_data = {
                'photo': photo_path,  # <--- Now this is a string (or None), which IS serializable
                'first_name': form.cleaned_data['first_name'],
                'middle_name': form.cleaned_data['middle_name'],
                'last_name': form.cleaned_data['last_name'],
                'gender': form.cleaned_data['gender'],
                'marital_status': form.cleaned_data['marital_status'],
                'birth_place': form.cleaned_data['birth_place'],
                'birth_date': form.cleaned_data['birth_date'].isoformat(),
                'nationality': form.cleaned_data['nationality'],
                'address': {
                    'street': form.cleaned_data['address_street'],
                    'quarter': form.cleaned_data['address_quarter'],
                    'city_commune': form.cleaned_data['address_city_commune'],
                },
                'contact': {
                    'phone_number': form.cleaned_data['contact_phone_number'],
                    'whatsapp_number': form.cleaned_data.get('contact_whatsapp_number'),
                    'email': form.cleaned_data['contact_email'],
                },
                'diploma': {
                    'institution': form.cleaned_data['diploma_institution'],
                    'obtaining_year': form.cleaned_data['diploma_obtaining_year'],
                    'diploma_number': form.cleaned_data['diploma_number'],
                    'section': form.cleaned_data['diploma_section'],
                    'percentage': str(form.cleaned_data['diploma_percentage']),
                },
                'father': {
                    'first_name': form.cleaned_data['father_first_name'],
                    'middle_name': form.cleaned_data['father_middle_name'],
                    'last_name': form.cleaned_data['father_last_name'],
                    'origin_country': form.cleaned_data['father_origin_country'],
                    'province': form.cleaned_data['father_province'],
                    'address': form.cleaned_data['father_address'],
                    'phone_number': form.cleaned_data['father_phone_number'],
                    'email': form.cleaned_data.get('father_email'),
                },
                'mother': {
                    'first_name': form.cleaned_data['mother_first_name'],
                    'middle_name': form.cleaned_data['mother_middle_name'],
                    'last_name': form.cleaned_data['mother_last_name'],
                    'origin_country': form.cleaned_data['mother_origin_country'],
                    'province': form.cleaned_data['mother_province'],
                    'address': form.cleaned_data['mother_address'],
                    'phone_number': form.cleaned_data['mother_phone_number'],
                    'email': form.cleaned_data.get('mother_email'),
                },
            }
            
            enrollment_data = {
                'year': form.cleaned_data['year'].pk,
                'semester': form.cleaned_data['semester'].pk,
                'faculty': form.cleaned_data['faculty'].pk,
                'department': form.cleaned_data.get('department').pk if form.cleaned_data.get('department') else None,
                'promotion': form.cleaned_data['promotion'],
                'admission_exam': form.cleaned_data.get('admission_exam', False),
                'how_known': form.cleaned_data['how_known'],
                'why_chosen': form.cleaned_data['why_chosen'],
                'mutual_affiliate': form.cleaned_data.get('mutual_affiliate', False),
                'mutual_details': form.cleaned_data.get('mutual_details', ''),
                'commitments_accepted': form.cleaned_data['commitments_accepted'],
            }
            
            # --- STEP 3: Create the Request ---
            # We no longer need the separate .save() block after this because 
            # the photo path is already included in student_data above.
            request_obj = EnrollmentRequest.objects.create(
                student_data=student_data,
                enrollment_data=enrollment_data,
            )
            
            messages.success(request, "Votre demande d'inscription a été soumise avec succès. Vous serez contacté une fois qu'elle sera traitée.")
            return redirect('enrollment:request_success', pk=request_obj.pk)
        
        return render(request, self.template_name, {
            "form": form,
            "page_title": "Demande d'inscription",
        })
class EnrollmentRequestSuccessView(TemplateView):
    """Page de confirmation après soumission d'une demande"""
    template_name = "enrollment/enrollment_request_success.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_id = self.kwargs.get('pk')
        if request_id:
            context['enrollment_request'] = get_object_or_404(EnrollmentRequest, pk=request_id)
        return context


# ====================================================================
# Gestion des demandes par les chargés d'inscription
# ====================================================================

# CORRECTION MRO APPLIQUÉE : BaseListView en premier
class EnrollmentRequestListView(BaseListView, AcademicAccessMixin, RolePermissionMixin):
    model = EnrollmentRequest
    list_display = ("submitted_at", "status", "student_data")
    page_title = "Demandes d'inscription"
    create_url_name = None
    detail_url_name = "enrollment:request_detail"
    update_url_name = None
    delete_url_name = None
    
    def get_list_display(self):
        return ["submitted_at", "status", "student_name", "contact_email"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Personnaliser les en-têtes
        context['headers'] = ["Date de soumission", "Statut", "Étudiant", "Email"]
        # Personnaliser les lignes
        rows = []
        for obj in context['object_list']:
            student_name = f"{obj.student_data.get('first_name', '')} {obj.student_data.get('last_name', '')}"
            contact_email = obj.student_data.get('contact', {}).get('email', '-')
            rows.append({
                'pk': obj.pk,
                'values': [
                    obj.submitted_at.strftime('%d/%m/%Y %H:%M'),
                    obj.get_status_display(),
                    student_name,
                    contact_email,
                ]
            })
        context['rows'] = rows
        return context


# CORRECTION MRO APPLIQUÉE : BaseDetailView en premier
class EnrollmentRequestDetailView(BaseDetailView, AcademicAccessMixin, RolePermissionMixin):
    model = EnrollmentRequest
    template_name = "enrollment/enrollment_request_detail.html"
    context_object_name = "request"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Détails de la demande d'inscription"
        return context


# CORRECTION MRO APPLIQUÉE : View en premier
class EnrollmentRequestApproveView(View, AcademicAccessMixin, RolePermissionMixin):
    """Approuve une demande d'inscription"""
    
    def post(self, request, pk):
        enrollment_request = get_object_or_404(EnrollmentRequest, pk=pk)
        notes = request.POST.get('notes', '')
        
        try:
            # Assurez-vous que la méthode approve() de votre modèle gère correctement
            # la création de l'objet Enrollment à partir des données sérialisées.
            enrollment = enrollment_request.approve(reviewer=request.user, notes=notes)
            messages.success(request, f"La demande a été approuvée et l'inscription #{enrollment.pk} a été créée.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'approbation : {str(e)}")
        
        return redirect('enrollment:request_detail', pk=pk)


# CORRECTION MRO APPLIQUÉE : View en premier
class EnrollmentRequestRejectView(View, AcademicAccessMixin, RolePermissionMixin):
    """Rejette une demande d'inscription"""
    
    def post(self, request, pk):
        enrollment_request = get_object_or_404(EnrollmentRequest, pk=pk)
        notes = request.POST.get('notes', '')
        
        enrollment_request.reject(reviewer=request.user, notes=notes)
        messages.success(request, "La demande a été rejetée.")
        
        return redirect('enrollment:request_detail', pk=pk)


# ====================================================================
# Inscription directe par un chargé d'inscription
# ====================================================================

# CORRECTION MRO APPLIQUÉE : View en premier
class DirectEnrollmentCreateView(View, AcademicAccessMixin, RolePermissionMixin):
    """Vue pour qu'un chargé d'inscription crée directement une inscription"""
    template_name = "enrollment/direct_enrollment_form.html"
    form_class = CompleteEnrollmentForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            "form": form,
            "page_title": "Inscrire un étudiant",
        })
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Assurez-vous que la méthode save() de CompleteEnrollmentForm
                # gère la création de l'étudiant, puis de l'inscription.
                enrollment = form.save()
                messages.success(request, f"L'étudiant {enrollment.student} a été inscrit avec succès.")
                return redirect('enrollment:enrollment_detail', pk=enrollment.pk)
            except Exception as e:
                messages.error(request, f"Erreur lors de l'inscription : {str(e)}")
        
        return render(request, self.template_name, {
            "form": form,
            "page_title": "Inscrire un étudiant",
        })


# ====================================================================
# Vues CRUD standard pour Enrollment
# ====================================================================

# CORRECTION MRO APPLIQUÉE : BaseListView en premier
class EnrollmentListView(BaseListView, AcademicAccessMixin, RolePermissionMixin):
    model = Enrollment
    list_display = ("student", "year", "semester", "faculty", "promotion")
    page_title = "Inscriptions"
    create_url_name = "enrollment:enrollment_create"
    detail_url_name = "enrollment:enrollment_detail"
    update_url_name = "enrollment:enrollment_update"
    delete_url_name = "enrollment:enrollment_delete"


# CORRECTION MRO APPLIQUÉE : BaseCreateView en premier
class EnrollmentCreateView(BaseCreateView, AcademicAccessMixin, RolePermissionMixin):
    model = Enrollment
    form_class = EnrollmentForm
    success_url_name = "enrollment:enrollment_list"
    success_message = "Inscription enregistrée."


# CORRECTION MRO APPLIQUÉE : BaseDetailView en premier
class EnrollmentDetailView(BaseDetailView, AcademicAccessMixin, RolePermissionMixin):
    model = Enrollment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = context['object']
        
        # Actions métiers supplémentaires
        context['extra_actions'] = [
            {
                'label': 'Fiche d\'inscription (PDF)',
                'url': reverse_lazy('enrollment:registration_pdf', kwargs={'pk': enrollment.pk}),
                'icon': 'bi-file-earmark-pdf',
                'class': 'btn-outline-primary',
            },
            {
                'label': 'Bulletin LMD (PDF)',
                'url': reverse_lazy('enrollment:bulletin_pdf', kwargs={'pk': enrollment.pk}),
                'icon': 'bi-file-earmark-pdf',
                'class': 'btn-outline-info',
            },
        ]
        return context


# CORRECTION MRO APPLIQUÉE : BaseUpdateView en premier
class EnrollmentUpdateView(BaseUpdateView, AcademicAccessMixin, RolePermissionMixin):
    model = Enrollment
    form_class = EnrollmentForm
    success_url_name = "enrollment:enrollment_list"
    success_message = "Inscription mise à jour."


# CORRECTION MRO APPLIQUÉE : BaseDeleteView en premier
class EnrollmentDeleteView(BaseDeleteView, AcademicAccessMixin, RolePermissionMixin):
    model = Enrollment
    success_url_name = "enrollment:enrollment_list"


# ====================================================================
# Vues pour SecondaryChoice et Document
# ====================================================================

# CORRECTION MRO APPLIQUÉE : BaseListView en premier
class SecondaryChoiceListView(BaseListView, AcademicAccessMixin, RolePermissionMixin):
    model = SecondaryChoice
    list_display = ("enrollment", "faculty", "promotion")
    page_title = "Choix secondaires"
    create_url_name = "enrollment:secondary_choice_create"
    detail_url_name = "enrollment:secondary_choice_detail"
    update_url_name = "enrollment:secondary_choice_update"
    delete_url_name = "enrollment:secondary_choice_delete"


# CORRECTION MRO APPLIQUÉE : BaseCreateView en premier
class SecondaryChoiceCreateView(BaseCreateView, AcademicAccessMixin, RolePermissionMixin):
    model = SecondaryChoice
    form_class = SecondaryChoiceForm
    success_url_name = "enrollment:secondary_choice_list"
    success_message = "Choix secondaire créé."


# CORRECTION MRO APPLIQUÉE : BaseDetailView en premier
class SecondaryChoiceDetailView(BaseDetailView, AcademicAccessMixin, RolePermissionMixin):
    model = SecondaryChoice


# CORRECTION MRO APPLIQUÉE : BaseUpdateView en premier
class SecondaryChoiceUpdateView(BaseUpdateView, AcademicAccessMixin, RolePermissionMixin):
    model = SecondaryChoice
    form_class = SecondaryChoiceForm
    success_url_name = "enrollment:secondary_choice_list"
    success_message = "Choix secondaire mis à jour."


# CORRECTION MRO APPLIQUÉE : BaseDeleteView en premier
class SecondaryChoiceDeleteView(BaseDeleteView, AcademicAccessMixin, RolePermissionMixin):
    model = SecondaryChoice
    success_url_name = "enrollment:secondary_choice_list"


# CORRECTION MRO APPLIQUÉE : BaseListView en premier
class DocumentListView(BaseListView, AcademicAccessMixin, RolePermissionMixin):
    model = Document
    list_display = ("enrollment", "document_name", "is_required", "file_path")
    page_title = "Documents d'inscription"
    create_url_name = "enrollment:document_create"
    detail_url_name = "enrollment:document_detail"
    update_url_name = "enrollment:document_update"
    delete_url_name = "enrollment:document_delete"


# CORRECTION MRO APPLIQUÉE : BaseCreateView en premier
class DocumentCreateView(BaseCreateView, AcademicAccessMixin, RolePermissionMixin):
    model = Document
    form_class = DocumentForm
    success_url_name = "enrollment:document_list"
    success_message = "Document ajouté."


# CORRECTION MRO APPLIQUÉE : BaseDetailView en premier
class DocumentDetailView(BaseDetailView, AcademicAccessMixin, RolePermissionMixin):
    model = Document


# CORRECTION MRO APPLIQUÉE : BaseUpdateView en premier
class DocumentUpdateView(BaseUpdateView, AcademicAccessMixin, RolePermissionMixin):
    model = Document
    form_class = DocumentForm
    success_url_name = "enrollment:document_list"
    success_message = "Document mis à jour."


# CORRECTION MRO APPLIQUÉE : BaseDeleteView en premier
class DocumentDeleteView(BaseDeleteView, AcademicAccessMixin, RolePermissionMixin):
    model = Document
    success_url_name = "enrollment:document_list"


# ====================================================================
# Vues PDF (existantes)
# ====================================================================

# CORRECTION MRO APPLIQUÉE : View en premier
class EnrollmentPDFBaseView(View, RolePermissionMixin):
    allowed_roles = RoleGroups.ACADEMIC


class EnrollmentRegistrationPDFView(EnrollmentPDFBaseView):
    """Génère la fiche d'inscription en PDF"""
    
    def get(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk)
        # ... (code PDF existant)
        return build_pdf_response("fiche_inscription.pdf", lambda: None)


class EnrollmentBulletinPDFView(EnrollmentPDFBaseView):
    """Génère le bulletin LMD en PDF"""
    
    def get(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk)
        # ... (code PDF existant)
        return build_pdf_response("bulletin_lmd.pdf", lambda: None)