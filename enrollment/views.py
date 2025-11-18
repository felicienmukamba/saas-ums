from django.db.models import Avg
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

from .forms import DocumentForm, EnrollmentForm, SecondaryChoiceForm
from .models import Document, Enrollment, SecondaryChoice
from grades.models import Grade


class AcademicAccessMixin:
    allowed_roles = RoleGroups.ACADEMIC


class EnrollmentListView(AcademicAccessMixin, BaseListView):
    model = Enrollment
    list_display = ("student", "year", "semester", "faculty", "promotion")
    page_title = "Inscriptions"
    create_url_name = "enrollment:enrollment_create"
    detail_url_name = "enrollment:enrollment_detail"
    update_url_name = "enrollment:enrollment_update"
    delete_url_name = "enrollment:enrollment_delete"


class EnrollmentCreateView(AcademicAccessMixin, BaseCreateView):
    model = Enrollment
    form_class = EnrollmentForm
    success_url_name = "enrollment:enrollment_list"
    success_message = "Inscription enregistrée."


class EnrollmentDetailView(AcademicAccessMixin, BaseDetailView):
    model = Enrollment

    def get_extra_actions(self):
        obj = getattr(self, "object", None) or self.get_object()
        return [
            {
                "label": "Fiche d'inscription (PDF)",
                "url": reverse("enrollment:enrollment_registration_pdf", args=[obj.pk]),
            },
            {
                "label": "Bulletin LMD (PDF)",
                "url": reverse("enrollment:enrollment_bulletin_pdf", args=[obj.pk]),
            },
        ]


class EnrollmentUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    success_url_name = "enrollment:enrollment_list"
    success_message = "Inscription mise à jour."


class EnrollmentDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Enrollment
    success_url_name = "enrollment:enrollment_list"


class SecondaryChoiceListView(AcademicAccessMixin, BaseListView):
    model = SecondaryChoice
    list_display = ("enrollment", "faculty", "promotion")
    page_title = "Choix secondaires"
    create_url_name = "enrollment:secondary_choice_create"
    detail_url_name = "enrollment:secondary_choice_detail"
    update_url_name = "enrollment:secondary_choice_update"
    delete_url_name = "enrollment:secondary_choice_delete"


class SecondaryChoiceCreateView(AcademicAccessMixin, BaseCreateView):
    model = SecondaryChoice
    form_class = SecondaryChoiceForm
    success_url_name = "enrollment:secondary_choice_list"
    success_message = "Choix secondaire créé."


class SecondaryChoiceDetailView(AcademicAccessMixin, BaseDetailView):
    model = SecondaryChoice


class SecondaryChoiceUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = SecondaryChoice
    form_class = SecondaryChoiceForm
    success_url_name = "enrollment:secondary_choice_list"
    success_message = "Choix secondaire mis à jour."


class SecondaryChoiceDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = SecondaryChoice
    success_url_name = "enrollment:secondary_choice_list"


class DocumentListView(AcademicAccessMixin, BaseListView):
    model = Document
    list_display = ("enrollment", "document_name", "is_required", "file_path")
    page_title = "Documents d'inscription"
    create_url_name = "enrollment:document_create"
    detail_url_name = "enrollment:document_detail"
    update_url_name = "enrollment:document_update"
    delete_url_name = "enrollment:document_delete"


class DocumentCreateView(AcademicAccessMixin, BaseCreateView):
    model = Document
    form_class = DocumentForm
    success_url_name = "enrollment:document_list"
    success_message = "Document ajouté."


class DocumentDetailView(AcademicAccessMixin, BaseDetailView):
    model = Document


class DocumentUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Document
    form_class = DocumentForm
    success_url_name = "enrollment:document_list"
    success_message = "Document mis à jour."


class DocumentDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Document
    success_url_name = "enrollment:document_list"


class EnrollmentPDFBaseView(RolePermissionMixin, View):
    allowed_roles = RoleGroups.ACADEMIC


