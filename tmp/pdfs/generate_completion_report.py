from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_DIR / "Capstone_Project_Completion_Report.pdf"


def bullet(text, style):
    return Paragraph(f"<bullet>-</bullet>{text}", style)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D9E2EC"))
    canvas.line(2 * cm, 1.65 * cm, A4[0] - 2 * cm, 1.65 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606D"))
    canvas.drawString(2 * cm, 1.1 * cm, "The Daily Brief - Capstone Project Completion Report")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Page {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=colors.HexColor("#102A43"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#52606D"),
        alignment=TA_CENTER,
        spaceAfter=20,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0B7285"),
        spaceBefore=14,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyReport",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#243B53"),
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletReport",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        leftIndent=14,
        firstLineIndent=-9,
        textColor=colors.HexColor("#243B53"),
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#52606D"),
    )
)
styles.add(
    ParagraphStyle(
        name="TableCell",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.6,
        leading=11,
        textColor=colors.HexColor("#102A43"),
    )
)
styles.add(
    ParagraphStyle(
        name="TableHeader",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8.8,
        leading=11,
        textColor=colors.white,
    )
)


story = []
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("The Daily Brief", styles["ReportTitle"]))
story.append(Paragraph("Django News Application - Capstone Project Completion Report", styles["Subtitle"]))

summary_data = [
    ["Project", "Django News Application"],
    ["Database", "MariaDB migration completed"],
    ["API", "Token-authenticated REST API with role-based access"],
    ["Verification", "28 automated tests passed"],
]
summary_table = Table(summary_data, colWidths=[4.2 * cm, 11.8 * cm])
summary_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E6FFFA")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0B7285")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#243B53")),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("LEADING", (0, 0), (-1, -1), 14),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C6F6D5")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)
story.append(summary_table)

story.append(Paragraph("Project overview", styles["Section"]))
story.append(
    Paragraph(
        "The Daily Brief is a Django news application for readers, independent "
        "journalists, and editors. Readers can view approved articles, subscribe "
        "to publishers and journalists, and access subscription-based content. "
        "Journalists submit articles and create newsletters. Editors review and "
        "approve submissions.",
        styles["BodyReport"],
    )
)

story.append(Paragraph("Core implementation completed", styles["Section"]))
for item in [
    "Created a custom user model with Reader, Journalist, and Editor roles.",
    "Added Publishers, Articles, Newsletters, subscription relationships, and approval logs.",
    "Added Django groups that stay aligned with each user's role, including the required permissions for articles and newsletters.",
    "Implemented article approval, subscriber email notifications, and internal approval logging.",
    "Connected browser pages for public articles, newsletters, journalist submission, login, and editor review.",
]:
    story.append(bullet(item, styles["BulletReport"]))

story.append(PageBreak())
story.append(Paragraph("API and access control", styles["Section"]))
story.append(
    Paragraph(
        "The application includes a token-authenticated REST API. The following "
        "endpoints support the required workflow:",
        styles["BodyReport"],
    )
)

api_text_rows = [
    ["Endpoint", "Purpose"],
    ["POST /api/token/", "Obtain a token using a username and password."],
    ["GET, POST /api/articles/", "List approved articles; journalists submit articles."],
    ["GET /api/articles/subscribed/", "Reader-only access to subscribed content."],
    ["GET, PUT, PATCH, DELETE /api/articles/&lt;id&gt;/", "Retrieve or manage an article according to role."],
    ["POST /api/articles/&lt;id&gt;/approve/", "Editor approval of an article."],
    ["GET, POST /api/newsletters/", "List or create newsletters."],
    ["GET, PUT, PATCH, DELETE /api/newsletters/&lt;id&gt;/", "Retrieve or manage a newsletter."],
]
api_rows = [
    [Paragraph(cell, styles["TableHeader"]) for cell in api_text_rows[0]]
] + [
    [Paragraph(cell, styles["TableCell"]) for cell in row]
    for row in api_text_rows[1:]
]
api_table = Table(api_rows, colWidths=[7.1 * cm, 8.9 * cm], repeatRows=1)
api_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102A43")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.8),
            ("LEADING", (0, 0), (-1, -1), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F0F4F8")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F7FAFC")]),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BCCCDC")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.append(api_table)

story.append(Paragraph("Security and data work", styles["Section"]))
for item in [
    "Secured the internal approval callback with an environment-based token in the X-Callback-Token header.",
    "Used constant-time token comparison for callback validation and rejected missing or incorrect tokens.",
    "Stored MariaDB credentials and callback values in a local .env file excluded from Git.",
    "Exported the original SQLite data, migrated the MariaDB schema, loaded the fixture, and confirmed the Django system check passed.",
    "Added a .gitignore, .env.example, requirements.txt, and README for a cleaner GitHub submission.",
]:
    story.append(bullet(item, styles["BulletReport"]))

story.append(PageBreak())
story.append(Paragraph("Testing and manual demonstration", styles["Section"]))
story.append(
    Paragraph(
        "Automated tests were written with Django REST Framework's testing tools. "
        "The final test run completed successfully with 28 tests passing and no "
        "Django system check issues.",
        styles["BodyReport"],
    )
)

test_rows = [
    ["Area checked", "Examples covered"],
    ["Authentication", "Valid token login, rejected incorrect password, protected profile."],
    ["Role permissions", "Reader denied article creation; journalist submission; editor management and approval."],
    ["Subscriptions", "Reader receives only approved articles from subscribed publishers and journalists."],
    ["Newsletters", "Only approved articles accepted; author editing and deletion rules checked."],
    ["Callback workflow", "Missing and invalid tokens rejected; valid secured callback creates an approval log."],
    ["Website workflow", "Public page filtering, journalist web submission, and editor web approval."],
]
test_table = Table(test_rows, colWidths=[4.4 * cm, 11.6 * cm], repeatRows=1)
test_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B7285")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.8),
            ("LEADING", (0, 0), (-1, -1), 12),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#99C2C8")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#E6FFFA")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.append(test_table)

story.append(Paragraph("Postman evidence", styles["Section"]))
story.append(
    Paragraph(
        "An importable Postman collection and safe environment template are included "
        "in the postman folder. They demonstrate public endpoints, role-specific "
        "token login, reader restrictions, journalist submission, editor approval, "
        "and newsletter creation. The collection contains response tests for each "
        "expected outcome.",
        styles["BodyReport"],
    )
)

story.append(Paragraph("Submission checklist", styles["Section"]))
for item in [
    "Submit the contents of the Capstone -News_app folder from Documents/Codex.",
    "Include the Python source code, templates, migrations, README, Postman folder, and this report.",
    "Do not submit the myenv folder, local .env file, SQLite database, backup fixture, passwords, or generated tokens.",
    "Use Postman screenshots only after hiding passwords and tokens.",
]:
    story.append(bullet(item, styles["BulletReport"]))

story.append(Spacer(1, 0.4 * cm))
story.append(
    Paragraph(
        "Prepared as supporting documentation for the Django News Application capstone submission.",
        styles["Small"],
    )
)

document = SimpleDocTemplate(
    str(OUTPUT_FILE),
    pagesize=A4,
    leftMargin=2 * cm,
    rightMargin=2 * cm,
    topMargin=1.7 * cm,
    bottomMargin=2.2 * cm,
    title="The Daily Brief - Capstone Project Completion Report",
    author="Brett",
)
document.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT_FILE)
