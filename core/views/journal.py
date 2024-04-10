from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 

from core.models import * 

from django.db.models import Q
from django.contrib import messages 
from django.http import HttpResponse, JsonResponse 

# reportlab lib 
from reportlab.lib.pagesizes import letter, landscape 
from reportlab.pdfgen import canvas 
from reportlab.lib import colors 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib.units import cm 
from reportlab.platypus import Frame, Paragraph, Table, TableStyle, Spacer

from collections import defaultdict
from datetime import datetime


@login_required(login_url='/login/')
def journal_test_view(request):
    journal = BangNhatKy.objects.get(pk=8)
    print(journal)
    nets = BangMeLuoi.objects.filter(IDChuyenBien=journal.IDChuyenBien)
    print(nets)

    # tạo một từ điển để lưu tổng số lượng của từng loài cá
    species_totals = defaultdict(int) # species: giống loài

    # duyệt qua danh sách các mẻ lưới
    for net in nets:
        species_in_net = BangLoaiCaDuocDanhBatTrongMeLuoi.objects.filter(IDMeLuoi=net)

        for species in species_in_net:
            species_totals[species.IDLoaiCa] += species.SanLuong 
    top_6_species = sorted(species_totals.items(), key=lambda x: x[1], reverse=True)[:6]
    top_6_species_name = [BangLoaiCaDanhBat.objects.get(ID=species_id.ID).Ten for species_id, _ in top_6_species]

    quantity_matrix = []
    for net in nets:
        net_quantities = []
        species_in_net = BangLoaiCaDuocDanhBatTrongMeLuoi.objects.filter(IDMeLuoi=net)

        for species_id, _ in top_6_species:
            quantity = next((species.SanLuong for species in species_in_net if species.IDLoaiCa == species_id), 0)
            net_quantities.append(quantity)

        quantity_matrix.append(net_quantities)

    # In ra tên của 6 loài cá
    print("Tên của 6 loài cá có tổng sản lượng nhiều nhất:")
    print(top_6_species_name)

    # In ra mảng hai chiều
    print("Sản lượng của từng loài cá trong từng mẻ lưới:")
    for row in quantity_matrix:
        print(row)

    # lấy ra tên 6 loài cá
    # lấy ra sản lượng trong từng mẻ lưới của loài cá 

    return render(request, 'journal-test.html', {})


# Nhật ký khai thác thủy sản 
@login_required(login_url='/login/')
def journal_view(request):
    titles = ["STT", "Mã tàu", "Ngày tạo nhật ký", "Chủ tàu", "CMND (CCCD)", "Mã nhật ký", "Ghi chú", "Thao tác"]
    if request.user.user_type == '1' or request.user.is_staff:
        ships = BangTau.objects.all().order_by('SoDangKy')
        items = []
        for ship in ships:
            newest_journal = ship.bangnhatky_set.order_by('-NgayTao').first()
            if newest_journal is not None:
                # print(newest_journal)
                items.append(newest_journal)
        return render(request, 'core/journal.html', {
            'titles': titles,
            'items': items,
        }, status=200)
    else:
        ships = BangTau.objects.filter(Q(CangCaDangKy=request.user.staff.cangca)).order_by('SoDangKy')
        items = []
        for ship in ships:
            newest_journal = ship.bangnhatky_set.order_by('-NgayTao').first()
            if newest_journal is not None:
                items.append(newest_journal)
        return render(request, 'core/journal.html', {
            'titles': titles,
            'items': items,
        }, status=200)


# pdf view 
@login_required(login_url='/login/')
def journal_pdf_view(request, pk):
    response = generate_journal_pdf(request, pk)
    return HttpResponse(response.content, content_type='application/pdf')


