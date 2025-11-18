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
from ums.pdf import Paragraph, Spacer, build_pdf_response, build_table, get_pdf_styles

from .forms import PaymentForm
from .models import Payment


class FinanceAccessMixin:
    allowed_roles = RoleGroups.FINANCE


class PaymentListView(FinanceAccessMixin, BaseListView):
    model = Payment
    list_display = ("enrollment", "academic_fee", "amount_paid", "payment_method", "payment_date")
    page_title = "Paiements"
    create_url_name = "payments:payment_create"
    detail_url_name = "payments:payment_detail"
    update_url_name = "payments:payment_update"
    delete_url_name = "payments:payment_delete"


class PaymentCreateView(FinanceAccessMixin, BaseCreateView):
    model = Payment
    form_class = PaymentForm
    success_url_name = "payments:payment_list"
    success_message = "Paiement enregistré."


class PaymentDetailView(FinanceAccessMixin, BaseDetailView):
    model = Payment

    def get_extra_actions(self):
        obj = getattr(self, "object", None) or self.get_object()
        return [
            {
                "label": "Reçu officiel (PDF)",
                "url": reverse("payments:payment_receipt_pdf", args=[obj.pk]),
            }
        ]


class PaymentUpdateView(FinanceAccessMixin, BaseUpdateView):
    model = Payment
    form_class = PaymentForm
    success_url_name = "payments:payment_list"
    success_message = "Paiement mis à jour."


class PaymentDeleteView(FinanceAccessMixin, BaseDeleteView):
    model = Payment
    success_url_name = "payments:payment_list"


class PaymentReceiptPDFView(RolePermissionMixin, View):
    allowed_roles = RoleGroups.FINANCE

    def get(self, request, pk):
        payment = get_object_or_404(
            Payment.objects.select_related(
                "enrollment__student",
                "academic_fee__category",
                "academic_fee__year",
            ),
            pk=pk,
        )
        styles = get_pdf_styles()

        def build():
            flow = [
                Paragraph("REÇU OFFICIEL - SERVICE FINANCIER", styles["Title"]),
                Spacer(1, 6),
                Paragraph(f"N° {payment.receipt_number}", styles["Heading2"]),
                Spacer(1, 12),
            ]
            student = payment.enrollment.student
            flow.append(
                build_table(
                    [
                        ["Étudiant", str(student)],
                        ["Matricule", student.matricule or "-"],
                        ["Filière", payment.enrollment.faculty.name],
                        ["Année académique", payment.academic_fee.year.name],
                    ],
                    col_widths=[170, 260],
                )
            )
            flow.append(Spacer(1, 12))
            flow.append(
                build_table(
                    [
                        ["Catégorie de frais", payment.academic_fee.category.name],
                        ["Montant réglé", f"{payment.amount_paid} USD"],
                        ["Méthode", payment.payment_method],
                        ["Date", payment.payment_date.strftime("%d/%m/%Y %H:%M")],
                    ],
                    col_widths=[170, 260],
                )
            )
            flow.append(Spacer(1, 18))
            flow.append(
                Paragraph(
                    "Reçu délivré par le service financier conformément aux directives LMD. "
                    "Signature du caissier : ______________________",
                    styles["BodyText"],
                )
            )
            return flow

        filename = f"recu-{payment.receipt_number}.pdf"
        return build_pdf_response(filename, build)
