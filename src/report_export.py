# @Author : Yulia
# @File   : report_export.py
# @Time   : 2025/9/6

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def export_full_report(metrics, results_df, figs, model_acc, selected_charts):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # --- Title ---
    story.append(Paragraph("🎮 Player Behavior Analysis Report", styles["Title"]))
    story.append(Spacer(1, 12))

    # --- Overview ---
    if metrics:
        story.append(Paragraph("🧭 Overview", styles["Heading2"]))
        for k, v in metrics.items():
            story.append(Paragraph(f"<b>{k}:</b> {v}", styles["Normal"]))
        story.append(Spacer(1, 12))

    # --- Correlation Results ---
    if results_df is not None:
        story.append(Paragraph("🔗 Correlation Results", styles["Heading2"]))
        story.append(Paragraph(results_df.to_html(index=False), styles["Normal"]))
        story.append(Spacer(1, 12))

    # --- Prediction Accuracy ---
    if model_acc is not None:
        story.append(Paragraph("🤖 Prediction Model", styles["Heading2"]))
        story.append(Paragraph(f"Accuracy: {model_acc*100:.2f}%", styles["Normal"]))
        story.append(Spacer(1, 12))

    # --- Figures ---
    for title, fig in figs.items():
        if title not in selected_charts:
            continue
        img_buf = BytesIO()
        fig.write_image(img_buf, format="png")
        img_buf.seek(0)
        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Image(img_buf, width=12*cm, height=7*cm))
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer
