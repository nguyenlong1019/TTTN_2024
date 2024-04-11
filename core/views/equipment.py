from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.db.models import Q 
from django.contrib import messages

from core.models import * 


def check_serial_number_valid(serial_number):
    '''Kiểm tra mã thiết bị nhật ký đã có hay chưa?'''
    equips = BangThietBiNhatKyKhaiThac.objects.filter(SerialNumber=serial_number)
    if equips.exists():
        return False 
    return True # trả về False nếu đã tồn tại, ngược lại trả về True


@login_required(login_url='/login/')
def add_new_equipment_view(request):
    if request.user.user_type == '3':
        if request.method == 'POST':
            SerialNumber = request.POST.get('serialNumber')
            NgaySanXuat = request.POST.get('ngaySanXuat')
            FWVersion = request.POST.get('FWVersion')

            if not check_serial_number_valid(SerialNumber):
                messages.info(request, "Serial Number của thiết bị đã tồn tại!")
                return redirect('add-equipment')

            equipment = BangThietBiNhatKyKhaiThac.objects.create(
                SerialNumber=SerialNumber,
                NgaySanXuat=NgaySanXuat,
                FWVersion=FWVersion
            )

            messages.info(request, "Tạo thiết bị nhật ký khai thác thành công!!!")
            return redirect('index')
        else:
            return render(request, 'core/add-equipment.html', {}, status=200)
    else:
        return render(request, '403.html', {}, status=403)


@login_required(login_url='/login/')
def edit_equipment_view(request, pk):
    if request.user.user_type == '3':
        if request.method == 'POST':
            SerialNumber = request.POST.get('serialNumber')
            NgaySanXuat = request.POST.get('ngaySanXuat')
            FWVersion = request.POST.get('FWVersion')

            try:
                equipment = BangThietBiNhatKyKhaiThac.objects.get(pk=pk)
            except BangThietBiNhatKyKhaiThac.DoesNotExist:
                messages.error(request, f"Không tìm thấy thiết bị với ID = '{pk}'")
                return redirect('index')

            if SerialNumber != '' and SerialNumber != equipment.SerialNumber:
                if check_serial_number_valid(SerialNumber):
                    equipment.SerialNumber = SerialNumber
                else:
                    messages.info(request, "Số Serial Number đã tồn tại!!!")
                    return redirect('edit-equipment', pk)
            
            equipment.NgaySanXuat = NgaySanXuat 
            equipment.FWVersion = FWVersion 
            equipment.save()

            messages.info(request, f"Cập nhật thông tin thiết bị thành công!")
            return redirect('index')
        else:
            try:
                equipment = BangThietBiNhatKyKhaiThac.objects.get(pk=pk)
            except BangThietBiNhatKyKhaiThac.DoesNotExist:
                messages.error(request, f"Không tìm thấy thiết bị với ID = '{pk}'")
                return redirect('index')
            return render(request, 'core/edit-equipment.html', {'equipment': equipment}, status=200)
    else:
        return render(request, '403.html', {}, status=403)


@login_required(login_url='/login/')
def delete_equipment_view(request, pk):
    if request.user.user_type == '3':
        try:
            equipment = BangThietBiNhatKyKhaiThac.objects.get(pk=pk)
        except BangThietBiNhatKyKhaiThac.DoesNotExist:
            messages.error(request, f"Không tìm thấy thiết bị với ID = '{pk}'")
            return redirect('index')
        ship = BangTau.objects.filter(IDDevice=equipment)
        # print(ship)
        if ship.exists():
            for ship in ships:
                ship.IDDevice = None 
                ship.save()
                print("OKe")

        equipment.delete()
        messages.info(request, f"Xóa thiết bị với ID = {pk} thành công!!")
        return redirect('index')
    else:
        return render(request, '403.html', {}, status=403)


@login_required(login_url='/login/')
def search_equipment_view(request):
    if request.user.user_type == '3':
        query = request.GET.get('q')
        query_type = request.GET.get('query-type')
        titles = ["STT", "Serial Number", "Ngày sản xuất", "Version", "Mã tàu", "Trạng thái", "Thao tác"]

        # mã thiết bị
        if query_type == '1':
            equipments = BangThietBiNhatKyKhaiThac.objects.filter(Q(IDThietBi__icontains=query)) 
            if len(list(equipments)) == 0:
                messages.info(request, f"Không tìm thấy thông tin thiết bị liên quan đến Mã thiết bị với query='{query}'")
        
        # serial number 
        elif query_type == '2':
            equipments = BangThietBiNhatKyKhaiThac.objects.filter(Q(SerialNumber__icontains=query))
            if len(list(equipments)) == 0:
                messages.info(request, f"Không tìm thấy thông tin thiết bị liên quan đến Serial Number với query='{query}'")
            
        # mã tàu
        # elif query_type == '3':
        #     ships = BangTau.objects.filter(Q(SoDangKy__icontains=query))
        #     equipments = []
        #     for ship in ships:
        #         # print(ship.IDDevice)
        #         item = BangThietBiNhatKyKhaiThac.objects.filter(pk=ship.IDDevice.ID)
        #         equipments.append(item)
        #     if len(list(equipments)) == 0:
        #         messages.info(request, f"Không tìm thấy thông tin thiết bị liên quan đến mã tàu với query='{query}'")

        else:
            equipments = BangThietBiNhatKyKhaiThac.objects.all().order_by('SerialNumber')
        
        # print(equipments)
        return render(request, 'core/index.html', {
            'titles': titles,
            'items': equipments
        }, status=200)
    else:
        return render(request, '403.html', {}, status=403)
