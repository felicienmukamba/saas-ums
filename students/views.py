from django.db.models import Avg, Q, Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from ums.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
    RoleGroups,
    RolePermissionMixin,
)
from ums.pdf import (
    Paragraph,
    Spacer,
    build_pdf_response,
    build_table,
    get_pdf_styles,
    lmd_decision,
    lmd_mention,
)

from .forms import (
    AddressForm,
    ContactForm,
    DiplomaForm,
    ParentForm,
    SponsorForm,
    StudentForm,
    StudentSponsorForm,
)
from .models import Address, Contact, Diploma, Parent, Sponsor, Student, StudentSponsor

from enrollment.models import Enrollment
from grades.models import Grade


class AcademicAccessMixin:
    allowed_roles = RoleGroups.ACADEMIC


class AddressListView(AcademicAccessMixin, BaseListView):
    model = Address
    list_display = ("street", "quarter", "city_commune")
    page_title = "Adresses"
    create_url_name = "students:address_create"
    detail_url_name = "students:address_detail"
    update_url_name = "students:address_update"
    delete_url_name = "students:address_delete"


class AddressCreateView(AcademicAccessMixin, BaseCreateView):
    model = Address
    form_class = AddressForm
    success_url_name = "students:address_list"
    success_message = "Adresse créée."


class AddressDetailView(AcademicAccessMixin, BaseDetailView):
    model = Address


class AddressUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Address
    form_class = AddressForm
    success_url_name = "students:address_list"
    success_message = "Adresse mise à jour."


class AddressDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Address
    success_url_name = "students:address_list"


class ContactListView(AcademicAccessMixin, BaseListView):
    model = Contact
    list_display = ("email", "phone_number", "whatsapp_number")
    page_title = "Contacts"
    create_url_name = "students:contact_create"
    detail_url_name = "students:contact_detail"
    update_url_name = "students:contact_update"
    delete_url_name = "students:contact_delete"


class ContactCreateView(AcademicAccessMixin, BaseCreateView):
    model = Contact
    form_class = ContactForm
    success_url_name = "students:contact_list"
    success_message = "Contact créé."


class ContactDetailView(AcademicAccessMixin, BaseDetailView):
    model = Contact


class ContactUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Contact
    form_class = ContactForm
    success_url_name = "students:contact_list"
    success_message = "Contact mis à jour."


class ContactDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Contact
    success_url_name = "students:contact_list"


class DiplomaListView(AcademicAccessMixin, BaseListView):
    model = Diploma
    list_display = ("diploma_number", "institution", "obtaining_year", "section")
    page_title = "Diplômes"
    create_url_name = "students:diploma_create"
    detail_url_name = "students:diploma_detail"
    update_url_name = "students:diploma_update"
    delete_url_name = "students:diploma_delete"


class DiplomaCreateView(AcademicAccessMixin, BaseCreateView):
    model = Diploma
    form_class = DiplomaForm
    success_url_name = "students:diploma_list"
    success_message = "Diplôme créé."


class DiplomaDetailView(AcademicAccessMixin, BaseDetailView):
    model = Diploma


class DiplomaUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Diploma
    form_class = DiplomaForm
    success_url_name = "students:diploma_list"
    success_message = "Diplôme mis à jour."


class DiplomaDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Diploma
    success_url_name = "students:diploma_list"


class ParentListView(AcademicAccessMixin, BaseListView):
    model = Parent
    list_display = ("first_name", "last_name", "phone_number")
    page_title = "Parents"
    create_url_name = "students:parent_create"
    detail_url_name = "students:parent_detail"
    update_url_name = "students:parent_update"
    delete_url_name = "students:parent_delete"


class ParentCreateView(AcademicAccessMixin, BaseCreateView):
    model = Parent
    form_class = ParentForm
    success_url_name = "students:parent_list"
    success_message = "Parent créé."


class ParentDetailView(AcademicAccessMixin, BaseDetailView):
    model = Parent


class ParentUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Parent
    form_class = ParentForm
    success_url_name = "students:parent_list"
    success_message = "Parent mis à jour."


class ParentDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Parent
    success_url_name = "students:parent_list"


class SponsorListView(AcademicAccessMixin, BaseListView):
    model = Sponsor
    list_display = ("organization", "sponsor_type", "phone_number")
    page_title = "Sponsors"
    create_url_name = "students:sponsor_create"
    detail_url_name = "students:sponsor_detail"
    update_url_name = "students:sponsor_update"
    delete_url_name = "students:sponsor_delete"


class SponsorCreateView(AcademicAccessMixin, BaseCreateView):
    model = Sponsor
    form_class = SponsorForm
    success_url_name = "students:sponsor_list"
    success_message = "Sponsor créé."


class SponsorDetailView(AcademicAccessMixin, BaseDetailView):
    model = Sponsor


class SponsorUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Sponsor
    form_class = SponsorForm
    success_url_name = "students:sponsor_list"
    success_message = "Sponsor mis à jour."


class SponsorDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Sponsor
    success_url_name = "students:sponsor_list"


class StudentListView(AcademicAccessMixin, BaseListView):
    model = Student
    list_display = ("matricule", "first_name", "last_name", "gender", "contact")
    page_title = "Étudiants"
    create_url_name = "students:student_create"
    detail_url_name = "students:student_detail"
    update_url_name = "students:student_update"
    delete_url_name = "students:student_delete"


class StudentCreateView(AcademicAccessMixin, BaseCreateView):
    model = Student
    form_class = StudentForm
    success_url_name = "students:student_list"
    success_message = "Étudiant créé."


