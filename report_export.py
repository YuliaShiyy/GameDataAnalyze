# @Author : Yulia
# @File   : report_export.py
# @Time   : 2025/9/4

import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def _add_table(story, title, df):
    """把 DataFrame 转成报告里的 Table"""
    styles = getSampleStyleSheet()
    story.append(Paragraph(title, styles["Heading2"]))
    if df is None or df.empty:
        story.append(Paragraph("No data available", styles["Normal"]))
    else:
        table_data = [df.columns.tolist()] + df.astype(str).values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ]))
        story.append(table)
    story.append(Spacer(1, 15))


def export_full_report(metrics, results_df, figs, model_acc):
    """
    导出完整版报告（指标 + 相关性表格 + 所有图表）
    metrics: dict 概览指标
    results_df: DataFrame 相关性分析结果
    figs: dict 所有图表对象
    model_acc: float 模型准确率
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("🎮 Player Behavior Analysis Report", styles["Title"]))
    story.append(Spacer(1, 20))

    # 概览指标
    story.append(Paragraph("📊 Overview Metrics", styles["Heading2"]))
    for k, v in metrics.items():
        story.append(Paragraph(f"{k}: {v}", styles["Normal"]))
    story.append(Spacer(1, 15))

    # 相关性表格
    if results_df is not None:
        _add_table(story, "🔗 Correlation Analysis Results", results_df)

    # 所有图表
    for title, fig in figs.items():
        if fig is None:
            continue
        try:
            img_buf = io.BytesIO()
            fig.write_image(img_buf, format="png")
            img_buf.seek(0)
            story.append(Paragraph(f"📈 {title}", styles["Heading2"]))
            story.append(Image(img_buf, width=400, height=250))
            story.append(Spacer(1, 15))
        except Exception:
            continue

    # 模型准确率
    if model_acc is not None:
        story.append(Paragraph("🤖 Prediction Model Accuracy", styles["Heading2"]))
        story.append(Paragraph(f"Accuracy: {model_acc:.2%}", styles["Normal"]))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
