from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from django.http import JsonResponse 
import json 
import os 
from dotenv import load_dotenv # pip install python-dotenv
from django.views.decorators.csrf import csrf_exempt
import json, random
from datetime import datetime, date 
from .models import * 
from django.contrib.auth.models import User 
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse 
from openpyxl import Workbook 
import tempfile

# Reportlab for PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, portrait, landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import letter 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics


from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas 
from reportlab.lib.units import cm 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
from reportlab.lib.pagesizes import letter, landscape 
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors


# Report view
from django.db.models import Sum 
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware


# Handle 404, 500, 400, 403
def handler404(request, *args, **argv):
    return render(request, '404.html', {}, status=404)  


def handler500(request, *args, **argv):
    return render(request, '500.html', {}, status=500)


def handler400(request, *args, **argv):
    return render(request, '400.html', {}, status=400)


def handler403(request, *args, **argv):
    return render(request, '403.html', {}, status=403)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'core/login.html', {'message': 'Password không đúng!!'}, status=401)
        except Exception as e:
            return render(request, 'core/login.html', {'message': f'User với {username} không tồn tại!'}, status=500)
    return render(request, 'core/login.html', status=200)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def index(request):
    '''Quản lý hải trình'''
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

    ships = BangTau.objects.all()

    return render(request, 'core/index.html', {
        'api_key': API_KEY,
        'ships': ships,
    }, status=200)


