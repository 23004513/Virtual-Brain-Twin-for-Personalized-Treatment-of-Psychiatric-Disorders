from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
import datetime
optimal_coupling_a = 0.0145
best_corr = 0.0295
report_filename = "Virtual_Brain_Twin_Report.pdf"
doc = SimpleDocTemplate(report_filename, pagesize=A4)
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'title',
    parent=styles['Title'],
    fontSize=20,
    textColor=colors.darkblue,
    alignment=1
)
normal_style = styles['Normal']

content = []
content.append(Paragraph(" Virtual Brain Twin – Personalized Treatment Report", title_style))
content.append(Spacer(1, 20))
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
content.append(Paragraph(f"<b>Generated On:</b> {now}", normal_style))
content.append(Spacer(1, 10))
table_data = [
    ["Parameter", "Value"],
    ["Optimal Coupling (a)", f"{optimal_coupling_a:.4f}"],
    ["Best Correlation", f"{best_corr:.4f}"]
]
table = Table(table_data, colWidths=[200, 200])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('BOX', (0, 0), (-1, -1), 1, colors.black),
]))
content.append(table)
content.append(Spacer(1, 20))
interpretation = """
This report summarizes the Virtual Brain Twin simulation.  
The optimal coupling parameter (a) represents the balance between
different brain regions’ activity levels, while the correlation indicates
how closely the simulated brain dynamics match the target functional
connectivity.  
Higher correlations imply better personalization.  
These parameters can now guide further tuning or clinical simulation.
"""
content.append(Paragraph(interpretation, normal_style))
content.append(Spacer(1, 10))
try:
    img = Image("brain_activity_plot.png", width=400, height=250)
    content.append(Spacer(1, 10))
    content.append(Paragraph("<b>Simulated Brain Activity Graph:</b>", normal_style))
    content.append(Spacer(1, 10))
    content.append(img)
    content.append(Spacer(1, 20))
except Exception as e:
    content.append(Paragraph("Graph image not found. Please run main.py first to generate it.", normal_style))
doc.build(content)

print(f" Report generated successfully: {report_filename}")
