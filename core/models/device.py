from django.db import models  
from .equipment import * 
from .shipowners import * 


class BangDonViHanhChinhCapTinh(models.Model):
    '''Đơn vị hành chính cấp tỉnh'''
    MaTinh = models.IntegerField(
        primary_key=True,
        default=1,
    )
    TenTiengViet = models.CharField(max_length=50, null=True, blank=True)
    TenVietTat = models.CharField(max_length=6, null=True, blank=True, unique=False)
    TenTiengAnh = models.CharField(max_length=50, null=True, blank=True)
    Cap = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bảng đơn vị hành chính cấp tỉnh"

    def __str__(self):
        return f"{self.MaTinh}-{self.TenTiengViet}"


class BangDonViHanhChinhCapHuyen(models.Model):
    '''Đơn vị hành chính cấp huyện'''
    MaHuyen = models.IntegerField(
        primary_key=True,
        default=1
    )
    TenHuyen = models.CharField(max_length=50, null=True, blank=True)
    TenHuyenEn = models.CharField(max_length=50, null=True, blank=True)
    Cap = models.CharField(max_length=50, null=True, blank=True)
    MaTinh = models.ForeignKey(
        BangDonViHanhChinhCapTinh,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )

    class Meta:
        verbose_name_plural = "Bảng đơn vị hành chính cấp huyện"

    def __str__(self):
        return f"{self.MaHuyen}-{self.TenHuyen}"


class BangMaLoaiTau(models.Model):
    '''Mã loại tàu'''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDLoaiTau = models.CharField(max_length=8, null=False, default='', unique=True)
    TenLoaiTau = models.CharField(max_length=255, null=False, default='')

    class Meta:
        verbose_name_plural = "Bảng mã loại tàu"

    def __str__(self):
        return f"{self.IDLoaiTau}-{self.TenLoaiTau}"


class BangCangCa(models.Model):
    '''
    Đối tượng cảng cá

    ID
    IDCangCa: string (độ dài là 2-3), bắt buộc: mã định danh của cảng cá theo quy định
    Ten: string (độ dài 1-128), bắt buộc: tên cảng cá
    DiaChi: string (1-500), bắt buộc: địa chỉ cảng cá
    DienThoai: string (0-20), không bắt buộc, điện thoại cảng cá
    Fax: string (0-20), không bắt buộc, Fax cảng cá
    Email: string (1-128), không bắt buộc, Email cảng cá
    ViDo: float, bắt buộc, vĩ độ cảng cá, làm tròn 4 chữ số phần thập phân
    KinhDo: float, bắt buộc, kinh độ cảng cá, làm tròn 4 chữ số phần thập phân
    TenCangTruong: string (0-128), không bắt buộc, tên cảng trưởng
    DienThoaiCangTruong: string (0-20), không bắt buộc, điện thoại cảng trưởng

    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDCangCa = models.CharField(
        max_length=6, null=False, unique=True, default='',
        help_text='Mã định danh của cảng cá theo quy định'
    )
    Ten = models.CharField(max_length=128, 
        null=False, default='', help_text='Tên cảng cá')
    DiaChi = models.CharField(max_length=255, 
        null=False, default='', help_text='Địa chỉ cảng cá')
    DienThoai = models.CharField(max_length=20, 
        null=True, blank=True, help_text='Điện thoại cảng cá')
    ViDo = models.DecimalField(null=False, decimal_places=4, 
        default=0, help_text='Vĩ độ cảng cá', max_digits=8)
    KinhDo = models.DecimalField(null=False, decimal_places=4, 
        default=0, help_text='Kinh độ cảng cá', max_digits=8)
    
    Fax = models.CharField(max_length=20, 
        null=True, blank=True, help_text='Fax cảng cá')
    Email = models.CharField(max_length=128, 
        null=True, blank=True, help_text='Email cảng cá')
    
    # Cảng trưởng nên thêm model vào User ()
    TenCangTruong = models.CharField(max_length=128, 
        null=True, blank=True, help_text='Tên cảng trưởng')
    DienThoaiCangTruong = models.CharField(max_length=20, 
        null=True, blank=True, help_text='Điện thoại cảng trưởng')

    IDTinh = models.ForeignKey(
        BangDonViHanhChinhCapTinh,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )

    class Meta:
        verbose_name_plural = "Bảng cảng cá"

    def __str__(self):
        return f"{self.IDTinh.MaTinh}-{self.Ten}"


class BangNganhNgheKhaiThac(models.Model):
    '''
    Đối tượng ngành nghề khai thác

    ID: 
    IDNganhNghe: string (1-5), bắt buộc, Mã định danh của nghề theo quy định
    Ten: string (1-128), bắt buộc: Tên nghề
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDNganhNghe = models.CharField(
        max_length=5, null=False, unique=True, default='',
        help_text='Mã định danh của nghề theo quy định'
    )
    Ten = models.CharField(max_length=128, null=False, 
        default='', help_text='Tên nghề')
    HoNghe = models.CharField(max_length=128, null=False,default='', help_text='Họ nghề')

    class Meta:
        verbose_name_plural = "Bảng ngành nghề khai thác"

    def __str__(self):
        return f"{self.HoNghe}-{self.IDNganhNghe}"


