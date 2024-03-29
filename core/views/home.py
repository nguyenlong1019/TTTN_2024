from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required

from core.models import * 

from django.db.models import Q 
import json 
from django.http import HttpResponse, JsonResponse


@login_required(login_url='/login/')
def index(request):
    '''Quản lý hải trình: Trang theo dõi vị trí tàu theo thời gian thực'''
    if request.user.user_type == '3':
        titles = ["STT", "Serial Number", "Ngày sản xuất", "Version", "Mã tàu", "Trạng thái", "Thao tác"]
        equipments = BangThietBiNhatKyKhaiThac.objects.all().order_by('-ID')
        return render(request, 'core/index.html', {
            'titles': titles,
            'items': equipments
        }, status=200)

    if request.user.user_type == '1' or request.user.is_staff:
        # Filter theo tàu nào đã có vị trí, tàu nào chưa có vị trí để tránh lỗi
        ships = []
        ships_with_position = BangTau.objects.prefetch_related('bangvitritau_set')
        ship_counter = 0
        for ship in ships_with_position:
            if ship.bangvitritau_set.exists():
                ships.append(ship)
                ship_counter += 1
        
        return render(request, 'core/index.html', {
            'ships': ships,
            'ship_counter': ship_counter,
        }, status=200)
    
    if request.user.user_type == '2':
        ships = []
        ships_with_position = BangTau.objects.filter(CangCaDangKy=request.user.staff.cangca).prefetch_related('bangvitritau_set')
        ship_counter = 0

        for ship in ships_with_position:
            if ship.bangvitritau_set.exists():
                ships.append(ship)
                ship_counter += 1

        return render(request, 'core/index.html', {
            'ships': ships,
            'ship_counter': ship_counter
        }, status=200) 

    return render(request, '403.html', {}, status=403)


@login_required(login_url='/login/')
def marine_diary_view(request):
    """
    Lịch sử hải trình
    """
    query = request.GET.get('q')
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    if request.user.user_type == '1' or request.user.is_staff:
        try:
            ships = BangTau.objects.filter(Q(SoDangKy__icontains=query))
            if ships.exists():
                ship = BangTau.objects.filter(Q(SoDangKy__icontains=query)).first()
                if not ship.bangvitritau_set.exists():
                    messages.info(request, f"Thông tin tàu {ship.SoDangKy} chưa được cập nhật vị trí")
                    return redirect('index')
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
    elif request.user.user_type == '2':
        try:
            ships = BangTau.objects.filter(Q(SoDangKy__icontains=query) & Q(CangCaDangKy=request.user.staff.cangca))
            if ships.exists():
                ship = BangTau.objects.filter(Q(SoDangKy__icontains=query) & Q(CangCaDangKy=request.user.staff.cangca)).first()
                if not ship.bangvitritau_set.exists():
                    messages.info(request, f"Thông tin tàu {ship.SoDangKy} chưa được cập nhật vị trí")
                    return redirect('index')
            else:
                messages.info(request, f"Không tìm thấy tàu với query = '{query}' tại cảng cá {request.user.staff.cangca.Ten}") 
                return redirect('index')        
        except ValueError:
            messages.info(request, f"Số đăng ký tàu không được phép trống hoặc None!!")
            return redirect('index')

        return render(request, 'core/index-search.html', {
            'ship': ship,
            'start_date': start_date,
            'end_date': end_date
        }, status=200) 
    else:
        return render(request, '403.html', {}, status=403)


# lấy lịch sử vị trí tàu 
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
    

# Lấy info của tất cả các tàu và hiển thị trên map 
@login_required(login_url='/login/')
def get_all_location_api(request):
    # ships = BangTau.objects.all()

    # Lấy danh sách tàu đã có vị trí
    ships = []
    if request.user.user_type == '1' or request.user.is_staff:
        ships_with_position = BangTau.objects.prefetch_related('bangvitritau_set')
    elif request.user.user_type == '2':
        ships_with_position = BangTau.objects.filter(CangCaDangKy=request.user.staff.cangca).prefetch_related('bangvitritau_set')
    else:
        return render(request, '403.html', {}, status=403)

    for ship in ships_with_position:
        if ship.bangvitritau_set.exists():
            ships.append(ship)

    info = []
    for i in ships:
        new_loc = i.bangvitritau_set.order_by('-Ngay').first()
        print(new_loc.Ngay)
        ship_info = {
            'SoDangKy': i.SoDangKy,
            'ChuTau': i.IDChuTau.HoTen,
            'ThuyenTruong': i.IDThuyenTruong.HoTen,
            'ViDo': new_loc.ViDo,
            'KinhDo': new_loc.KinhDo,
            'NgayCapNhat': f"{new_loc.Ngay.hour}:{new_loc.Ngay.minute}:{new_loc.Ngay.second} Ngày {new_loc.Ngay.day} tháng {new_loc.Ngay.month} năm {new_loc.Ngay.year}",
        }
        # print(ship_info['NgayCapNhat'])
        info.append(ship_info)
    return JsonResponse({
        'status': 200,
        'message': 'Cập nhật thông tin vị trí các tàu thành công!',
        'info': info,
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
        
        bundles = []
        for item in fish_totals:
            data = {
                'fish_name': item['IDLoaiCa__Ten'],
                'qty': item['tong_san_luong']
            }
            bundles.append(data)
        
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