@login_required(login_url='/login/')
def marine_diary_view(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')

    # hiểu, vì filter nó sẽ không gây ra DoesNotExist
    try:
        ships = BangTau.objects.filter(Q(SoDangKy__icontains=query))
        if ships.exists():
            ship = BangTau.objects.filter(Q(SoDangKy__icontains=query)).first()
        else:
            messages.info(request, f"Không tìm thấy tàu với query = '{query}'") 
            return redirect('index')        
    except ValueError:
        messages.info(request, f"Số đăng ký tàu không được phép trống hoặc None!!")
        return redirect('index')

    return render(request, 'core/index-search.html', {
        'ship': ship,
        'start_date': start_date,
        'end_date': end_date
    }, status=200)


@login_required(login_url='/login/')
def get_ship_location_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pk = data.get('pk')
            start_date = data.get('startDate');
            end_date = data.get('endDate')

            try:
                ship = BangTau.objects.get(pk=pk)
            except BangTau.DoesNotExist:
                messages.info(request, f"Không tìm thấy thông tin tàu với query = '{pk}'")
                return redirect('index')

            location = BangViTriTau.objects.filter(
                Q(Ngay__gte=start_date) & Q(Ngay__lte=end_date),
                IDTau = ship
            ).order_by('Ngay').values('ViDo', 'KinhDo', 'Ngay')
            # print(location)
            for loc in location:
                loc['Ngay'] = loc['Ngay'].strftime('%Y-%m-%d %H:%M:%S')
            # print(location)

            location_data = list(location)

            info = {
                'SoDangKy': ship.SoDangKy,
                'ChuTau': ship.IDChuTau.HoTen,
                'ThuyenTruong': ship.IDThuyenTruong.HoTen,
                'ViDo': location_data[-1]['ViDo'],
                'KinhDo': location_data[-1]['KinhDo'],
                'Ngay': location_data[-1]['Ngay']
            }


            return JsonResponse({
                'message': f'Nhật ký hải trình tàu {ship.SoDangKy}',
                'status': 200,
                'location': location_data,
                'info': info,
            }, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({
                'message': 'Dữ liệu không hợp lệ',
                'status': 400
            }, status=400)
    else:
        return JsonResponse({
            'message': 'Method not allowed',
            'status': 405
        }, status=405)
    

@login_required(login_url='/login/')
def get_all_location_api(request):
    ships = BangTau.objects.all()
    info = []
    for i in ships:
        new_loc = i.bangvitritau_set.order_by('-Ngay').first()
        ship_info = {
            'SoDangKy': i.SoDangKy,
            'ChuTau': i.IDChuTau.HoTen,
            'ThuyenTruong': i.IDThuyenTruong.HoTen,
            'ViDo': new_loc.ViDo,
            'KinhDo': new_loc.KinhDo,
            'NgayCapNhat': new_loc.Ngay,
        }
        info.append(ship_info)
    return JsonResponse({
        'status': 200,
        'message': 'Cập nhật thông tin vị trí các tàu thành công!',
        'info': info,
    }, status=200)


@login_required(login_url='/login/')
def report_view(request):
    fishing_port = BangCangCa.objects.all()
    titles = ["STT", "Tên Loài Cá", "Sản Lượng"]

    # Lấy thời điểm 24h trước 
    time_threshold = timezone.now() - timedelta(hours=24)

    # Lấy danh sách các mẻ lưới có thời gian thu ngư cụ trong khoảng 24h
    bang_me_luoi_24h = BangMeLuoi.objects.filter(ThoiDiemThuNguCu__lte=time_threshold)
    # print(bang_me_luoi_24h)
    # Tính tổng sản lượng của mỗi loại cá được đánh bắt trong 24h
    items = (
        BangLoaiCaDuocDanhBatTrongMeLuoi.objects
        .filter(IDMeLuoi__in=bang_me_luoi_24h)
        .values('IDLoaiCa__Ten')
        .annotate(tong_san_luong=Sum('SanLuong'))
        .order_by('-tong_san_luong').all()
    )

    return render(request, 'core/report.html', {
        'fishing_port': fishing_port,
        'titles': titles,
        'items': items,
    }, status=200)


@login_required(login_url='/login/')
def top_10_fishing_api(request):
    # Lấy thời điểm 24h trước 
    time_threshold = timezone.now() - timedelta(hours=24)

    # Lấy danh sách các mẻ lưới có thời gian thu ngư cụ trong khoảng 24h
    bang_me_luoi_24h = BangMeLuoi.objects.filter(ThoiDiemThuNguCu__lte=time_threshold)
    # print(bang_me_luoi_24h)
    # Tính tổng sản lượng của mỗi loại cá được đánh bắt trong 24h
    top_loai_ca = (
        BangLoaiCaDuocDanhBatTrongMeLuoi.objects
        .filter(IDMeLuoi__in=bang_me_luoi_24h)
        .values('IDLoaiCa__Ten')
        .annotate(tong_san_luong=Sum('SanLuong'))
        .order_by('-tong_san_luong')[:10]
    )
    # print(top_loai_ca)
    bundles = []
    for item in top_loai_ca:
        data = {
            'fish_name': item['IDLoaiCa__Ten'],
            'qty': item['tong_san_luong']
        }
        bundles.append(data)
    # print(bundles)
    return JsonResponse({
        'message': 'Top 10 loại cá được đánh bắt nhiều nhất trong 24h qua',
        'status': 200,
        'bundles': bundles
    }, status=200)


@login_required(login_url='/login/')
def journal_view(request):
    titles = ["STT", "Mã tàu", "Ngày tạo nhật ký", "Chủ tàu", "CMND (CCCD)", "Mã nhật ký", "Ghi chú", "Thao tác"]
    items = BangNhatKy.objects.all()
    # print(items)
    return render(request, 'core/journal.html', {
        'titles': titles,
        'items': items,
    }, status=200)


@login_required(login_url='/login/')
def journal_pdf_view(request, pk):
    response = generate_journal_pdf(request, pk)
    return HttpResponse(response.content, content_type='application/pdf')
    # return render(request, 'core/view_journal_pdf.html', {
    #     'pdf_content': response.content
    # }, status=200)


@login_required(login_url='/login/')
def generate_journal_pdf(request, pk):
    try:
        ediary = BangNhatKy.objects.get(pk=pk)
    except BangNhatKy.DoesNotExist:
        messages.info(request, f"Không tìm thấy thông tin nhật ký với ID = '{pk}'") 
        return redirect('journal-view')
    except Exception as e:
        messages.info(request, f"Lỗi khi truy xuất thông tin nhật ký!!!")
        return redirect('journal-view')

    # Tạo một đối tượng HttpResponse với content_type là 'application/pdf'
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="example.pdf"'
    response['Content-Disposition'] = 'inline; filename="example.pdf"'

    page_width, page_height = landscape(letter)
    pdf = canvas.Canvas(
        response,
        pagesize=(page_width, page_height)
    )

    # Vẽ đường
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.line(320, 515, 470, 515)  # Vẽ đường ngang trên cùng của Frame

    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    font_normal_path = 'times.ttf'
    font_bold_path = 'timesbd.ttf'

    pdfmetrics.registerFont(TTFont('Times_New_Roman', font_normal_path))
    pdfmetrics.registerFont(TTFont('Times_New_Roman_Bold', font_bold_path))

    h2 = ParagraphStyle('CustomHeading2', parent=styles['Heading2'])
    h2.fontName = 'Times_New_Roman_Bold'
    h2.alignment = 1

    h2_normal = ParagraphStyle('CustomHeading3', parent=styles['Heading2'])
    h2_normal.fontName = "Times_New_Roman"
    h2_normal.alignment = 1

    # Vẽ hình chữ nhật
    # pdf.rect(515, 515, 200, 25)

    # Tính toán vị trí trung tâm của hình chữ nhật
    rect_x = 515
    rect_y = 515
    rect_width = 200
    rect_height = 25
    text = "BĐ-12344-KT-12-23"
    text_width, text_height = pdf.stringWidth(text), 16
    text_x = rect_x + (rect_width - text_width) / 2
    text_y = rect_y + (rect_height - text_height) / 2

    # Vẽ hình chữ nhật
    pdf.rect(rect_x, rect_y, rect_width, rect_height)
    pdf.setFont("Times_New_Roman", 16)
    # Thêm văn bản vào trung tâm của hình chữ nhật
    pdf.drawString(text_x, text_y, text)

    frm1_width = page_width - (2.5 * cm) * 2
    frm1_height = (7/10) * (page_height - 2.5 *cm)

    flow_obj1 = []
    frame1 = Frame(
        x1=2.5*cm,
        y1=page_height - frm1_height - 2.5*cm,
        width=frm1_width,
        height=frm1_height,
        showBoundary=1
    )

    paragraph_normal = styles['Normal']
    paragraph_normal.fontSize = 13
    paragraph_normal.spaceAfter = 1.3 * paragraph_normal.fontSize 
    paragraph_normal.fontName = "Times_New_Roman"

    flow_obj1.append(Paragraph("TỔNG CỤC THỦY SẢN", h2))
    flow_obj1.append(Paragraph("NHẬT KÝ KHAI THÁC THỦY SẢN", h2))
    flow_obj1.append(Paragraph("NGHỀ CHÍNH: Đánh bắt cá ngừ.........(**)", h2_normal))

    flow_obj1.append(Paragraph("1. Họ và tên chủ tàu: Nguyễn Văn Long....................; 2. Họ và tên thuyền trưởng: Nguyễn Văn Long........................", paragraph_normal))
    flow_obj1.append(Paragraph("3. Số đăng ký tàu: BĐ-12314.........; 4. Chiều dài lớn nhất của tàu: 30....m; 5. Tổng công suất máy chính: 250.......KW", paragraph_normal))
    flow_obj1.append(Paragraph("6. Số Giấy phép khai thác thủy sản: GP-120.................Thời hạn đến: 27/12/2039...........................................", paragraph_normal))
    flow_obj1.append(Paragraph("7. Nghề phụ 1: Đánh bắt cá ngừ...........................; 8. Nghề phụ 2: Đánh bắt cá ngừ.....................................", paragraph_normal))
    flow_obj1.append(Paragraph("9. Kích thước chủ yếu của ngư cụ (ghi cụ thể theo nghề chính): ", paragraph_normal))
    flow_obj1.append(Paragraph("a) Nghề câu: Chiều dài toàn bộ vàng câu: 20..............m; Số lưỡi câu: 1234..............................................lưỡi", paragraph_normal))
    flow_obj1.append(Paragraph("b) Nghề lưới vây, rê: Chiều dài toàn bộ lưới: 20.........m; Chiều cao lưới: 12................................................m", paragraph_normal))
    flow_obj1.append(Paragraph("c) Nghề lưới chụp: Chu vi miệng lưới: 30.................m; Chiều cao lưới: 12................................................m", paragraph_normal))
    flow_obj1.append(Paragraph("d) Nghề lưới kéo: Chiều dài giềng phao: 30...............m; Chiều dài toàn bộ lưới: 20........................................m", paragraph_normal))
    flow_obj1.append(Paragraph("e) Nghề khác:...........................................................", paragraph_normal))

    frame1.addFromList(flow_obj1, pdf)

    frm2_width = (1/4)*(page_width - 5 * cm)
    frm2_height = (1/6)  * (page_height - 2.5 *cm)
    flow_obj2 = []
    frame2 = Frame(
        x1=2.5*cm,
        y1=page_height - (frm1_height + frm2_height) - 2.5*cm,
        width=frm2_width,
        height=frm2_height,
        showBoundary=1
    )

    paragrap_bold = styles['Title']
    paragrap_bold.fontSize = 13
    paragrap_bold.spaceAfter = 1.3 * paragrap_bold.fontSize 
    paragrap_bold.fontName = "Times_New_Roman_Bold"
    paragrap_bold.alignment = 0

    flow_obj2.append(Paragraph("Chuyến biển số: 12...........", paragrap_bold))


    frame2.addFromList(flow_obj2, pdf)

    frm3_width = (3/4)*(page_width - 5 * cm)
    frm3_height = (1/6) * (page_height - 2.5 *cm)
    flow_obj3 = []
    frame3 = Frame(
        x1=2.5*cm + frm2_width,
        y1=page_height - (frm1_height + frm3_height) - 2.5*cm,
        width=frm3_width,
        height=frm3_height,
        showBoundary=1
    )

    flow_obj3.append(Paragraph("10. Cảng đi: Cảng Quy Nhơn.......; Thời gian đi: Ngày 20... tháng 11... năm 2023...",paragraph_normal))
    flow_obj3.append(Paragraph("11. Cảng về: Cảng Tam Quan.......; Thời gian cập cảng: Ngày 20... tháng 12... năm 2023...",paragraph_normal))
    flow_obj3.append(Paragraph("12. Nộp Nhật ký: Ngày 20... tháng 12... năm 2023...; Vào Sổ số: BĐ-12344-KT-12-23",paragraph_normal))

    frame3.addFromList(flow_obj3, pdf)

    pdf.showPage()

    h2_left = ParagraphStyle('CustomHeading2', parent=styles['Heading2'])
    h2_left.fontName = 'Times_New_Roman_Bold'
    h2_left.alignment = 0


    flow_obj4 = []
    frame4 = Frame(
        x1=2.5*cm,
        y1=2.5*cm,
        width=(page_width - 5*cm),
        height=(page_height - 4*cm),
        showBoundary=0
    )
    flow_obj4.append(Paragraph("I. THÔNG TIN VỀ HOẠT ĐỘNG KHAI THÁC THỦY SẢN", h2_left))
    flow_obj4.append(Paragraph("1.Thông tin mẻ lưới/câu", paragrap_bold))

    ratio = (page_width - 4*cm) / 40
    colWidths = []
    colWidths.append(ratio*2)
    colWidths.append(ratio*4)
    colWidths.append(ratio*3)
    colWidths.append(ratio*3)
    colWidths.append(ratio*4)
    for i in range(8):
        colWidths.append(ratio*3)
    # print(colWidths)

    data = [
        ['Mẻ\nthứ', 'Thời \nđiểm bắt\nđầu thả', 'Vị trí thả', '', 'Thời\nđiểm kết\nthúc thu', 'Vị trí thu', '', 'Sản lượng các loài chủ yếu**(kg)', '', '', '', '', '', 'Tổng sản\nlượng\n(kg)'],
        ['', '', 'Vĩ độ', 'Kinh độ', '', 'Vĩ độ', 'Kinh độ', 'Loài 1', 'Loài 2', 'Loài 3', 'Loài 4', 'Loài 5', 'Loài 6', ''],
        ['', '', '', '', ''],
        [1, '20/01/2023', 13.04, 109.01, '20/02/2023', 13.05, 110.11, 100, 200, 3000, 400, 500, 900, 5100],
        [2, '21/02/2023', 13.04, 109.01, '21/03/2023', 13.05, 110.11, 100, 200, 3000, 400, 500, 900, 5100],
        [3, '21/02/2023', 13.04, 109.01, '21/03/2023', 13.05, 110.11, 100, 200, 3000, 400, 500, 900, 5100],
    ]

    table = Table(data, colWidths=colWidths)
    tstyle = TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONT", (0, 0), (-1, -1), "Times_New_Roman",13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ("SPAN", (0, 0), (0, 2)),  # Row span from row 0 to row 1 for the first column (col - row) (col - row )  (Row span thì col giữ nguyên) # mẻ thứ
        ("SPAN", (1, 0), (1, 2)),   # Row span from row 1 to row 2 for the second column  # thời điểm bắt đầu thả
        ("SPAN", (2, 0), (3, 0)),  # Column span from column 0 to column 2 for the first Row (col span thì row giữ nguyên) # vị trí thả
        ("SPAN", (2, 1), (2, 2)), # vĩ độ thả
        ("SPAN", (3, 1), (3, 2)), # kinh độ thả
        ("SPAN", (4, 0), (4, 2)), # thời điểm kết thúc thu 
        ("SPAN", (5, 0), (6, 0)), # vị trí thu
        ("SPAN", (5, 1), (5, 2)), # vĩ độ thu
        ("SPAN", (6, 1), (6, 2)), # kinh độ thu
        ("SPAN", (7, 0), (12, 0)), # sản lượng các loài
        ("SPAN", (7, 1), (7, 2)), # loài
        ("SPAN", (8, 1), (8, 2)), # loài
        ("SPAN", (9, 1), (9, 2)), # loài
        ("SPAN", (10, 1), (10, 2)), # loài
        ("SPAN", (11, 1), (11, 2)), # loài
        ("SPAN", (12, 1), (12, 2)), # loài
        ("SPAN", (13, 0), (13, 2)) # tổng sản lượng
    ])
    table.setStyle(tstyle)
    flow_obj4.append(table)
    flow_obj4.append(Spacer(1, 0.25*cm))
    flow_obj4.append(Paragraph("**Ghi các đối tượng khai thác chính theo từng nghề (Kéo, Rê, Vây, Câu, Chụp…). Đối với các nghề khai thác cá ngừ cần ghi rõ sản lượng của từng loài như: cá ngừ Vây vàng, cá ngừ Mắt to, cá ngừ Vằn (Sọc dưa), cá ngừ khác (Chù, ồ…).", paragraph_normal))
    flow_obj4.append(Paragraph("2.Thông tin về các loài nguy cấp quý hiếm", paragrap_bold))
    flow_obj4.append(Paragraph("Cá voi/Cá heo/Bò biển/Quản đồng/Vích/Đồi mồi dứa/Đồi mồi/Rùa da/Loài khác (Ghi tên cụ thể)", paragraph_normal))

    data2 = [
        ["Mẻ","Loài","Thời điểm\nbắt gặp", "Khối\nlượng/con\n(kg)", "Số lượng\nước tính", "Kích thước\nước tính\n(cm)", "Bắt gặp trong quá trình khai thác\n(chọn 1)", "", "", "Tình trạng bắt gặp (chọn 1)"],
        ["", "", "", "", "", "", "Lưới/câu", "Kéo lưới", "Khác", "Sống", "Chết", "Bị thương"],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
    ]
    colWidths2 = [1*cm, 2.2*cm, 3*cm]
    for i in range(9):
        colWidths2.append(2.2*cm)
    table2 = Table(data2, colWidths=colWidths2)
    tstyle2 = TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONT", (0, 0), (-1, -1), "Times_New_Roman",13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ("SPAN", (0, 0), (0, 1)), # mẻ
        ("SPAN", (1, 0), (1, 1)), # loài
        ("SPAN", (2, 0), (2, 1)), # thời điểm bắt gặp
        ("SPAN", (3, 0), (3, 1)), # khối lượng/con (kg)
        ("SPAN", (4, 0), (4, 1)), # số lượng
        ("SPAN", (5, 0), (5, 1)), # kích thước
        ("SPAN", (6, 0), (8, 0)), # bắt gặp trong quá trình khai thác
        ("SPAN", (9, 0), (11, 0)), # tình trạng bắt gặp
    ])
    table2.setStyle(tstyle2)
    flow_obj4.append(table2)
    flow_obj4.append(Spacer(1, 0.25*cm))
    flow_obj4.append(Paragraph("Thông tin bổ sung về loài (nếu có): (Về màu sắc loài; thiết bị, thẻ gắn số trên cá thể;…và các thông tin khác nếu có)\n\
        ……………………………………………………………………………………………………………………………………………………\
    …………………………..………………………………………………………………………………………………………………………\
    ……………………………………………………………………………………….", style_normal))
    frame4.addFromList(flow_obj4, pdf)
    pdf.showPage()

    flow_obj5 = []
    frame5 = Frame(
        x1=2.5*cm,
        y1=2.5*cm + 0.4*(page_height - 5*cm),
        width=(page_width - 5*cm),
        height=0.6*(page_height - 3*cm),
        showBoundary=0
    )

    flow_obj5.append(Paragraph("II. THÔNG TIN VỀ HOẠT ĐỘNG CHUYỂN TẢI (nếu có)", h2_left))
    data3 = [
        ["TT", "Ngày, tháng", "Thông tin tàu thu\nmua/chuyển tải", "", "Vị trí thu mua,\nchuyển tải", "", "Đã bán/chuyển tải", "", "Thuyền trưởng \ntàu thu mua,\nchuyểntải"],
        ["", "", "Số đăng ký\ntàu", "Số giấy phép\nkhaithác", "Vĩ độ", "Kinh độ", "Tên loài\nthủy sản", "Khối lượng\n(kg)", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
    ]
    table3 = Table(data3, colWidths=[1*cm, 3*cm, 2.5*cm, 3*cm, 2*cm, 2*cm, 3*cm, 3*cm, 3.5*cm])
    tsyle3 = TableStyle([
        # col, row
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONT", (0, 0), (-1, -1), "Times_New_Roman",13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ("SPAN", (0, 0), (0, 1)), # tt
        ("SPAN", (1, 0), (1, 1)), # ngày, tháng
        ("SPAN", (2, 0), (3, 0)), # thông tin thu mua, chuyển tải
        ("SPAN", (4, 0), (5, 0)), # vị trí thu mua, chuyển tải
        ("SPAN", (6, 0), (7, 0)), # đã bán, chuyển tải
        ("SPAN", (8, 0), (8, 1)), # thuyển trưởng ký
    ])
    table3.setStyle(tsyle3)
    flow_obj5.append(table3)
    flow_obj5.append(Spacer(1, 0.5*cm))
    # flow_obj5.append(Paragraph("Ngày ...... tháng ...... năm ......", paragraph_normal))
    # flow_obj5.append(Paragraph("Thuyền trưởng", paragrap_bold))
    # flow_obj5.append(Paragraph("(ký, ghi rõ họ tên)", paragraph_normal))

    frame5.addFromList(flow_obj5, pdf)

    flow_obj6 = []
    frame6 = Frame(
        x1=16*cm,
        y1=4*cm,
        width=10*cm,
        height=6*cm,
        showBoundary=0
    )

    paragraph_bold_center = styles['Title']
    paragraph_bold_center.fontSize = 13
    paragraph_bold_center.alignment = 1
    paragraph_bold_center.fontName = "Times_New_Roman_Bold"
    paragraph_bold_center.spaceAfter = 1.1 * paragraph_bold_center.fontSize 

    paragraph_normal_center = styles['Normal']
    paragraph_normal_center.fontSize = 13
    paragraph_normal_center.alignment = 1
    paragraph_normal_center.fontName = "Times_New_Roman"
    paragraph_normal_center.spaceAfter = 1.1 * paragraph_normal_center.fontSize 

    flow_obj6.append(Paragraph("Ngày ..... tháng ..... năm ......", paragraph_normal_center))
    flow_obj6.append(Paragraph("Thuyền trưởng", paragraph_bold_center))
    flow_obj6.append(Paragraph("(ký, ghi rõ họ tên)", paragraph_normal_center))
    frame6.addFromList(flow_obj6, pdf)

    pdf.showPage()

    pdf.save()

    return response 


    # Code part 2
    # page_width, page_height = landscape(letter)
    # # phần này cần xem lại định dạng cm và A4 nằm ngang
    # pdf = SimpleDocTemplate(response, pagesize=(page_width, page_height), topMargin=inch, bottomMargin=inch)

    # story = []
    # styles = getSampleStyleSheet()
    # style_normal = styles['Normal']

    # font_path = 'times.ttf'  # Đường dẫn đến font chữ Times New Roman
    # pdfmetrics.registerFont(TTFont('Times_New_Roman', font_path))
    # style_normal.fontName = 'Times_New_Roman'

    # # Nội dung sử dụng Unicode cho tiếng Việt
    # content = [
    #     "Tổng cục thủy sản",
    #     f"Chủ tàu: {ediary.IDThietBi.IDChuTau.HoTen} .......... Thuyền trưởng: {ediary.IDThietBi.IDThuyenTruong.HoTen}",
    #     "Chuyến biển: 1 .......... Số lượng mẻ lưới: 4......",
    #     "STT   Mã tàu      Ngày tạo nhật ký   Chủ tàu      Mã chủ tàu      Mã nhật ký      Ghi chú",
    #     f"1     {ediary.IDThietBi.SoDangKy}    {ediary.NgayTao}        {ediary.IDThietBi.IDChuTau.HoTen}     {ediary.IDThietBi.IDChuTau.CMND_CCCD}      {ediary.MaNhatKy}     "  # Dùng Unicode cho tiếng Việt
    # ]

    # for line in content:
    #     p = Paragraph(line, style_normal)
    #     story.append(p)
    #     story.append(Spacer(1, 0.2 * inch))  # Thêm khoảng trắng giữa các dòng

    # # Thêm PageBreak nếu cần thiết để phù hợp với số lượng trang
    # while len(story) * 0.2 * inch < page_height:
    #     story.append(Spacer(1, 0.2 * inch))

    # # Add the content to the PDF
    # pdf.build(story)

    # return response





    # Code Part 1
    # Tạo một đối tượng SimpleDocTemplate
    # pdf = SimpleDocTemplate(response, pagesize=letter)
    # styles = getSampleStyleSheet()

    # # Tạo nội dung PDF
    # story = []
    # styles = getSampleStyleSheet()
    # style_normal = styles['Normal']
    # p = Paragraph("This is an example PDF generated using ReportLab in Django.", style_normal)
    # story.append(p)

    # p1 = Paragraph("Chủ tàu: Nguyễn Văn A .......... Thuyền trưởng: Nguyễn Văn B", style_normal)
    # story.append(p1)

    # p2 = Paragraph("Chuyến biển: 1 .......... Số lượng mẻ lưới: 4......", style_normal)
    # story.append(p2)

    # # Tạo một bảng đơn giản
    # data = [['STT', 'Mã tàu', 'Ngày tạo nhật ký', 'Chủ tàu', 'Mã chủ tàu', 'Mã nhật ký', 'Ghi chú'],
    #         ['1', 'BĐ-12314', '21-01-2024', 'Nguyễn Văn A', '', 'NK-21355', '']]
    # table = Table(data)
    # table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
    #                            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    #                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    #                            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    #                            ('BOTTOMPADDING', (0,0), (-1,0), 12),
    #                            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    #                            ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    # story.append(table)

    # # Add the content to the PDF
    # pdf.build(story)

    # return response


@login_required(login_url='/login/')
def device_view(request):
    '''Quản lý tàu cá'''
    titles = ["STT","IMO","Số hiệu tàu","Chủ tàu","Loại tàu","Nơi đăng ký","Thuyền trưởng","Cảng cá ĐK","TBNKKT","Thao tác"]
    items = BangTau.objects.all().order_by('-ID')
    return render(request, 'core/device.html', {
        'titles': titles,
        'items': items, 
    }, status=200)


@login_required(login_url='/login/')
def add_new_device_view(request):
    '''Thêm tàu cá mới'''
    if request.method == 'POST':
        print(request.POST)

        TenTau = request.POST.get('tenTau')
        try:
            ChuTau = BangChuTau.objects.get(pk=request.POST['chuTau'])
        except Exception as e:
            return redirect('add-device')

        try:
            LoaiTau = BangMaLoaiTau.objects.get(pk=request.POST['loaiTau'])
        except Exception as e:
            return redirect('add-device')

        # xử lý số đăng ký trùng, IMO trùng
        SoDangKy = request.POST.get('soDangKy')
        HoHieu = request.POST.get('hoHieu')
        CoHieu = request.POST.get('coHieu')
        IMO = request.POST.get('IMO')
        
        try:
            NoiDangKy = BangDonViHanhChinhCapTinh.objects.get(pk=request.POST['noiDangKy'])
        except Exception as e:
            return redirect('add-device')
        print(NoiDangKy)
        try:
            CangCaDangKy = BangCangCa.objects.get(pk=request.POST['cangCaDangKy'])
        except Exception as e:
            return redirect('add-device')
        
        try:
            CangCaPhu = BangCangCa.objects.get(pk=request.POST['cangCaPhu'])
        except:
            return redirect('add-device')

        try:
            NgheChinh = BangNganhNgheKhaiThac.objects.get(pk=request.POST['ngheChinh'])
        except Exception as e:
            return redirect('add-device')
        
        NghePhu1 = BangNganhNgheKhaiThac.objects.get(pk=request.POST['nghePhu1'])
        NgayDangKy = request.POST.get('ngayDangKy')
        NgayHetHanDangKy = request.POST.get('ngayHetHanDangKy')
        NgaySanXuatTau = request.POST.get('ngaySanXuatTau')
        NgayHetHanSuDung = request.POST.get('ngayHetHanSuDung')
        
        try:
            MaThietBi = BangThietBiNhatKyKhaiThac.objects.get(pk=request.POST['maThietBi'])
        except Exception as e:
            return redirect('add-device')
        
        try:
            ThuyenTruong = BangThuyenTruong.objects.get(pk=request.POST['thuyenTruong'])
        except Exception as e:
            return redirect('add-device')
        
        try:
            Tinh = BangDonViHanhChinhCapTinh.objects.get(pk=request.POST['tinhThanhPho'])
        except Exception as e:
            return redirect('add-device')
        
        SoLuongThuyenVien = request.POST.get('soLuongThuyenVien')
        TongTaiTrong = request.POST.get('tongTaiTrong')
        ChieuDaiLonNhat = request.POST.get('chieuDaiLonNhat')
        ChieuRongLonNhat = request.POST.get('chieuRongLonNhat')
        CongSuatMay = request.POST.get('congSuatMay')
        MonNuoc = request.POST.get('monNuoc')
        DungTichHamCa = request.POST.get('dungTichHamCa')
        VanTocDanhBat = request.POST.get('vanTocDanhBat')
        VanTocHanhTrinh = request.POST.get('vanTocHanhTrinh')
        ThongSoNguCu = request.POST.get('thongSoNguCu')

        new_ship = BangTau.objects.create(
            SoDangKy=SoDangKy,
            TenTau=TenTau,
            HoHieu=HoHieu,
            CoHieu=CoHieu,
            IMO=IMO,
            NoiDangKy=NoiDangKy,
            CangCaDangKy=CangCaDangKy,
            NgheChinh=NgheChinh,
            NghePhu1=NghePhu1,
            NgayDangKy=NgayDangKy,
            NgayHetHanDangKy=NgayHetHanDangKy,
            TongTaiTrong=TongTaiTrong,
            ChieuDaiLonNhat=ChieuDaiLonNhat,
            ChieuRongLonNhat=ChieuRongLonNhat,
            CongSuatMay=CongSuatMay,
            MonNuoc=MonNuoc,
            SoThuyenVien=SoLuongThuyenVien,
            NgaySanXuat=NgaySanXuatTau,
            NgayHetHan=NgayHetHanSuDung,
            LoaiTau=LoaiTau,
            DungTichHamCa=DungTichHamCa,
            VanTocDanhBat=VanTocDanhBat,
            VanTocHanhTrinh=VanTocHanhTrinh,
            IDDevice=MaThietBi,
            IDChuTau=ChuTau,
            IDThuyenTruong=ThuyenTruong,
            IDTinh=Tinh,
            ThongSoNguCu=ThongSoNguCu
        )

        MaThietBi.is_active = True
        MaThietBi.save()
        ThuyenTruong.hasShip = True
        ThuyenTruong.save()

        messages.success(request, f"Thêm thông tin tàu {SoDangKy} thành công!!")
        return redirect('device-view')


    city_list = BangDonViHanhChinhCapTinh.objects.all()
    shipowners = BangChuTau.objects.all()
    ship_type_list = BangMaLoaiTau.objects.all()
    gate_list = BangCangCa.objects.all()
    job_list = BangNganhNgheKhaiThac.objects.all()
    device_list = BangThietBiNhatKyKhaiThac.objects.all().exclude(is_active=True) # danh sách thiết bị chưa kích hoạt
    captain_list = BangThuyenTruong.objects.all().exclude(hasShip=True) # danh sách các thuyền trưởng chưa có tàu nào
    today = date.today()
    return render(request, 'core/add-new-device.html', {
        'shipowners': shipowners,
        'ship_type_list': ship_type_list,
        'city_list': city_list,
        'gate_list': gate_list,
        'job_list': job_list,
        'device_list': device_list,
        'captain_list': captain_list,
        'today': today,
    }, status=200)


@login_required(login_url='/login/')
def edit_device_view(request, pk):
    if request.method == 'POST':
        TenTau = request.POST.get('tenTau')
        try:
            ChuTau = BangChuTau.objects.get(pk=request.POST['chuTau'])
        except Exception as e:
            return redirect('add-device')

        try:
            LoaiTau = BangMaLoaiTau.objects.get(pk=request.POST['loaiTau'])
        except Exception as e:
            return redirect('add-device')

        # xử lý số đăng ký trùng, IMO trùng
        SoDangKy = request.POST.get('soDangKy')
        HoHieu = request.POST.get('hoHieu')
        CoHieu = request.POST.get('coHieu')
        IMO = request.POST.get('IMO')
        
        try:
            NoiDangKy = BangDonViHanhChinhCapTinh.objects.get(pk=request.POST['noiDangKy'])
        except Exception as e:
            return redirect('add-device')
        print(NoiDangKy)
        try:
            CangCaDangKy = BangCangCa.objects.get(pk=request.POST['cangCaDangKy'])
        except Exception as e:
            return redirect('add-device')
        
        try:
            CangCaPhu = BangCangCa.objects.get(pk=request.POST['cangCaPhu'])
        except:
            return redirect('add-device')

        try:
            NgheChinh = BangNganhNgheKhaiThac.objects.get(pk=request.POST['ngheChinh'])
        except Exception as e:
            return redirect('add-device')
        
        NghePhu1 = BangNganhNgheKhaiThac.objects.get(pk=request.POST['nghePhu1'])
        NgayDangKy = request.POST.get('ngayDangKy')
        NgayHetHanDangKy = request.POST.get('ngayHetHanDangKy')
        NgaySanXuatTau = request.POST.get('ngaySanXuatTau')
        NgayHetHanSuDung = request.POST.get('ngayHetHanSuDung')
        
        try:
            MaThietBi = BangThietBiNhatKyKhaiThac.objects.get(pk=request.POST['maThietBi'])
        except Exception as e:
            return redirect('add-device')
        
        try:
            ThuyenTruong = BangThuyenTruong.objects.get(pk=request.POST['thuyenTruong'])
        except Exception as e:
            return redirect('add-device')
        
        try:
            Tinh = BangDonViHanhChinhCapTinh.objects.get(pk=request.POST['tinhThanhPho'])
        except Exception as e:
            return redirect('add-device')
        
        SoLuongThuyenVien = request.POST.get('soLuongThuyenVien')
        TongTaiTrong = request.POST.get('tongTaiTrong')
        ChieuDaiLonNhat = request.POST.get('chieuDaiLonNhat')
        ChieuRongLonNhat = request.POST.get('chieuRongLonNhat')
        CongSuatMay = request.POST.get('congSuatMay')
        MonNuoc = request.POST.get('monNuoc')
        DungTichHamCa = request.POST.get('dungTichHamCa')
        VanTocDanhBat = request.POST.get('vanTocDanhBat')
        VanTocHanhTrinh = request.POST.get('vanTocHanhTrinh')
        ThongSoNguCu = request.POST.get('thongSoNguCu')

        ship = BangTau.objects.get(pk=pk)

        tbnkkt = ship.IDDevice
        tbnkkt.is_active = False
        tbnkkt.save()

        captain = ship.IDThuyenTruong
        captain.hasShip = False
        captain.save()

        ship.SoDangKy=SoDangKy
        ship.TenTau=TenTau
        ship.HoHieu=HoHieu
        ship.CoHieu=CoHieu
        ship.IMO=IMO
        ship.NoiDangKy=NoiDangKy
        ship.CangCaDangKy = CangCaDangKy
        ship.NgheChinh=NgheChinh
        ship.NghePhu1=NghePhu1
        ship.NgayDangKy=NgayDangKy
        ship.NgayHetHanDangKy=NgayHetHanDangKy
        ship.TongTaiTrong=TongTaiTrong
        ship.ChieuDaiLonNhat=ChieuDaiLonNhat
        ship.ChieuRongLonNhat=ChieuRongLonNhat
        ship.CongSuatMay=CongSuatMay
        ship.MonNuoc=MonNuoc
        ship.SoThuyenVien=SoLuongThuyenVien
        ship.NgaySanXuat=NgaySanXuatTau
        ship.NgayHetHan=NgayHetHanSuDung
        ship.LoaiTau=LoaiTau
        ship.DungTichHamCa=DungTichHamCa
        ship.VanTocDanhBat=VanTocDanhBat
        ship.VanTocHanhTrinh=VanTocHanhTrinh
        ship.IDDevice=MaThietBi
        ship.IDChuTau=ChuTau
        ship.IDThuyenTruong=ThuyenTruong
        ship.IDTinh=Tinh
        ship.ThongSoNguCu=ThongSoNguCu

        MaThietBi.is_active = True
        MaThietBi.save()
        ThuyenTruong.hasShip = True
        ThuyenTruong.save()

        ship.save()    
        messages.success(request, f"Cập nhật thông tin tàu {ship.SoDangKy} thành công!!")
        return redirect('device-view')


    try:
        item = BangTau.objects.get(pk=pk)
    except Exception as e:
        messages.info(request, f'Không tìm thấy thông tin tàu hợp lệ!')
        redirect('device-view')
    
    shipowners = BangChuTau.objects.all()
    ship_type_list = BangMaLoaiTau.objects.all()
    city_list = BangDonViHanhChinhCapTinh.objects.all()
    gate_list = BangCangCa.objects.all()
    job_list = BangNganhNgheKhaiThac.objects.all()
    device_list = BangThietBiNhatKyKhaiThac.objects.all().exclude(is_active=True)
    captain_list = BangThuyenTruong.objects.all().exclude(hasShip=True)

    return render(request, 'core/edit-device.html', {
        'item': item,
        'shipowners': shipowners,
        'ship_type_list': ship_type_list,
        'city_list': city_list,
        'gate_list': gate_list,
        'job_list': job_list,
        'device_list': device_list,
        'captain_list': captain_list,
    }, status=200)


@login_required(login_url='/login/')
def delete_device_view(request, pk):
    try:
        ship = BangTau.objects.get(pk=pk)
        soDangKy = ship.SoDangKy

        tbnkkt = ship.IDDevice
        tbnkkt.is_active = False
        tbnkkt.save()

        captain = ship.IDThuyenTruong
        captain.hasShip = False
        captain.save()
        
        ship.delete()
        messages.success(request, f"Xóa tàu {soDangKy} thành công!!")
        return redirect('device-view')
    except Exception as e:
        messages.error(request, f"Tàu mới pk = {pk} không tồn tại!!")
        return redirect('device-view')


@login_required(login_url='/login/')
def search_device_view(request):
    query = request.GET.get('q')
    query_type = request.GET.get('query-type')
    # print(query)
    # print(query_type)
    titles = ["STT","IMO","Số hiệu tàu","Chủ tàu","Loại tàu","Nơi đăng ký","Thuyền trưởng","Cảng cá ĐK","TBNKKT","Thao tác"]
    items = BangTau.objects.all().order_by('-ID')

    if query_type == '1':
        items = BangTau.objects.filter(Q(IMO__icontains=query)).order_by('-ID')
        if len(items) == 0:
            messages.info(request, f'Không tìm thấy IMO hợp lệ!')
    elif query_type == '2':
        items = BangTau.objects.filter(Q(SoDangKy__icontains=query)).order_by('-ID') 
        if len(items) == 0:
            messages.info(request, f'Không tìm thấy số đăng ký tàu hợp lệ!')
    elif query_type == '3':
        users = BangChuTau.objects.filter(Q(HoTen__icontains=query)).order_by('-ID')
        # print(users)
        items = []
        for user in users:
            item = user.bangtau_chutau.all()
            # print(item)
            items.extend(item)
        # print(items) 
        if len(items) == 0:
            messages.info(request, f'Không tìm thấy chủ tàu hợp lệ!')
    elif query_type == '4':
        users = BangThuyenTruong.objects.filter(Q(HoTen__icontains=query)).order_by('-ID').exclude(hasShip=False)
        items = []
        for user in users:
            print(user)
            item = user.bangtau
            items.append(item)
        # thuyentruong = BangThuyenTruong.objects.first()
        # bangtau_instance = thuyentruong.bangtau
        # print(bangtau_instance)
        if len(items) == 0:
            messages.info(request, f'Không tìm thấy thông tin thuyền trưởng hợp lệ!')
    elif query_type == '5':
        devices = BangThietBiNhatKyKhaiThac.objects.filter(Q(SerialNumber__icontains=query)).exclude(is_active=False)
        items = []
        for d in devices:
            item = d.bangtau
            items.append(item)
        if len(items) == 0:
            messages.info(request, f'Không tìm thấy thông tin thiết bị hợp lệ!')
    elif query_type == '6':
        items = BangTau.objects.filter(Q(IMO__icontains=query) | Q(SoDangKy__icontains=query))  
        if len(items) == 0:
            messages.info(request, f'Không tìm thấy thông tin IMO hoặc Số đăng ký hợp lệ!')

    return render(request, 'core/device.html', {
        'titles': titles,
        'items': items, 
    }, status=200)
    

@login_required(login_url='/login/')
def download_device_data(request, number):
    number = int(number)
    wb = Workbook()
    ws = wb.active # worksheet
    if number == '1':
        qty = 50
    elif number == '2':
        qty = 100
    elif number == '3':
        qty = 200
    elif number == '4':
        qty = 500
    else:
        qty = None 
    if qty is not None:
        ship_list = BangTau.objects.all()[:qty]
    else:
        ship_list = BangTau.objects.all()

    ws["A1"] = "STT"
    ws["B1"] = "IMO"
    ws["C1"] = "Số hiệu tàu"
    ws["D1"] = "Chủ tàu"
    ws["E1"] = "Loại tàu"
    ws["F1"] = "Nơi đăng ký"
    ws["G1"] = "Thuyền trưởng"
    ws["H1"] = "Cảng cá ĐK"
    ws["I1"] = "TBNKKT" 

    for i, ship in enumerate(ship_list, start=2):
        ws[f"A{i}"] = i - 1
        ws[f"B{i}"] = ship.IMO
        ws[f"C{i}"] = ship.SoDangKy
        ws[f"D{i}"] = ship.IDChuTau.HoTen
        ws[f"E{i}"] = ship.LoaiTau.IDLoaiTau
        ws[f"F{i}"] = ship.NoiDangKy.TenTiengViet
        ws[f"G{i}"] = ship.IDThuyenTruong.HoTen
        ws[f"H{i}"] = ship.CangCaDangKy.Ten
        ws[f"I{i}"] = ship.IDDevice.SerialNumber

    _, filepath = tempfile.mkstemp(suffix='.xlsx')
    wb.save(filepath)

    with open(filepath, 'rb') as f:
        excel_data = f.read()
    
    response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="example.xlsx"'
    return response


@login_required(login_url='/login/')
def shipowners_view(request):
    titles = ["STT", "Họ tên", "Số CMND(CCCD)", "Địa chỉ", "Trạm bờ", "Email", "Số điện thoại", "Người dùng", "Thao tác"]
    captains = list(BangThuyenTruong.objects.all())
    shipowners = list(BangChuTau.objects.all())

    for captain in captains:
        captain.type = 'captain'
    for shipowner in shipowners:
        shipowner.type = 'shipowner'    
    
    combined_list = captains + shipowners
    random.shuffle(combined_list)
    return render(request, 'core/shipowners.html', {
        'titles': titles,
        'items': combined_list,
    }, status=200)


@login_required(login_url='/login/')
def search_shipowners_view(request):
    query = request.GET.get('q')
    query_type = request.GET.get('query-type')
    titles = ["STT", "Họ tên", "Số CMND(CCCD)", "Địa chỉ", "Trạm bờ", "Email", "Số điện thoại", "Người dùng", "Thao tác"]
    captains = list(BangThuyenTruong.objects.all())
    shipowners = list(BangChuTau.objects.all())

    if query_type == '1':
        captains = []
        shipowners = list(BangChuTau.objects.filter(Q(HoTen__icontains=query)))
        if len(captains) == 0 and len(shipowners) == 0:
            messages.info(request, f"Không tìm thấy thông tin họ tên chủ tàu hợp lệ với query='{query}'")
    elif query_type == '2':
        captains = list(BangThuyenTruong.objects.filter(Q(HoTen__icontains=query)))
        shipowners = []
        if len(captains) == 0 and len(shipowners) == 0:
            messages.info(request, f"Không tìm thấy thông tin họ tên thuyền trưởng hợp lệ với query='{query}'")
    elif query_type == '3':
        captains = []
        shipowners = list(BangChuTau.objects.filter(Q(IDChuTau__icontains=query)))
        if len(captains) == 0 and len(shipowners) == 0:
            messages.info(request, f"Không tìm thấy thông tin mã chủ tàu hợp lệ với query='{query}'")
    elif query_type == '4':
        captains = list(BangThuyenTruong.objects.filter(Q(IDThuyenTruong__icontains=query)))
        shipowners = []
        if len(captains) == 0 and len(shipowners) == 0:
            messages.info(request, f"Không tìm thấy thông tin mã thuyền trưởng hợp lệ với query='{query}'") 
    elif query_type == '5':
        captains = list(BangThuyenTruong.objects.filter(Q(CMND_CCCD__icontains=query)))
        shipowners = list(BangChuTau.objects.filter(Q(CMND_CCCD__icontains=query)))
        if len(captains) == 0 and len(shipowners) == 0:
            messages.info(request, f"Không tìm thấy thông tin CMND/CCCD hợp lệ với query='{query}'") 
    elif query_type == '6':
        captains = list(BangThuyenTruong.objects.filter(Q(DienThoai__icontains=query)))
        shipowners = list(BangChuTau.objects.filter(Q(DienThoai__icontains=query)))
        if len(captains) == 0 and len(shipowners) == 0:
            messages.info(request, f"Không tìm thấy thông tin số điện thoại hợp lệ với query='{query}'") 
    elif query_type == '7':
        captains = list(BangThuyenTruong.objects.filter(Q(HoTen__icontains=query) | Q(IDThuyenTruong__icontains=query) | Q(CMND_CCCD__icontains=query) | Q(DienThoai__icontains=query)))
        shipowners = list(BangChuTau.objects.filter(Q(HoTen__icontains=query) | Q(IDChuTau__icontains=query) | Q(CMND_CCCD__icontains=query) | Q(DienThoai__icontains=query)))
        if len(captains) == 0 and len(shipowners) == 0:
            messages.info(request, f"Không tìm thấy thông tin truy vấn hợp lệ với query='{query}'") 


    for captain in captains:
        captain.type = 'captain'
    for shipowner in shipowners:
        shipowner.type = 'shipowner'

    combined_list = captains + shipowners
    random.shuffle(combined_list)
    return render(request, 'core/shipowners.html', {
        'titles': titles,
        'items': combined_list,
    }, status=200)


@login_required(login_url='/login/')
def add_shipowners_view(request):
    if request.method == 'POST':
        HoTen = request.POST.get('hoTen')
        CMND_CCCD = request.POST.get('CMND-CCCD')
        NgaySinh = request.POST.get('ngaySinh')
        DiaChi = request.POST.get('diaChi')
        DienThoai = request.POST.get('dienThoai')
        Fax = request.POST.get('fax')
        Email = request.POST.get('email')
        try:
            Huyen = BangDonViHanhChinhCapHuyen.objects.get(MaHuyen=request.POST['maHuyen'])
        except Exception as e:
            messages.error(request, f"Không tồn tại huyện có mã tỉnh '{request.POST['maHuyen']}'")
            return redirect('add-shipowners')
        ChucDanh = request.POST.get('chucDanh')

        if ChucDanh == '1':
            new_shipowner = BangChuTau.objects.create(
                HoTen=HoTen,
                CMND_CCCD=CMND_CCCD,
                NgaySinh=NgaySinh,
                DiaChi=DiaChi,
                DienThoai=DienThoai,
                Fax=Fax,
                Email=Email,
                MaHuyen=Huyen
            )
            messages.success(request, f"Thêm thông tin chủ tàu mới thành công!!!")
            return redirect('shipowners-view')
        elif ChucDanh == '2':
            new_captain = BangThuyenTruong.objects.create(
                HoTen=HoTen,
                CMND_CCCD=CMND_CCCD,
                NgaySinh=NgaySinh,
                DiaChi=DiaChi,
                DienThoai=DienThoai,
                Fax=Fax,
                Email=Email,
                MaHuyen=Huyen
            )
            messages.success(request, f"Thêm thông tin thuyền trưởng mới thành công!!!")
            return redirect('shipowners-view')
        else:
            messages.error(request, "Lỗi không đúng định dạng dữ liệu yêu cầu!!!")
            return redirect('shipowners-view')
    distric_list = BangDonViHanhChinhCapHuyen.objects.all()
    return render(request, 'core/add-new-shipowners.html', {
        'distric_list': distric_list,
    }, status=200) 


@login_required(login_url='/login/')
def edit_shipowners_view(request, pk, user_type):
    if request.method == 'POST':

        Huyen = BangDonViHanhChinhCapHuyen.objects.get(pk=request.POST['maHuyen'])
        HoTen = request.POST.get('hoTen')
        CMND_CCCD = request.POST.get('CMND-CCCD')
        NgaySinh = request.POST.get('ngaySinh')
        DiaChi = request.POST.get('diaChi')
        DienThoai = request.POST.get('dienThoai')
        Fax = request.POST.get('fax')
        Email = request.POST.get('email')

        if user_type == 'captain':
            try:
                captain = BangThuyenTruong.objects.get(pk=pk)
            except Exception as e:
                messages.error(request, f"Không tìm thấy thông tin thuyền trưởng với ID = {pk}")
            captain.HoTen = HoTen
            captain.CMND_CCCD = CMND_CCCD
            captain.NgaySinh = NgaySinh
            captain.DiaChi = DiaChi
            captain.DienThoai = DienThoai
            captain.Fax = Fax 
            captain.Email = Email
            captain.Huyen = Huyen
            captain.save()
            
            messages.info(request, f"Cập nhật thông tin thuyền trưởng {HoTen} - {CMND_CCCD} thành công!")
            return redirect('shipowners-view')
        elif user_type == 'shipowner':
            try:
                shipowner = BangChuTau.objects.get(pk=pk)
            except Exception as e:
                messages.error(request, f"Không tìm thấy thông tin thuyền trưởng với ID = {pk}")
            shipowner.HoTen = HoTen
            shipowner.CMND_CCCD = CMND_CCCD
            shipowner.NgaySinh = NgaySinh
            shipowner.DiaChi = DiaChi
            shipowner.DienThoai = DienThoai
            shipowner.Fax = Fax 
            shipowner.Email = Email
            shipowner.Huyen = Huyen
            shipowner.save()
            
            messages.info(request, f"Cập nhật thông tin chủ tàu {HoTen} - {CMND_CCCD} thành công!")
            return redirect('shipowners-view')
        else:
            pass # return 404 page

    distric_list = BangDonViHanhChinhCapHuyen.objects.all()
    if user_type == 'captain':
        try:
            captain = BangThuyenTruong.objects.get(pk=pk)
        except Exception as e:
            messages.error(request, "Không tìm thấy thông tin thuyền trưởng!!!")
            return redirect('shipowners-view') 

        return render(request, 'core/edit-shipowners.html', {
            'item': captain,
            'user_type': 'captain',
            'distric_list': distric_list,
        }, status=200)
    elif user_type == 'shipowner':
        try:
            shipowner = BangChuTau.objects.get(pk=pk)
        except Exception as e:
            messages.error(request, "Không tìm thấy thông tin chủ tàu!!!")
            return redirect('shipowners-view') 
        
        return render(request, 'core/edit-shipowners.html', {
            'item': shipowner,
            'user_type': 'shipowner',
            'distric_list': distric_list,
        }, status=200)
    else:
        messages.error(request, "Lỗi truy vấn!!!")
        return redirect('shipowners-view') 


@login_required(login_url='/login/')
def delete_shipowners_view(request, pk):
    pass
    

@login_required(login_url='/login/')
def account_view(request):
    titles = ["STT", "Tên tài khoản", "Cấp độ tài khoản", "Tình trạng", "Loại tài khoản", "Địa chỉ", "Email", "Số điện thoại", "Thao tác"]
    return render(request, 'core/account.html', {
        'titles': titles,
    }, status=200)


@csrf_exempt
def login_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if username == 'admin':
                if password == '@Long1705':
                    return JsonResponse({
                        'message': 'Login successfully!', 
                        'passed': True, 
                        'username': 'Long02'
                    }, status=200)
                else:
                    return JsonResponse({
                        'message': 'Password is not correct!',
                        'passed': False,
                        'username': 'Anonymous'
                    }, staus=401) 
            else:
                return JsonResponse({
                    'message': 'Username does not exits!',
                    'passed': False,
                    'username': 'Anonymous'
                })
        except Exception as e:
            return JsonResponse({
                'message': 'Server error!',
                'passed': False,
                'username': 'Anonymous'
            })
    else:
        return JsonResponse({
            'message': 'Method not allowed!',
            'passed': False,
            'username': 'Anonymous'
        })

    
def test_api_mobile(request):
    return JsonResponse({
        'message': 'Hello World!',
        'status': 200
    }, status=200)


def ship_name_list(request):
    return JsonResponse({
        'message': 'Danh sách tàu cá',
        'status': 200,
        'data': [
            {
                'so_hieu_tau': 'KH-12235',
                'chu_tau': 'Nguyễn Văn Long'
            },
            {
                'so_hieu_tau': 'BĐ-12935',
                'chu_tau': 'Nguyễn Văn Long'
            },
            {
                'so_hieu_tau': 'HP-99999',
                'chu_tau': 'Nguyễn Văn Long'
            },
            {
                'so_hieu_tau': 'HN-29299',
                'chu_tau': 'Nguyễn Văn Long'
            },
        ]
    }, status=200)


def ship_realtime_location(request):
    now = datetime.now()
    formatted_date = now.strftime("%d %b, %Y %H:%M:%S")
    print(formatted_date)
    # 16.344088, 108.599521 [16.408051, 108.489041, 16.415336, 108.251537, 16.583879, 107.982372]
    # 13.811880, 109.594370 [13.658198, 109.478250, 13.509807, 109.674731, 13.100527, 109.479232]
    # 12.963734, 109.654796 [12.824108, 109.441995, 12.655258, 109.672265, 12.336105, 109.328733]
    # 11.457285, 109.207992 [11.636259, 109.196456, 11.819430, 109.472452, 11.992313, 109.358127]
    return JsonResponse({
        'message': 'Vị trí tàu cá hiện tại.',
        'status': 200,
        'ship_list': [
            {
                'so_hieu_tau': 'KH-12235',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '1705',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-123455',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 16.344088,
                    'lng': 108.599521,
                },
                'time': formatted_date,
            },
            {
                'so_hieu_tau': 'BĐ-12935',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '1777',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-129455',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 13.811880,
                    'lng': 109.594370,
                },
                'time': formatted_date,
            },
            {
                'so_hieu_tau': 'HP-99999',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '2000',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-129955',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 12.963734,
                    'lng': 109.654796,
                },
                'time': formatted_date,
            },
            {
                'so_hieu_tau': 'HN-29299',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '1723',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-123685',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 11.457285,
                    'lng': 109.207992,
                },
                'time': formatted_date,
            },
        ],
    }, status=200) 