class BangTau(models.Model):
    '''
    Bảng tàu

    ID
    IDTau: Guid, bắt buộc: Mã định danh tàu
    SoDangKy: string (10-15), bắt buộc: Số đăng ký
    TenTau: string (1-128), bắt buộc: Tên tàu
    HoHieu: string (1-128), bắt buộc: Hô hiệu
    CoHieu: string (0-128), không bắt buộc: Cờ hiệu
    IMO: string (1-128), bắt buộc: IMO
    NoiDangKy: string (2-3), bắt buộc: Mã nơi đăng ký
    CangCaDangKy: string (2-3), bắt buộc: Mã cảng cá đăng ký
    CangCaPhu: string (2-3), bắt buộc: Mã cảng cá phụ
    NgheChinh: string (1-5), bắt buộc: Mã nghề
    NghePhu1: string (1-5), không bắt buộc: Mã nghề
    NghePhu2: string (1-5), không bắt buộc: Mã nghề
    NgayDangKy: string (10), bắt buộc: Ngày đăng ký
    NgayHetHanDangKy: string (10), bắt buộc: Thời hạn giấy phép
    TongTaiTrong: float, bắt buộc: Tổng tải trọng tàu
    ChieuDaiLonNhat: float, băt buộc: Chiều dài tàu
    ChieuRongLonNhat: float, bắt buộc: Chiều rộng tàu
    CongSuatMay: float, bắt buộc: Công suất máy
    MonNuoc float, bắt buộc: Mớn nước
    SoThuyenVien: Integer, bắt buộc: Số thuyền viên
    NgaySanXuat: string (10), không bắt buộc: Ngày sản xuất tàu
    NgayHetHan: string (10), không bắt buộc: Ngày hết hạn
    LoaiTau: string (2-3), bắt buộc: Mã loại tàu
    DungTichHamCa: float, không bắt buộc: Dung tích hầm cá
    VanTocDanhBat: float, bắt buộc: Vận tốc tàu chạy lúc đánh bắt
    VanTocHanhTrinh: float, bắt buộc: Vận tốc lớn nhất của tàu
    IDDevice: string, bắt buộc: ID thiết bị nhật ký khai thác
    IDChuTau: Guid, bắt buộc: Mã định danh chủ tàu
    IDThuyenTruong: Guid, bắt buộc: Mã định danh thuyền trưởng
    IDTinh: string, (2-3), bắt buộc: Mã tỉnh, TP theo quy định
    ThongSoNguCu: string, (1-255), bắt buộc: Thông số ngư cụ
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDTau = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4,
        help_text='Mã định danh tàu'
    )
    SoDangKy = models.CharField(
        max_length=15, null=False, default='', 
        help_text='Số đăng ký'
    ) 
    TenTau = models.CharField(max_length=128, 
        null=False, default='', help_text='Tên tàu')
    HoHieu = models.CharField(max_length=128, 
        null=False, default='', help_text='Hô hiệu')
    CoHieu = models.CharField(max_length=128, 
        null=True, blank=True, help_text='Cờ hiệu')
    IMO = models.CharField(max_length=128, null=False, default='', 
        help_text='IMO - International Maritime Organization - Tổ chức hàng hải quốc tế'
    )
    
    NoiDangKy = models.ForeignKey(
        BangDonViHanhChinhCapTinh,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )

    CangCaDangKy = models.ForeignKey(
        related_name='cangcadangky',
        to=BangCangCa,
        on_delete=models.DO_NOTHING,
        editable=False,
        null=False,
        default=1
    )
    
    CangCaPhu = models.ForeignKey(
        related_name='cangcadangky_2',
        to=BangCangCa,
        on_delete=models.DO_NOTHING,
        editable=False,
        null=False,
        default=1
    )

    NgheChinh = models.ForeignKey(
        related_name='nghechinh',
        to=BangNganhNgheKhaiThac,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )

    NghePhu1 = models.ForeignKey(related_name='nghephu_1', 
        to=BangNganhNgheKhaiThac,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    ) 

    NghePhu2 = models.ForeignKey(related_name='nghephu_2', 
        to=BangNganhNgheKhaiThac,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    ) 
    NgayDangKy = models.DateField(null=False, validators=[
        MinValueValidator(limit_value=date(1900, 1, 1)),
        MaxValueValidator(limit_value=date.today())
    ], help_text='Ngày đăng ký', default=date(1900, 1, 1))
    NgayHetHanDangKy = models.DateField(null=False, 
        help_text='Ngày hết hạn đăng ký', 
        default=date(1900, 1, 1)
    )
    TongTaiTrong = models.FloatField(null=False, 
        default=0, help_text='Tổng trọng tải tàu')
    ChieuDaiLonNhat = models.FloatField(null=False, 
        default=0, help_text='Chiều dài tàu')
    ChieuRongLonNhat = models.FloatField(null=False, 
        default=0, help_text='Chiều rộng tàu')
    CongSuatMay = models.FloatField(null=False, 
        default=0, help_text='Công suất máy')
    MonNuoc = models.FloatField(null=False, 
        default=0, help_text='Mớn nước')
    SoThuyenVien = models.IntegerField(null=False, 
        default=0, help_text='Số thuyền viên')
    NgaySanXuat = models.DateField(null=True, blank=True, validators=[
        MinValueValidator(limit_value=date(1900, 1, 1)),
        MaxValueValidator(limit_value=date.today())
    ], help_text='Ngày sản xuất')
    NgayHetHan = models.DateField(null=True, blank=True, default=date(1900, 1, 1), help_text='Ngày hết hạn')

    LoaiTau = models.ForeignKey(
        BangMaLoaiTau,
        on_delete=models.DO_NOTHING,
        null=False, default=1
    )  

    DungTichHamCa = models.FloatField(null=True, 
        blank=True, help_text='Dung tích hầm cá')
    VanTocDanhBat = models.FloatField(null=False, 
        default=0, help_text='Vận tốc tàu chạy lúc đánh bắt')
    VanTocHanhTrinh = models.FloatField(null=False, 
        default=0, help_text='Vận tốc lớn nhất của tàu')
    
    IDDevice = models.OneToOneField(
        BangThietBiNhatKyKhaiThac,
        on_delete=models.DO_NOTHING,
        null=True, 
        blank=True,
        help_text='Thiết bị nhật ký khai thác'
    )  
    
    IDChuTau = models.ForeignKey(
        BangChuTau,
        on_delete=models.DO_NOTHING,
        related_name='bangtau_chutau',
        null=True, blank=True,
    )  
    
    IDThuyenTruong = models.OneToOneField(
        BangThuyenTruong,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    
    IDTinh = models.ForeignKey(
        related_name='bang_tau_tinh',
        to=BangDonViHanhChinhCapTinh,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    ) 
    ThongSoNguCu = models.CharField(max_length=255, null=False, 
        default='', help_text='Thông số ngư cụ')

    class Meta:
        verbose_name_plural = "Bảng tàu"

    def __str__(self):
        return f"{self.ID}-{self.SoDangKy}-{self.IDChuTau.HoTen}-{self.CangCaDangKy.Ten}"


class BangLoaiCaDanhBat(models.Model):
    '''
    ID
    IDCa: string, (2-6), bắt buộc: Mã định danh của loại cá
    Ten: string, (1-128), bắt buộc: Tên loại cá
    '''
    ID = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDCa = models.CharField(
        max_length=6,
        null=False,
        default='',
        unique=True,
        help_text='Mã định danh của loại cá'
    )
    Ten = models.CharField(max_length=128, null=False, 
        default='', help_text='Tên loại cá')

    class Meta:
        verbose_name_plural = "Bảng loại cá đánh bắt"

    def __str__(self):
        return f"{self.IDCa}-{self.Ten}"


class BangVungBienDanhBat(models.Model):
    '''
    Đối tượng vùng biển đánh bắt
    
    ID
    IDVungBien: Guid, bắt buộc: Mã định danh vùng biển
    Ten: string (1-128), bắt buộc: Tên vùng biển
    Ma: string (1-10), bắt buộc: Mã vùng biển theo quy định
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDVungBien = models.UUIDField(
        unique=True, editable=False, default=uuid.uuid4,
        help_text='Mã định danh vùng biển'    
    )
    Ten = models.CharField(max_length=128, 
        null=False, default='', help_text='Tên vùng biển')
    Ma = models.CharField(max_length=10, 
        null=False, default='', help_text='Mã vùng biển theo quy định')

    class Meta:
        verbose_name_plural = "Bảng vùng biển đánh bắt"

    def __str__(self):
        return f"{self.ID}-{self.Ten}-{self.Ma}"


