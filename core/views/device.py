from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 


# quản lý tàu cá 
@login_required(login_url='/login/')
def device_view(request):
    '''Quản lý tàu cá'''
    titles = ["STT","IMO","Số hiệu tàu","Chủ tàu","Loại tàu","Nơi đăng ký","Thuyền trưởng","Cảng cá ĐK","TBNKKT","Thao tác"]
    
    if request.user.user_type == '1' or request.user.is_staff:
        items = BangTau.objects.all().order_by('SoDangKy')
    elif request.user.user_type == '2':
        items = BangTau.objects.filter(Q(CangCaDangKy=request.user.staff.cangca)).order_by('SoDangKy')
    else:
        return render(request, '403.html', {}, status=403)

    return render(request, 'core/device.html', {
        'titles': titles,
        'items': items, 
    }, status=200)


# thêm thông tin tàu cá mới
@login_required(login_url='/login/')
def add_new_device_view(request):
    '''Thêm tàu cá mới'''
    if request.user.user_type == '1' or request.user.is_staff:
        if request.method == 'POST':
            # print(request.POST)

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
        shipowners = BangChuTau.objects.all().order_by('HoTen')
        ship_type_list = BangMaLoaiTau.objects.all()
        gate_list = BangCangCa.objects.all().order_by('Ten')
        job_list = BangNganhNgheKhaiThac.objects.all()
        device_list = BangThietBiNhatKyKhaiThac.objects.all().order_by('SerialNumber').exclude(is_active=True) # danh sách thiết bị chưa kích hoạt
        captain_list = BangThuyenTruong.objects.all().order_by('HoTen').exclude(hasShip=True) # danh sách các thuyền trưởng chưa có tàu nào
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
    elif request.user.user_type == '2':
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
        shipowners = BangChuTau.objects.all().order_by('HoTen')
        ship_type_list = BangMaLoaiTau.objects.all()
        gate_list = BangCangCa.objects.all().order_by('Ten')
        job_list = BangNganhNgheKhaiThac.objects.all()
        device_list = BangThietBiNhatKyKhaiThac.objects.all().order_by('SerialNumber').exclude(is_active=True) # danh sách thiết bị chưa kích hoạt
        captain_list = BangThuyenTruong.objects.all().order_by('HoTen').exclude(hasShip=True) # danh sách các thuyền trưởng chưa có tàu nào
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
    else:
        return render(request, '403.html', {}, status=403)


# sửa thông tin tàu cá
@login_required(login_url='/login/')
def edit_device_view(request, pk):
    if request.user.user_type == '2' or request.user.user_type == '1' or request.user.is_staff:
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
        
        shipowners = BangChuTau.objects.all().order_by('HoTen')
        ship_type_list = BangMaLoaiTau.objects.all()
        city_list = BangDonViHanhChinhCapTinh.objects.all()
        gate_list = BangCangCa.objects.all().order_by('Ten')
        job_list = BangNganhNgheKhaiThac.objects.all()
        device_list = BangThietBiNhatKyKhaiThac.objects.all().order_by('SerialNumber').exclude(is_active=True)
        captain_list = BangThuyenTruong.objects.all().order_by('HoTen').exclude(hasShip=True)

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
    else:
        return render(request, '403.html', {}, status=403) 

# xóa thông tin tàu cá
@login_required(login_url='/login/')
def delete_device_view(request, pk):
    if request.user.user_type == '1' or request.user.is_staff or request.user.user_type == '2':
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
    else:
        return render(request, '403.html', {}, status=403) 


# Tìm kiếm thông tin tàu cá
@login_required(login_url='/login/')
def search_device_view(request):
    query = request.GET.get('q')
    query_type = request.GET.get('query-type')
    titles = ["STT","IMO","Số hiệu tàu","Chủ tàu","Loại tàu","Nơi đăng ký","Thuyền trưởng","Cảng cá ĐK","TBNKKT","Thao tác"]
    if request.user.user_type == '1' or request.user.is_staff:
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
    elif request.user.user_type == '2':
        items = BangTau.objects.filter(Q(CangCaDangKy=request.user.staff.cangca)).order_by('-ID')

        if query_type == '1':
            items = BangTau.objects.filter(Q(IMO__icontains=query) & Q(CangCaDangKy=request.user.staff.cangca)).order_by('-ID')
            if len(items) == 0:
                messages.info(request, f'Không tìm thấy IMO hợp lệ!')
        elif query_type == '2':
            items = BangTau.objects.filter(Q(SoDangKy__icontains=query) & Q(CangCaDangKy=request.user.staff.cangca)).order_by('-ID') 
            if len(items) == 0:
                messages.info(request, f'Không tìm thấy số đăng ký tàu hợp lệ!')
        elif query_type == '3':
            users = BangChuTau.objects.filter(Q(HoTen__icontains=query)).order_by('-ID')
            # print(users)
            items = []
            for user in users:
                item = user.bangtau_chutau
                for i in item:
                    if i.CangCaDangKy.ID == request.user.staff.cangca.ID:
                        items.append(item)
            # print(items) 
            if len(items) == 0:
                messages.info(request, f'Không tìm thấy chủ tàu hợp lệ!')
        elif query_type == '4':
            users = BangThuyenTruong.objects.filter(Q(HoTen__icontains=query)).order_by('-ID').exclude(hasShip=False)
            items = []
            for user in users:
                print(user)
                item = user.bangtau
                if item.CangCaDangKy.ID == request.user.staff.cangca.ID:
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
                if item.CangCaDangKy.ID == request.user.staff.cangca.ID:
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
    else:
        return render(request, '403.html', {}, status=403)
    

# download device data
@login_required(login_url='/login/')
def download_device_data(request, number):
    if request.user.user_type == '1' or request.user.is_staff:
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
            if ship is not None:
                ws[f"A{i}"] = i - 1
                ws[f"B{i}"] = ship.IMO
                ws[f"C{i}"] = ship.SoDangKy
                ws[f"D{i}"] = ship.IDChuTau.HoTen
                ws[f"E{i}"] = ship.LoaiTau.IDLoaiTau
                ws[f"F{i}"] = ship.NoiDangKy.TenTiengViet
                ws[f"G{i}"] = ship.IDThuyenTruong.HoTen
                ws[f"H{i}"] = ship.CangCaDangKy.Ten
                ws[f"I{i}"] = ship.IDDevice.SerialNumber
            else:
                ws[f"A{i}"] = ''
                ws[f"B{i}"] = ''
                ws[f"C{i}"] = ''
                ws[f"D{i}"] = ''
                ws[f"E{i}"] = ''
                ws[f"F{i}"] = ''
                ws[f"G{i}"] = ''
                ws[f"H{i}"] = ''
                ws[f"I{i}"] = ''

        _, filepath = tempfile.mkstemp(suffix='.xlsx')
        wb.save(filepath)

        with open(filepath, 'rb') as f:
            excel_data = f.read()
        
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="example.xlsx"'
        return response
    elif request.user.user_type == '2':
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
            ship_list = BangTau.objects.filter(Q(CangCaDangKy=request.user.staff.cangca))[:qty]
        else:
            ship_list = BangTau.objects.filter(Q(CangCaDangKy=request.user.staff.cangca))

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
            ws[f"C{i}"] = "********"
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
    else:
        return render(request, '403.html', {}, status=403)