def ship_location_log(request):
    return JsonResponse({
        'message': 'Lịch sử vị trí tàu cá',
        'status': 200,
        'log': {
            'tc1': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'KH-12235',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '1705',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-123455',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 16.408051,
                        'lng': 108.489041,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 16.415336,
                        'lng': 108.251537,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 16.583879,
                        'lng': 107.982372,
                        'date': '29-11-2023',
                    },
                ]
            },


            'tc2': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'BĐ-12935',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '1777',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-129455',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 13.658198,
                        'lng': 109.478250,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 13.509807,
                        'lng': 109.674731,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 13.100527,
                        'lng': 109.479232,
                        'date': '29-11-2023',
                    },
                ]
            },


            'tc3': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'HP-99999',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '2000',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-129955',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 12.824108,
                        'lng': 109.441995,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 12.655258,
                        'lng': 109.672265,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 12.336105,
                        'lng': 109.328733,
                        'date': '29-11-2023',
                    },
                ]
            },


            'tc4': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'HN-29299',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '1723',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-123685',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 11.636259,
                        'lng': 109.196456,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 11.819430,
                        'lng': 109.472452,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 11.992313,
                        'lng': 109.358127,
                        'date': '29-11-2023',
                    },
                ]
            },
        },  
    }, status=200)