class BangChiTietVungBienDanhBat(models.Model):
    '''
    Đối tượng chi tiết vùng biển đánh bắt

    ID 
    IDVungBien: Guid, bắt buộc: Mã định danh vùng biển
    STT: Integer, bắt buộc: Số thứ tự của các đỉnh đa giác tạo thành vùng biển
    ViDo: Float, bắt buộc: Vĩ độ của 1 đỉnh đa giác của vùng biển, làm tròn 4 số phần thập phân
    KinhDo: Float, bắt buộc: Kinh độ của 1 đỉnh đa giác của vùng biển, làm tròn 4 số phần thập phân
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDVungBien = models.ForeignKey(
        BangVungBienDanhBat,
        on_delete=models.DO_NOTHING,
        null=False, 
        default=1
    )
    STT = models.IntegerField(null=False, default=1, 
        help_text='Số thứ tự của các đỉnh đa giác tạo thành vùng biển')
    ViDo = models.DecimalField(null=False, default=0, 
        help_text='Vĩ độ của 1 đỉnh đa giác của vùng biển', decimal_places=4, max_digits=8) # vĩ độ trung tâm vùng biển
    KinhDo = models.DecimalField(null=False, default=0, 
        help_text='Kinh độ của 1 đỉnh đa giác của vùng biển', decimal_places=4, max_digits=8) # kinh độ trung tâm vùng biển

    class Meta:
        verbose_name_plural = "Bảng chi tiết vùng biển đánh bắt"

    def __str__(self):
        return f"{self.ID}-{self.IDVungBien.Ten}"


class ToaDo(models.Model):
    ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    IDVungBien = models.ForeignKey(BangChiTietVungBienDanhBat, on_delete=models.DO_NOTHING,default=1)
    ViDo = models.DecimalField(null=False,default=0,decimal_places=4, max_digits=8)
    KinhDo = models.DecimalField(null=False,default=0,decimal_places=4,max_digits=8)

    class Meta:
        verbose_name_plural = "Bảng tọa độ"

    def __str__(self):
        return f"{self.ID} {self.ViDo}:{self.KinhDo}"


class BangViTriTau(models.Model):
    ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    IDTau = models.ForeignKey(
        BangTau,
        on_delete=models.DO_NOTHING,
        default=1,
    )
    ViDo = models.DecimalField(decimal_places=6, default=0, max_digits=12)
    KinhDo = models.DecimalField(decimal_places=6, default=0, max_digits=12)
    Ngay = models.DateTimeField(auto_now_add=True)
    TocDo = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    Huong = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Bảng vị trí tàu"

    def __str__(self):
        return f"{self.IDTau.SoDangKy}-{self.ViDo}:{self.KinhDo}"
