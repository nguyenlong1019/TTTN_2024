from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 


# Báo cáo thống kê
@login_required(login_url='/login/')
def report_view(request):
    fishing_port = BangCangCa.objects.all()
    titles = ["STT", "Tên Loài Cá", "Sản Lượng"]

    # Lấy thời điểm 24h trước 
    time_threshold = timezone.now() - timedelta(hours=24)

    # Lấy danh sách các mẻ lưới có thời gian thu ngư cụ trong khoảng 24h
    if request.user.user_type == '1' or request.user.is_staff:
        bang_me_luoi_24h = BangMeLuoi.objects.filter(ThoiDiemThuNguCu__lte=time_threshold)
    elif request.user.user_type == '2':
        bang_me_luoi_24h = BangMeLuoi.objects.filter(ThoiDiemThuNguCu__lte=time_threshold)
    else:
        return render(request, '403.html', {}, status=403)
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
def search_report_view(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    
    fishing_port = BangCangCa.objects.all()
    titles = ["STT", "Tên Loài Cá", "Sản Lượng"]

    try:
        gate = BangCangCa.objects.get(pk=query)
    except BangCangCa.DoesNotExist:
        messages.info(request, f"Không tìm thấy thông tin cảng cá với query = '{query}'")
        return redirect('report-view')

    # print(gate)

    # ngày về bến nằm trong khoảng start date và end date
    sea_trip_list = BangChuyenBien.objects.filter(Q(NgayVeBen__gte=start_date) & Q(NgayVeBen__lte=end_date) & Q(CangVeBen=gate))
    if len(sea_trip_list) == 0:
        messages.info(request, f"Không tìm thấy chuyến biển về cảng {gate.Ten} trong khoảng thời gian từ {start_date} đến {end_date}")
        return redirect('report-view')
    fish_totals = []

    for sea_trip in sea_trip_list:
        net_list = sea_trip.bangmeluoi_set.all()

        for net in net_list:
            fish_list = net.bangloaicaduocdanhbattrongmeluoi_set.values('IDLoaiCa__Ten').annotate(tong_san_luong=Sum('SanLuong'))

            fish_totals += fish_list
    fish_totals.sort(key=lambda x: x['tong_san_luong'], reverse=True)
    # print(fish_totals)
    return render(request, 'core/report-search.html', {
        'fishing_port': fishing_port,
        'titles': titles,
        'items': fish_totals,
        'selected_port': gate,
        'start_date': start_date,
        'end_date': end_date
    }, status=200) 