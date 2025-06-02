from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import datetime
import os

def exportar_resultado_pdf(resultados, nombre_archivo="memoria_calculo.pdf", usuario="", proyecto="Cálculo Eléctrico"):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    # === Logo ===
    logo_path = "logo.jpg"
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(logo, 40, height - 100, width=60, height=60, preserveAspectRatio=True, mask='auto')

    # === Título ===
    c.setFont("Helvetica-Bold", 12)
    c.drawString(120, height - 60, "CALCULOS ELÉCTRICOS NOM-001-SEDE-2012")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 90, proyecto.upper())

    # === Datos generales en dos columnas ===
    c.setFont("Helvetica", 10)
    y_start = height - 140
    x_left = 60
    x_right = width / 2 + 20
    spacing = 18

    datos_izquierda = [
        f"Tipo de carga: {resultados.get('tipo_carga', '')}",
        f"Voltaje: {resultados.get('voltaje', '')} V",
        f"I Calculado: {resultados.get('corriente', '')}",
        f"I Corregido: {resultados.get('corriente_corregida', '')}",
        f"Longitud: {resultados.get('longitud', '')} m"
    ]

    datos_derecha = [
        f"Caída de tensión: {resultados.get('caida_tension', 'Por calcular')}%",
        f"Material: {resultados.get('material', '')}",
        f"Tipo de instrumento: {resultados.get('tipo_instrumento', '---')}",
        f"Tipo de circuito: {resultados.get('tipo_circuito', '---')}"
    ]

    for i, dato in enumerate(datos_izquierda):
        c.drawString(x_left, y_start - (i * spacing), dato)

    for i, dato in enumerate(datos_derecha):
        c.drawString(x_right, y_start - (i * spacing), dato)

    # === Línea naranja ===
    c.setStrokeColor(colors.orange)
    c.setLineWidth(2)
    c.line(50, y_start - 5 * spacing - 10, width - 50, y_start - 5 * spacing - 10)

    # === Fórmulas y desarrollo ===
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.orange)
    c.drawCentredString(width / 2, y_start - 5 * spacing - 30, "FÓRMULAS Y SU DESARROLLO")
    c.setFillColor(colors.black)

    c.setLineWidth(2)
    c.line(50, y_start - 5 * spacing - 45, width - 50, y_start - 5 * spacing - 45)

    # === Pie de página ===
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 40, "Este cálculo fue generado conforme a la NOM-001-SEDE-2012.")
    c.drawString(50, 28, f"Usuario: {usuario} | Fecha: {datetime.date.today().strftime('%d/%m/%Y')}")

    c.save()
