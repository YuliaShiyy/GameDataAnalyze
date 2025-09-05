# @Author : Yulia
# @File   : report_export.py
# @Time   : 2025/9/3

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors

import matplotlib.pyplot as plt


def export_full_report(metrics, results_df, figs_all, model_acc, cluster_summary, trend):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # =====================
    # 封面
    # =====================
    story.append(Paragraph("<b>🎮 Player Behavior Analysis Report</b>", styles["Title"]))
    story.append(Spacer(1, 1 * cm))

    # =====================
    # 概览指标
    # =====================
    story.append(Paragraph("<b>Overview Metrics</b>", styles["Heading2"]))
    data_metrics = [[k, str(v)] for k, v in metrics.items()]
    table = Table(data_metrics, colWidths=[7 * cm, 7 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5 * cm))

    # =====================
    # 相关性分析结果
    # =====================
    if results_df is not None and not results_df.empty:
        story.append(Paragraph("<b>Correlation Analysis</b>", styles["Heading2"]))
        data_corr = [results_df.columns.tolist()] + results_df.values.tolist()
        table_corr = Table(data_corr, colWidths=[3.5 * cm] * len(results_df.columns))
        table_corr.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ]))
        story.append(table_corr)
        story.append(Spacer(1, 0.5 * cm))

    # =====================
    # 聚类结果
    # =====================
    if cluster_summary is not None:
        story.append(Paragraph("<b>Cluster Summary</b>", styles["Heading2"]))
        data_cluster = [cluster_summary.columns.tolist()] + cluster_summary.reset_index().values.tolist()
        table_cluster = Table(data_cluster, colWidths=[3.5 * cm] * len(cluster_summary.columns))
        table_cluster.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ]))
        story.append(table_cluster)
        story.append(Spacer(1, 0.5 * cm))

    # =====================
    # 预测模型准确率
    # =====================
    if model_acc is not None:
        story.append(Paragraph("<b>Prediction Model</b>", styles["Heading2"]))
        story.append(Paragraph(f"Model Accuracy: {model_acc*100:.2f}%", styles["Normal"]))
        story.append(Spacer(1, 0.5 * cm))

    # =====================
    # 趋势分析表
    # =====================
    if trend is not None:
        story.append(Paragraph("<b>Trend Data</b>", styles["Heading2"]))
        data_trend = [trend.columns.tolist()] + trend.values.tolist()
        table_trend = Table(data_trend, colWidths=[3 * cm] * len(trend.columns))
        table_trend.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ]))
        story.append(table_trend)
        story.append(Spacer(1, 0.5 * cm))

    # =====================
    # 插入图表
    # =====================
    for title, fig in figs_all.items():
        if fig is None:
            continue
        story.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
        img_buf = io.BytesIO()
        fig.write_image(img_buf, format="png")  # plotly 支持直接导出图片
        img_buf.seek(0)
        story.append(Image(img_buf, width=15 * cm, height=9 * cm))
        story.append(Spacer(1, 0.5 * cm))

    # =====================
    # 导出 PDF
    # =====================
    doc.build(story)
    buffer.seek(0)
    return buffer
