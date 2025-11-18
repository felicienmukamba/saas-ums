from __future__ import annotations

from io import BytesIO
from typing import Callable, Iterable

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf_response(filename: str, build_flowables: Callable[[], list]) -> HttpResponse:
    """
    Construit une réponse PDF standardisée (A4) à partir d'une fonction qui retourne
    la liste des flowables ReportLab.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2 * cm,
    )
    elements = build_flowables()
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.write(pdf)
    return response


def get_pdf_styles():
    """
    Retourne un jeu de styles harmonisés avec la charte Bootstrap utilisée par l'app.
    """

    styles = getSampleStyleSheet()
    styles["Title"].fontSize = 18
    styles["Title"].leading = 22
    styles["Heading1"].fontSize = 14
    styles["Heading1"].spaceAfter = 12
    styles["Heading2"].fontSize = 12
    styles["Heading2"].spaceBefore = 12
    styles["Heading2"].spaceAfter = 6
    styles.add(
        ParagraphStyle(
            name="Small",
            fontSize=9,
            leading=12,
            spaceAfter=4,
        )
    )
    return styles


def build_table(
    data: Iterable[Iterable],
    *,
    col_widths: Iterable | None = None,
    header: bool = False,
    align: str = "LEFT",
) -> Table:
    """
    Construit rapidement un tableau bordé compatible PDF.
    """

    table = Table(data, colWidths=col_widths)
    style_commands = [
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), align),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        style_commands += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    table.setStyle(TableStyle(style_commands))
    return table


def lmd_mention(score: float | None) -> str:
    if score is None:
        return "Non évalué"
    if score >= 80:
        return "Grande Distinction"
    if score >= 70:
        return "Distinction"
    if score >= 60:
        return "Satisfaction"
    if score >= 50:
        return "Passable"
    return "Ajourné"


def lmd_decision(score: float | None) -> str:
    if score is None:
        return "En attente"
    return "Admis" if score >= 50 else "Ajourné"


__all__ = [
    "build_pdf_response",
    "build_table",
    "get_pdf_styles",
    "lmd_mention",
    "lmd_decision",
    "Spacer",
    "Paragraph",
]