# pdf detail view 
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

    # font_normal_path = '/home/administrator/eproject/times.ttf'
    # font_bold_path = '/home/administrator/eproject/timesbd.ttf'

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
    text = ediary.MaNhatKy
    text_width, text_height = pdf.stringWidth(text), 16
    # text_x = rect_x + (rect_width - text_width) / 2
    text_x = rect_x
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
    flow_obj1.append(Paragraph(f"NGHỀ CHÍNH: {ediary.IDThietBi.NgheChinh.Ten}.........(**)", h2_normal))

    flow_obj1.append(Paragraph(f"1. Họ và tên chủ tàu: {ediary.IDThietBi.IDChuTau.HoTen}.................; 2. Họ và tên thuyền trưởng: {ediary.IDThietBi.IDThuyenTruong.HoTen}..................", paragraph_normal))
    flow_obj1.append(Paragraph(f"3. Số đăng ký tàu: {ediary.IDThietBi.SoDangKy}.....; 4. Chiều dài lớn nhất của tàu: {ediary.IDThietBi.ChieuDaiLonNhat} m; 5. Tổng công suất máy chính: {ediary.IDThietBi.CongSuatMay} KW", paragraph_normal))
    flow_obj1.append(Paragraph(f"6. Số Giấy phép khai thác thủy sản: .......................Thời hạn đến: .....................................................", paragraph_normal))
    flow_obj1.append(Paragraph(f"7. Nghề phụ 1: {ediary.IDThietBi.NghePhu1.Ten}..; 8. Nghề phụ 2: .......................................", paragraph_normal))
    flow_obj1.append(Paragraph(f"9. Kích thước chủ yếu của ngư cụ (ghi cụ thể theo nghề chính): ", paragraph_normal))
    flow_obj1.append(Paragraph(f"a) Nghề câu: Chiều dài toàn bộ vàng câu: ................m; Số lưỡi câu: ..................................................lưỡi", paragraph_normal))
    flow_obj1.append(Paragraph(f"b) Nghề lưới vây, rê: Chiều dài toàn bộ lưới: ...........m; Chiều cao lưới: ..................................................m", paragraph_normal))
    flow_obj1.append(Paragraph(f"c) Nghề lưới chụp: Chu vi miệng lưới: ...................m; Chiều cao lưới: ..................................................m", paragraph_normal))
    flow_obj1.append(Paragraph(f"d) Nghề lưới kéo: Chiều dài giềng phao: .................m; Chiều dài toàn bộ lưới: ..........................................m", paragraph_normal))
    flow_obj1.append(Paragraph(f"e) Nghề khác:...........................................................", paragraph_normal))

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

    flow_obj2.append(Paragraph(f"Chuyến biển số: {ediary.IDChuyenBien.ChuyenBienSo}...........", paragrap_bold))
    flow_obj2.append(Paragraph(f"{ediary.IDChuyenBien.ChuyenBienSo}/{datetime.now().year}", h2))


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

    flow_obj3.append(Paragraph(f"10. Cảng đi: {ediary.IDChuyenBien.CangXuatBen.Ten}.......; Thời gian đi: Ngày {ediary.IDChuyenBien.NgayXuatBen.day}... tháng {ediary.IDChuyenBien.NgayXuatBen.month}... năm {ediary.IDChuyenBien.NgayXuatBen.year}...",paragraph_normal))
    flow_obj3.append(Paragraph(f"11. Cảng về: {ediary.IDChuyenBien.CangVeBen.Ten}.......; Thời gian cập cảng: Ngày {ediary.IDChuyenBien.NgayVeBen.day}... tháng {ediary.IDChuyenBien.NgayVeBen.month}... năm {ediary.IDChuyenBien.NgayVeBen.year}...",paragraph_normal))
    flow_obj3.append(Paragraph(f"12. Nộp Nhật ký: Ngày ..... tháng ..... năm .......; Vào Sổ số: {ediary.MaNhatKy}",paragraph_normal))

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

    sea_trip = ediary.IDChuyenBien
    net_list = BangMeLuoi.objects.filter(IDChuyenBien=sea_trip).order_by('MeLuoiSo')
    # sum_qty = []
    # if net_list is not None:
    #     for net in net_list:
    #         sum = [0] * 6
    #         fish_list = BangLoaiCaDuocDanhBatTrongMeLuoi.objects.filter(IDMeLuoi=net).order_by('-SanLuong')[:6]
    #         # print(fish_list)
            
    #         if fish_list is not None:
    #             for index, fish in enumerate(fish_list):
    #                 sum[index] = fish.SanLuong
    #         sum_qty.append(sum)
    sum_qty = []
    if net_list is not None:

        # tạo một từ điển để lưu tổng số lượng của từng loài cá
        species_totals = defaultdict(int) # species: giống loài

        # duyệt qua danh sách các mẻ lưới
        for net in net_list:
            species_in_net = BangLoaiCaDuocDanhBatTrongMeLuoi.objects.filter(IDMeLuoi=net)

            for species in species_in_net:
                species_totals[species.IDLoaiCa] += species.SanLuong 
        top_6_species = sorted(species_totals.items(), key=lambda x: x[1], reverse=True)[:6]
        top_6_species_name = [BangLoaiCaDanhBat.objects.get(ID=species_id.ID).Ten for species_id, _ in top_6_species]

        
        for net in net_list:
            net_quantities = []
            species_in_net = BangLoaiCaDuocDanhBatTrongMeLuoi.objects.filter(IDMeLuoi=net)

            for species_id, _ in top_6_species:
                quantity = next((species.SanLuong for species in species_in_net if species.IDLoaiCa == species_id), 0)
                net_quantities.append(quantity)
            
            net_quantities += [0] * (6 - len(net_quantities))

            sum_qty.append(net_quantities)

    # print(sum_qty)
    tmp_list = []
    for i, item in enumerate(net_list):
        date_start = item.ThoiDiemThaNguCu
        date_end = item.ThoiDiemThuNguCu
        # print(item)
        tmp_ = [i+1, f"{date_start.day}-{date_start.month}-{date_start.year}", f"{str(item.ViDoThaNguCu)[0:7]}", f"{str(item.KinhDoThaNguCu)[0:7]}", f"{date_end.day}-{date_end.month}-{date_end.year}", f"{str(item.ViDoThuNguCu)[0:7]}", f"{str(item.KinhDoThuNguCu)[0:7]}", f"{sum_qty[i][0]}", f"{sum_qty[i][1]}", f"{sum_qty[i][2]}", f"{sum_qty[i][3]}", f"{sum_qty[i][4]}", f"{sum_qty[i][5]}", item.TongSanLuong]
        tmp_list.append(tmp_)
    # print(tmp_list)
    top6name = []
    for item in top_6_species_name:
        top6name.append(item.replace(" ", "\n"))
    top6name += [''] * (6 - len(top6name))
    # print(top6name)
    data = [
        ['Mẻ\nthứ', 'Thời \nđiểm bắt\nđầu thả', 'Vị trí thả', '', 'Thời\nđiểm kết\nthúc thu', 'Vị trí thu', '', 'Sản lượng các loài chủ yếu**(kg)', '', '', '', '', '', 'Tổng \nsản\nlượng\n(kg)'],
        ['', '', 'Vĩ độ', 'Kinh độ', '', 'Vĩ độ', 'Kinh độ', f'{top6name[0]}', f'{top6name[1]}', f'{top6name[2]}', f'{top6name[3]}', f'{top6name[4]}', f'{top6name[5]}', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
    ]
    data.extend(tmp_list)

    table = Table(data, colWidths=colWidths)
    tstyle = TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONT", (0, 0), (-1, -1), "Times_New_Roman",13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1,-1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ("SPAN", (0, 0), (0, 6)),  # Row span from row 0 to row 1 for the first column (col - row) (col - row )  (Row span thì col giữ nguyên) # mẻ thứ
        ("SPAN", (1, 0), (1, 6)),   # Row span from row 1 to row 2 for the second column  # thời điểm bắt đầu thả
        ("SPAN", (2, 0), (3, 0)),  # Column span from column 0 to column 2 for the first Row (col span thì row giữ nguyên) # vị trí thả
        ("SPAN", (2, 1), (2, 6)), # vĩ độ thả
        ("SPAN", (3, 1), (3, 6)), # kinh độ thả
        ("SPAN", (4, 0), (4, 6)), # thời điểm kết thúc thu 
        ("SPAN", (5, 0), (6, 0)), # vị trí thu
        ("SPAN", (5, 1), (5, 6)), # vĩ độ thu
        ("SPAN", (6, 1), (6, 6)), # kinh độ thu
        ("SPAN", (7, 0), (12, 0)), # sản lượng các loài
        ("SPAN", (7, 1), (7, 2)), # loài
        ("SPAN", (8, 1), (8, 2)), # loài
        ("SPAN", (9, 1), (9, 2)), # loài
        ("SPAN", (10, 1), (10, 2)), # loài
        ("SPAN", (11, 1), (11, 2)), # loài
        ("SPAN", (12, 1), (12, 2)), # loài
        ("SPAN", (13, 0), (13, 6)), # tổng sản lượng

        ("SPAN", (7, 1), (7, 6)),  # Loài cá có 5 chữ
        ("SPAN", (8, 1), (8, 6)),  # Loài cá có khoảng 6 chữ
        ("SPAN", (9, 1), (9, 6)),  # Loài 3
        ("SPAN", (10, 1), (10, 6)),  # Loài 4
        ("SPAN", (11, 1), (11, 6)),  # Loài 5
        ("SPAN", (12, 1), (12, 6)),  # Loài 6
    ])
    table.setStyle(tstyle)
    flow_obj4.append(table)
    flow_obj4.append(Spacer(1, 0.25*cm))
    flow_obj4.append(Paragraph("**Ghi các đối tượng khai thác chính theo từng nghề (Kéo, Rê, Vây, Câu, Chụp…). Đối với các nghề khai thác cá ngừ cần ghi rõ sản lượng của từng loài như: cá ngừ Vây vàng, cá ngừ Mắt to, cá ngừ Vằn (Sọc dưa), cá ngừ khác (Chù, ồ…).", paragraph_normal))
    
    frame4.addFromList(flow_obj4, pdf)
    pdf.showPage()

    flow_obj6 = []
    frame6 = Frame(
        x1=2.5*cm,
        y1=2.5*cm,
        width=(page_width - 5*cm),
        height=(page_height - 4*cm),
        showBoundary=0
    )

    flow_obj6.append(Paragraph("2.Thông tin về các loài nguy cấp quý hiếm", paragrap_bold))
    flow_obj6.append(Paragraph("Cá voi/Cá heo/Bò biển/Quản đồng/Vích/Đồi mồi dứa/Đồi mồi/Rùa da/Loài khác (Ghi tên cụ thể)", paragraph_normal))

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
    flow_obj6.append(table2)
    flow_obj6.append(Spacer(1, 0.25*cm))
    flow_obj6.append(Paragraph("Thông tin bổ sung về loài (nếu có): (Về màu sắc loài; thiết bị, thẻ gắn số trên cá thể;…và các thông tin khác nếu có)\n\
        ……………………………………………………………………………………………………………………………………………………\
    …………………………..………………………………………………………………………………………………………………………\
    ……………………………………………………………………………………….", style_normal))
    frame6.addFromList(flow_obj6, pdf)
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
        ["TT", "Ngày, tháng", "Thông tin tàu thu\nmua/chuyển tải", "", "Vị trí thu mua,\nchuyển tải", "", "Đã bán/chuyển tải", "", "Thuyền trưởng \ntàu thu mua,\nchuyển tải"],
        ["", "", "Số đăng ký\ntàu", "Số giấy phép\nkhai thác", "Vĩ độ", "Kinh độ", "Tên loài\nthủy sản", "Khối lượng\n(kg)", ""],
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