def mining_log(request):
    return JsonResponse({
        'message': 'Nhật ký khai thác điện tử',
        'status': 200,
        'data': [
            {
                'so_hieu_tau': 'KH-12235',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
            {
                'so_hieu_tau': 'HN-29299',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá bơn',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá bơn',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá bò hoa vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá nục thuôn',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
            {
                'so_hieu_tau': 'HP-99999',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Hồng Lang',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
            {
                'so_hieu_tau': 'BĐ-12935',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Ồ',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chấm',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Vằn',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Vằn',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chấm',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chấm',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chù',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
        ]
    }, status=200)
    


# RESTful API
@login_required(login_url='/login/')
def get_location_view_api(request, pk):
    try:
        ship = BangTau.objects.get(pk=pk)
    except Exception as e:
        return JsonResponse({
            'status': 404,
            'message': 'Ship not Found!',
            'bundle': {}
        }, status=404)

    location = BangViTriTau.objects.filter(IDTau=ship).order_by('-Ngay')[0]
    return JsonResponse({
        'status': 200,
        'message': f'Get info of ship: {ship.SoDangKy} successfully!',
        'bundle': {
            'shipowner': ship.IDChuTau.HoTen,
            'captain': ship.IDThuyenTruong.HoTen,
            'lat': location.ViDo,
            'lng': location.KinhDo,
            'date': location.Ngay,
        }
    }, status=200)
