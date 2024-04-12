from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse

from core.models import * 

from django.utils import timezone 
from datetime import timedelta 
from django.db.models import Sum, Q 
from django.contrib import messages 
from django.core.paginator import Paginator
import json


# Báo cáo thống kê
@login_required(login_url='/login/')
def report_view(request):
    fishing_port = BangCangCa.objects.all().order_by('Ten')
    titles = ["STT", "Tên Loài Cá", "Sản Lượng"]

    # Lấy thời điểm 24h trước 
    time_threshold = timezone.now() - timedelta(hours=24)
    # print(time_threshold)

    # Lấy danh sách các mẻ lưới có thời gian thu ngư cụ trong khoảng 24h
    if request.user.user_type == '1' or request.user.is_staff:
        # tất cả mẻ lưới trong 24h qua
        bang_me_luoi_24h = BangMeLuoi.objects.filter(ThoiDiemThuNguCu__gte=time_threshold)
    elif request.user.user_type == '2':
        # tất cả mẻ lưới trong 24h qua của các tàu đánh bắt
        bang_me_luoi_24h = BangMeLuoi.objects.filter(ThoiDiemThuNguCu__gte=time_threshold)
    else:
        return render(request, '403.html', {}, status=403)
    # print(bang_me_luoi_24h)
    # Tính tổng sản lượng của mỗi loại cá được đánh bắt trong 24h
    items = (
        BangLoaiCaDuocDanhBatTrongMeLuoi.objects
        .filter(IDMeLuoi__in=bang_me_luoi_24h)
        .values('IDLoaiCa__Ten')
        .annotate(tong_san_luong=Sum('SanLuong'))  # annotate: thêm cột mới vào kết quả truy vấn
        .order_by('-tong_san_luong').all()
    )
    # print(dir(items[0]))
    # print(items.query.field_names) # dùng trên object
    # print(items)
    # print(items[0].keys())

    total_ship = BangTau.objects.all().count()
    total_ship_active = BangTau.objects.filter(is_anchor=False).count()
    total_ship_anchor = BangTau.objects.filter(is_anchor=True).count()
    total_qty = 0
    if bang_me_luoi_24h.exists():
        for net in bang_me_luoi_24h:
            total_qty += net.TongSanLuong 

    items_per_page = 9
    p = Paginator(items, items_per_page)
    page = request.GET.get('page')
    items = p.get_page(page)
    current = items.number
    start = max(current - 2, 1)
    end = min(current + 2, items.paginator.num_pages)
    page_range = range(start, end)
    start_number = (current - 1) * items_per_page

    return render(request, 'core/report.html', {
        'fishing_port': fishing_port,
        'titles': titles,
        'items': items,
        'total_ship': total_ship,
        'total_ship_active': total_ship_active,
        'total_ship_anchor': total_ship_anchor,
        'total_qty': total_qty,
        'start': start, 
        'end': end, 
        'page_range': page_range,
        'start_number': start_number
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

    nets = BangMeLuoi.objects.filter(IDChuyenBien__in=sea_trip_list)
    if nets.exists():
        items = (
            BangLoaiCaDuocDanhBatTrongMeLuoi.objects
            .filter(IDMeLuoi__in=nets)
            .values('IDLoaiCa__Ten')
            .annotate(tong_san_luong=Sum('SanLuong'))  # annotate: thêm cột mới vào kết quả truy vấn
            .order_by('-tong_san_luong').all()
        )

    items_per_page = 9
    p = Paginator(items, items_per_page)
    page = request.GET.get('page')
    items = p.get_page(page)
    current = items.number
    start = max(current - 2, 1)
    end = min(current + 2, items.paginator.num_pages)
    page_range = range(start, end)
    start_number = (current - 1) * items_per_page
    return render(request, 'core/report-search.html', {
        'fishing_port': fishing_port,
        'titles': titles,
        'items': items,
        'selected_port': gate,
        'start_date': start_date,
        'end_date': end_date,
        'start': start, 
        'end': end, 
        'page_range': page_range,
        'start_number': start_number

    }, status=200) 


@login_required(login_url='/login/')
def search_top_10_fishing_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        query = data['query']
        start_date = data['start_date']
        end_date = data['end_date']

        try:
            gate = BangCangCa.objects.get(pk=query)
        except BangCangCa.DoesNotExist:
            messages.info(request, f"Không tìm thấy thông tin cảng cá với query = '{query}'")
            return redirect('report-view')
        print(gate)
        # ngày về bến nằm trong khoảng start date và end date
        sea_trip_list = BangChuyenBien.objects.filter(Q(NgayVeBen__gte=start_date) & Q(NgayVeBen__lte=end_date) & Q(CangVeBen=gate))
        if len(sea_trip_list) == 0:
            messages.info(request, f"Không tìm thấy chuyến biển về cảng {gate.Ten} trong khoảng thời gian từ {start_date} đến {end_date}")
            return redirect('report-view')
        print(sea_trip_list)
        nets = BangMeLuoi.objects.filter(IDChuyenBien__in=sea_trip_list)
        print(nets)
        bundles = []
        if nets.exists():
            top_loai_ca = (
                BangLoaiCaDuocDanhBatTrongMeLuoi.objects
                .filter(IDMeLuoi__in=nets)
                .values('IDLoaiCa__Ten')
                .annotate(tong_san_luong=Sum('SanLuong'))
                .order_by('-tong_san_luong')[:10]
            )
            # print(top_loai_ca)
            for item in top_loai_ca:
                data = {
                    'fish_name': item['IDLoaiCa__Ten'],
                    'qty': item['tong_san_luong']
                }
                bundles.append(data)
        # fish_totals = []

        # for sea_trip in sea_trip_list:
        #     net_list = sea_trip.bangmeluoi_set.all()

        #     for net in net_list:
        #         fish_list = net.bangloaicaduocdanhbattrongmeluoi_set.values('IDLoaiCa__Ten').annotate(tong_san_luong=Sum('SanLuong'))

        #         fish_totals += fish_list
        # fish_totals.sort(key=lambda x: x['tong_san_luong'], reverse=True)
        
        # bundles = []
        # for item in fish_totals:
        #     data = {
        #         'fish_name': item['IDLoaiCa__Ten'],
        #         'qty': item['tong_san_luong']
        #     }
        #     bundles.append(data)
        
        return JsonResponse({
            'message': f'Top 10 loại cá được đánh bắt nhiều nhất trong khoảng thời gian từ {start_date} đến {end_date} ',
            'status': 200,
            'bundles': bundles[:10],
            'start_date': start_date,
            'end_date': end_date
        }, status=200)

    else:
        return JsonResponse({
            'message': 'method not allowed',
            'success': False,
        }, status=405)


# Lấy 10 loại cá được đánh bắt nhiều nhất phục vụ cho biểu đồ
@login_required(login_url='/login/')
def top_10_fishing_api(request):
    # Lấy thời điểm 24h trước 
    time_threshold = timezone.now() - timedelta(hours=24)

    # Lấy danh sách các mẻ lưới có thời gian thu ngư cụ trong khoảng 24h
    bang_me_luoi_24h = BangMeLuoi.objects.filter(ThoiDiemThuNguCu__gte=time_threshold)
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