@login_required(login_url='/login/')
def search_journal_view(request):
    titles = ["STT", "Mã tàu", "Ngày tạo nhật ký", "Chủ tàu", "CMND (CCCD)", "Mã nhật ký", "Ghi chú", "Thao tác"]
    if request.user.user_type == '1' or request.user.is_staff:
        query = request.GET.get('q')
        query_type = request.GET.get('query-type')
        
        # mã tàu
        if query_type == '1':
            ships = BangTau.objects.filter(Q(SoDangKy__icontains=query))
            items = []
            for ship in ships:
                journal_list = ship.bangnhatky_set.all()
                items.extend(journal_list)
            if len(items) == 0:
                messages.info(request, f"Không tìm thấy thông tin nhật ký liên quan đến tàu có số đăng ký query = '{query}'")

        # mã chủ tàu
        if query_type == '2':
            pass 

        # mã thuyền trưởng
        if query_type == '3':
            pass 

        # mã nhật ký 
        if query_type == '4':
            items = BangNhatKy.objects.filter(Q(MaNhatKy__icontains=query))
            if len(items) == 0:
                messages.info(request, f"Không tìm thấy thông tin nhật ký với mã query = '{query}'")

        # mã chuyến biển
        if query_type == '5':
            tmp = BangChuyenBien.objects.filter(Q(ID__icontains=query) | Q(ChuyenBienSo__icontains=query))
            items = []
            for i in tmp:
                journal_list = i.bangnhatky_set.all()
                items.extend(journal_list) 
            print(len(items))
            if len(items) == 0:
                messages.info(request, f"Không tìm thấy thông tin nhật ký liên quan đến chuyển biến với query = '{query}'")  

        return render(request, 'core/journal.html', {
            'titles': titles,
            'items': items,
        }, status=200)

    elif request.user.user_type == '2':
        pass
    else:
        return render(request, '403.html', {}, status=403)
