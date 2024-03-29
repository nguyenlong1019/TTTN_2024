from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 

from core.models import * 


@login_required(login_url='/login/')
def add_new_equipment_view(request):
    if request.user.user_type == '3':
        if request.method == 'POST':
            SerialNumber = request.POST.get('serialNumber')
            NgaySanXuat = request.POST.get('ngaySanXuat')
            FWVersion = request.POST.get('FWVersion')

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
            
            equipment.SerialNumber = SerialNumber
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
        equipment.delete()
        messages.info(request, f"Xóa thiết bị với ID = {pk} thành công!!")
        return redirect('index')
    else:
        return render(request, '403.html', {}, status=403)


# @login_required(login_url='/login/')
# def check_valid_equipment_api(request):
#     if request.user.user_type == '3':
#         if request.method == 'POST':
#             data = json.load(request.body)
#             serial_number = data['SerialNumber']
#             equipment = BangThietBiNhatKyKhaiThac.objects.filter(SerialNumber=serial_number)
#             if equipment is not None:
#                 return JsonResponse({
#                     'message': 'Serial Number already exist!!!',
#                     'success': False
#                 }) 
#             else:
#                 return JsonResponse({
#                     'message': 'Validate form successfully!!!',
#                     'success': True
#                 })
#         else:
#             return JsonResponse({
#                 'message': 'Method not allowed',
#                 'success': False
#             }, status=405)
#     else:
#         return JsonResponse({
#             'message': "Error: User permission",
#             'success': False,
#         }, status=403)


@login_required(login_url='/login/')
def search_equipment_view(request):
    if request.user.user_type == '3':
        query = request.GET.get('q')
        query_type = request.GET.get('query-type')
        titles = ["STT", "Serial Number", "Ngày sản xuất", "Version", "Mã tàu", "Trạng thái", "Thao tác"]
        equipments = BangThietBiNhatKyKhaiThac.objects.all()

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
        
        # print(equipments)
        return render(request, 'core/index.html', {
            'titles': titles,
            'items': equipments
        }, status=200)
    else:
        return render(request, '403.html', {}, status=403)
