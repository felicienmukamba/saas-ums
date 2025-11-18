from django.db.models import Avg
from django.http import Http404
from django.shortcuts import get_object_or_404
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

from .forms import GradeForm
from .models import Grade
from core.models import AcademicYear, Department
from enrollment.models import Enrollment


class AcademicAccessMixin:
    allowed_roles = RoleGroups.ACADEMIC


class GradeListView(AcademicAccessMixin, BaseListView):
    model = Grade
    list_display = ("enrollment", "course_offering", "assessment_type", "score", "grading_date")
    page_title = "Notes"
    create_url_name = "grades:grade_create"
    detail_url_name = "grades:grade_detail"
    update_url_name = "grades:grade_update"
    delete_url_name = "grades:grade_delete"


class GradeCreateView(AcademicAccessMixin, BaseCreateView):
    model = Grade
    form_class = GradeForm
    success_url_name = "grades:grade_list"
    success_message = "Note enregistrée."


class GradeDetailView(AcademicAccessMixin, BaseDetailView):
    model = Grade


class GradeUpdateView(AcademicAccessMixin, BaseUpdateView):
    model = Grade
    form_class = GradeForm
    success_url_name = "grades:grade_list"
    success_message = "Note mise à jour."


class GradeDeleteView(AcademicAccessMixin, BaseDeleteView):
    model = Grade
    success_url_name = "grades:grade_list"


class ProclamationListPDFView(RolePermissionMixin, View):
    allowed_roles = RoleGroups.ACADEMIC

    def get(self, request):
        year_id = request.GET.get("year")
        promotion = request.GET.get("promotion")
        department_id = request.GET.get("department")

        if not year_id or not promotion:
            raise Http404("Les paramètres year et promotion sont requis.")

        try:
            year_id = int(year_id)
        except ValueError:
            raise Http404("Identifiant d'année invalide.")

        year = get_object_or_404(AcademicYear, pk=year_id)
        department = None
        if department_id:
            department = get_object_or_404(Department, pk=department_id)

        enrollments = Enrollment.objects.filter(year=year, promotion=promotion)
        if department:
            enrollments = enrollments.filter(department=department)
        enrollments = enrollments.select_related("student", "department").order_by(
            "department__name",
            "student__last_name",
        )

        if not enrollments.exists():
            raise Http404("Aucune inscription pour les critères fournis.")

        styles = get_pdf_styles()

        def build():
            flow = [
                Paragraph("LISTE DE PROCLAMATION", styles["Title"]),
                Paragraph(
                    f"Promotion: {promotion} | Année: {year.name}"
                    + (f" | Département: {department.name}" if department else ""),
                    styles["Heading2"],
                ),
                Spacer(1, 12),
            ]
            data = [["Étudiant", "Département", "Moyenne", "Mention", "Décision"]]

            for enrollment in enrollments:
                avg = (
                    Grade.objects.filter(enrollment=enrollment).aggregate(avg=Avg("score"))["avg"]
                )
                data.append(
                    [
                        str(enrollment.student),
                        enrollment.department.name if enrollment.department else "-",
                        f"{avg:.2f}" if avg is not None else "N/A",
                        lmd_mention(avg),
                        lmd_decision(avg),
                    ]
                )

            flow.append(build_table(data, header=True))
            flow.append(Spacer(1, 18))
            flow.append(
                Paragraph(
                    "La présente liste fait office de procès-verbal de proclamation conformément aux exigences LMD.",
                    styles["BodyText"],
                )
            )
            return flow

        filename = f"proclamation-{promotion}-{year.code if hasattr(year, 'code') else year.pk}.pdf"
        return build_pdf_response(filename, build)
