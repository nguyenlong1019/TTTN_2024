fileName = 'MyDoc.pdf'
title = 'Chào mừng bạn đến với thế giới Python'

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Đăng ký font chữ hỗ trợ tiếng Việt
pdfmetrics.registerFont(TTFont("timesvn", "times.ttf"))

pdf = canvas.Canvas(fileName)
# ###################################

# Sử dụng font chữ tiếng Việt
pdf.setFont('timesvn', 36)
pdf.drawCentredString(300, 770, title)
pdf.save()