class EnrollmentRegistrationPDFView(EnrollmentPDFBaseView):
    """
    Fiche d'inscription détaillée conforme aux usages des secrétariats académiques.
    """

    def get(self, request, pk):
        enrollment = get_object_or_404(
            Enrollment.objects.select_related(
                "student",
                "student__address",
                "student__contact",
                "year",
                "semester",
                "faculty",
                "department",
            ),
            pk=pk,
        )
        documents = Document.objects.filter(enrollment=enrollment)
        secondary_choice = SecondaryChoice.objects.filter(enrollment=enrollment).select_related("faculty", "department").first()
        styles = get_pdf_styles()

        def build():
            student = enrollment.student
            flow = [
                Paragraph("FICHE D'INSCRIPTION - SYSTÈME LMD", styles["Title"]),
                Spacer(1, 12),
            ]
            identity_rows = [
                ["Étudiant", str(student)],
                ["Matricule", student.matricule or "-"],
                ["Promotion demandée", enrollment.promotion],
                ["Année / Semestre", f"{enrollment.year.name} - {enrollment.semester.name}"],
                ["Faculté / Département", f"{enrollment.faculty.name} / {enrollment.department or '-'}"],
            ]
            if student.contact:
                identity_rows.append(["Contact", f"{student.contact.email} / {student.contact.phone_number}"])
            flow.append(build_table(identity_rows, col_widths=[180, 280]))

            if secondary_choice:
                flow.append(Spacer(1, 12))
                flow.append(Paragraph("Choix secondaire", styles["Heading2"]))
                flow.append(
                    build_table(
                        [
                            ["Faculté", secondary_choice.faculty.name],
                            ["Département", secondary_choice.department or "-"],
                            ["Promotion", secondary_choice.promotion],
                        ],
                        col_widths=[150, 300],
                    )
                )

            if documents.exists():
                flow.append(Spacer(1, 12))
                flow.append(Paragraph("Pièces justificatives", styles["Heading2"]))
                doc_data = [["Document", "Obligatoire", "Reçu"]]
                for doc in documents:
                    doc_data.append(
                        [
                            doc.document_name,
                            "Oui" if doc.is_required else "Optionnel",
                            "Oui" if doc.file_path else "En attente",
                        ]
                    )
                flow.append(build_table(doc_data, header=True))

            flow.append(Spacer(1, 18))
            flow.append(
                Paragraph(
                    "Signature du chef de promotion / secrétaire académique : ___________________",
                    styles["BodyText"],
                )
            )
            return flow

        filename = f"fiche-inscription-{enrollment.pk}.pdf"
        return build_pdf_response(filename, build)


class EnrollmentBulletinPDFView(EnrollmentPDFBaseView):
    """
    Bulletin LMD consolidé pour un étudiant / inscription.
    """

    def get(self, request, pk):
        enrollment = get_object_or_404(
            Enrollment.objects.select_related("student", "year", "semester", "faculty", "department"),
            pk=pk,
        )
        grades = (
            Grade.objects.filter(enrollment=enrollment)
            .select_related("course_offering__course", "assessment_type")
            .order_by("course_offering__course__course_name")
        )
        styles = get_pdf_styles()

        def build():
            student = enrollment.student
            flow = [
                Paragraph("BULLETIN LMD", styles["Title"]),
                Paragraph(f"{student} - {enrollment.year.name} / {enrollment.semester.name}", styles["Heading2"]),
                Spacer(1, 8),
            ]
            data = [["Cours", "Code", "Crédits", "Évaluation", "Note", "Résultat"]]
            for grade in grades:
                course = grade.course_offering.course
                data.append(
                    [
                        course.course_name,
                        course.course_code,
                        course.credits,
                        grade.assessment_type.name,
                        f"{grade.score:.2f}",
                        "Validé" if grade.score >= 50 else "Ajourné",
                    ]
                )

            if len(data) == 1:
                data.append(["Aucune note encodée", "-", "-", "-", "-", "-"])

            flow.append(build_table(data, header=True))

            avg = grades.aggregate(avg=Avg("score"))["avg"]
            flow.append(Spacer(1, 12))
            flow.append(
                build_table(
                    [
                        ["Moyenne générale", f"{avg:.2f}" if avg is not None else "N/A"],
                        ["Mention LMD", lmd_mention(avg)],
                        ["Décision", lmd_decision(avg)],
                    ],
                    col_widths=[200, 200],
                )
            )
            flow.append(Spacer(1, 18))
            flow.append(
                Paragraph(
                    "La moyenne minimale pour la validation d'une unité d'enseignement est fixée à 50% conformément "
                    "aux directives nationales en vigueur au sein du système LMD.",
                    styles["BodyText"],
                )
            )
            return flow

        filename = f"bulletin-{enrollment.pk}.pdf"
        return build_pdf_response(filename, build)