class StudentDetailView(AcademicAccessMixin, BaseDetailView):
    model = Student

    def get_extra_actions(self):
        obj = getattr(self, "object", None) or self.get_object()
        actions = [
            {
                "label": "État de sortie (PDF)",
                "url": reverse("students:student_exit_pdf", args=[obj.pk]),
            }
        ]
        latest_enrollment = (
            Enrollment.objects.filter(student=obj).select_related("year").order_by("-year__name").first()
        )
        if latest_enrollment:
            actions.append(
                {
                    "label": "Dernière fiche d'inscription",
                    "url": reverse("enrollment:enrollment_detail", args=[latest_enrollment.pk]),
                    "badge": "Voir",
                }
            )
        return actions


class StudentUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Student
    form_class = StudentForm
    success_url_name = "students:student_list"
    success_message = "Étudiant mis à jour."


class StudentDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Student
    success_url_name = "students:student_list"


class StudentSponsorListView(AcademicAccessMixin, BaseListView):
    model = StudentSponsor
    list_display = ("student", "sponsor", "contribution_type", "annual_commitment", "is_primary")
    page_title = "Parrainages"
    create_url_name = "students:student_sponsor_create"
    detail_url_name = "students:student_sponsor_detail"
    update_url_name = "students:student_sponsor_update"
    delete_url_name = "students:student_sponsor_delete"


class StudentSponsorCreateView(AcademicAccessMixin, BaseCreateView):
    model = StudentSponsor
    form_class = StudentSponsorForm
    success_url_name = "students:student_sponsor_list"
    success_message = "Parrainage créé."


class StudentSponsorDetailView(AcademicAccessMixin, BaseDetailView):
    model = StudentSponsor


class StudentSponsorUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = StudentSponsor
    form_class = StudentSponsorForm
    success_url_name = "students:student_sponsor_list"
    success_message = "Parrainage mis à jour."


class StudentSponsorDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = StudentSponsor
    success_url_name = "students:student_sponsor_list"


class StudentPDFBaseView(RolePermissionMixin, View):
    allowed_roles = RoleGroups.ACADEMIC


class StudentExitCertificatePDFView(StudentPDFBaseView):
    """
    Génère un état de sortie consolidé conforme aux attendus LMD (RDC).
    """

    def get(self, request, pk):
        student = get_object_or_404(
            Student.objects.select_related("address", "contact", "diploma"),
            pk=pk,
        )
        enrollments = (
            Enrollment.objects.filter(student=student)
            .select_related("year", "semester", "faculty", "department")
            .order_by("year__name", "semester__name")
        )
        grade_stats = (
            Grade.objects.filter(enrollment__student=student)
            .aggregate(
                average=Avg("score"),
                validated_credits=Sum(
                    "course_offering__course__credits",
                    filter=Q(score__gte=50),
                ),
            )
        )
        styles = get_pdf_styles()

        def build():
            flow = [
                Paragraph("République Démocratique du Congo", styles["Small"]),
                Paragraph("ÉTAT DE SORTIE - SYSTÈME LMD", styles["Title"]),
                Spacer(1, 12),
            ]
            identity_rows = [
                ["Nom complet", f"{student.last_name} {student.first_name}".upper()],
                ["Matricule", student.matricule or "-"],
                ["Genre", student.get_gender_display() if hasattr(student, "get_gender_display") else student.gender],
                ["Nationalité", student.nationality or "-"],
                ["Date / Lieu de naissance", f"{student.birth_date} - {student.birth_place}"],
            ]
            if student.contact:
                identity_rows.append(["Email", student.contact.email])
                identity_rows.append(["Téléphone", student.contact.phone_number])
            flow.append(Paragraph("Informations personnelles", styles["Heading2"]))
            flow.append(build_table(identity_rows, col_widths=[160, 300]))

            if enrollments:
                enrollment_table = [
                    ["Année académique", "Semestre", "Faculté", "Département", "Promotion"],
                ]
                for enrollment in enrollments:
                    enrollment_table.append(
                        [
                            enrollment.year.name,
                            enrollment.semester.name,
                            enrollment.faculty.name,
                            enrollment.department.name if enrollment.department else "-",
                            enrollment.promotion,
                        ]
                    )
                flow.append(Spacer(1, 12))
                flow.append(Paragraph("Parcours académique", styles["Heading2"]))
                flow.append(build_table(enrollment_table, header=True))

            summary_rows = [
                ["Crédits validés", grade_stats["validated_credits"] or 0],
                [
                    "Moyenne générale",
                    f"{grade_stats['average']:.2f}" if grade_stats["average"] is not None else "N/A",
                ],
                ["Mention", lmd_mention(grade_stats["average"])],
                ["Décision", lmd_decision(grade_stats["average"])],
            ]
            flow.append(Spacer(1, 12))
            flow.append(Paragraph("Synthèse académique LMD", styles["Heading2"]))
            flow.append(build_table(summary_rows, col_widths=[200, 200]))

            flow.append(Spacer(1, 18))
            flow.append(
                Paragraph(
                    "Conformément aux exigences du système LMD en RDC, cet état de sortie atteste du parcours "
                    "académique de l'étudiant, de la validation des unités d'enseignement et de la décision finale "
                    "de la faculté.",
                    styles["BodyText"],
                )
            )
            return flow

        filename = f"etat-sortie-{student.matricule or student.pk}.pdf"
        return build_pdf_response(filename, build)
