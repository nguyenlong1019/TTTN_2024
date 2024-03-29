from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 

from core.models import * 

from django.db.models import Q 
import random, json, operator
from django.contrib import messages
from django.http import JsonResponse


# quản lý thông tin chủ tàu, thuyền trưởng
@login_required(login_url='/login/')
def shipowners_view(request):
    if request.user.user_type == '1' or request.user.is_staff:
        titles = ["STT", "Họ tên", "Số CMND(CCCD)", "Địa chỉ", "Trạm bờ", "Email", "Số điện thoại", "Người dùng", "Thao tác"]
        captains = list(BangThuyenTruong.objects.all().order_by('HoTen'))
        shipowners = list(BangChuTau.objects.all().order_by('HoTen'))

        for captain in captains:
            captain.type = 'captain'
        for shipowner in shipowners:
            shipowner.type = 'shipowner'    
        
        combined_list = captains + shipowners
        # random.shuffle(combined_list)
        return render(request, 'core/shipowners.html', {
            'titles': titles,
            'items': combined_list,
        }, status=200)
    elif request.user.user_type == '2':
        titles = ["STT", "Họ tên", "Số CMND(CCCD)", "Địa chỉ", "Trạm bờ", "Email", "Số điện thoại", "Người dùng", "Thao tác"]
        captains = []
        shipowners = []
        ships = BangTau.objects.filter(CangCaDangKy=request.user.staff.cangca)
        if ships is not None:
            for ship in ships:
                if ship.IDChuTau:
                    shipowners.append(ship.IDChuTau)
                if ship.IDThuyenTruong:
                    captains.append(ship.IDThuyenTruong)
        for captain in captains:
            captain.type = 'captain'
        for shipowner in shipowners:
            shipowner.type = 'shipowner' 
        
        combined_list = list(set(captains)) + list(set(shipowners))
        combined_list = sorted(combined_list, key=operator.attrgetter('HoTen'))
        return render(request, 'core/shipowners.html', {
            'titles': titles,
            'items': combined_list,
        }, status=200)
    else:
        return render(request, '403.html', {}, status=403) 


# tìm kiếm thông tin chủ tàu, thuyền trưởng
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


# thêm chủ tàu, thuyền trưởng
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


# sửa thông tin chủ tàu, thuyền trưởng
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


# xóa thông tin tàu hoặc thuyền trưởng
@login_required(login_url='/login/')
def delete_shipowners_view(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        # print(data)
        if data['userType'] == 'captain':
            try:
                captain = BangThuyenTruong.objects.get(pk=pk)
            except BangThuyenTruong.DoesNotExist:
                return JsonResponse({
                    'message': f"Không tìm thấy thông tin thuyền trưởng với id = '{pk}'",
                    'success': False
                }, status=404)
            ship = BangTau.objects.filter(IDThuyenTruong=captain)
            if ship.exists():
                return JsonResponse({
                    'message': 'Không được phép xóa thuyền trưởng khi chưa xóa tàu liên kết!!!',
                    'success': False
                })
            else:
                captain.delete()
                return JsonResponse({
                    'message': "Xóa thông tin thuyền trưởng thành công!!!",
                    'success': True
                })
        elif data['userType'] == 'shipowner':
            try:
                shipowner = BangChuTau.objects.get(pk=pk)
            except BangChuTau.DoesNotExist:
                return JsonResponse({
                    'message': f"Không tìm thấy thông tin chủ tàu với id = '{pk}'",
                    'success': False
                }, status=404)

            ship = BangTau.objects.filter(IDChuTau=shipowner)
            if ship.exists():
                return JsonResponse({
                    'message': 'Không được phép xóa chủ tàu khi chưa xóa tàu liên kết!!!',
                    'success': False
                })
            else:
                shipowner.delete()
                return JsonResponse({
                    'message': "Xóa thông tin chủ tàu thành công!!!",
                    'success': True
                })
        else:
            return JsonResponse({
                'message': 'User Type không hợp lệ',
                'success': False
            })
    else:
        return JsonResponse({
            'message': 'Method not allowed!!',
            'success': False
        }, status=405)
