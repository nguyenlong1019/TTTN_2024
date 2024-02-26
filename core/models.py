from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from django.utils import timezone 
from datetime import date 
from django.contrib.auth.models import User 
import uuid 

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save 
from django.dispatch import receiver


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


class BangChuTau(models.Model):
    '''
    Đối tượng chủ tàu

    ID
    IDChuTau: kiểu dữ liệu Guid (sử dụng uuid trong python), 
    bắt buộc: mã định danh chủ tàu
    HoTen: string (4-500), bắt buộc: họ tên chủ tàu
    CMND/CCCD: string (1-20), bắt buộc: Chứng minh nhân dân chủ tàu
    NgaySinh: string (1-10), bắt buộc: Ngày tháng năm sinh chủ tàu
    DiaChi: string (1-500), bắt buộc: Địa chỉ chủ tàu
    DienThoai: string (1-20), bắt buộc: Số điện thoại chủ tàu
    Fax: string (1-20), không bắt buộc, Số Fax của chủ tàu
    Email: string (1-100), không bắt buộc, Email của chủ tàu

    Mối quan hệ: BangChuTau và BangDonViHanhChinhCapHuyen có mối quan hệ 1-n với nhau
    Một huyện có nhiều chủ tàu và một chủ tàu thuộc (nằm trong) một huyện
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDChuTau = models.UUIDField(
        unique=True, 
        editable=False,
        default=uuid.uuid4,
        help_text='Mã định danh chủ tàu',
    )
    HoTen = models.CharField(
        max_length=500, null=False, 
        default='', help_text='Họ tên chủ tàu'
    )
    CMND_CCCD = models.CharField(
        max_length=20, null=False, default='', 
        help_text='Chứng minh nhân dân chủ tàu'
    )
    NgaySinh = models.DateField(null=False, 
        validators=[
            MinValueValidator(limit_value=date(1900, 1, 1)),
            MaxValueValidator(limit_value=date.today())
        ], 
        help_text='Ngày tháng năm sinh chủ tàu', 
        default=date(1900, 1, 1)
    )
    DiaChi = models.CharField(
        max_length=500, null=False, 
        default='', help_text='Địa chỉ chủ tàu'
    )
    DienThoai = models.CharField(
        max_length=20, null=False, 
        default='', help_text='Số điện thoại chủ tàu'
    )
    Fax = models.CharField(
        max_length=20, null=True, blank=True, 
        help_text='Số Fax của chủ tàu'
    )
    Email = models.CharField(
        max_length=100, null=True, blank=True, 
        help_text='Email của chủ tàu'
    )

    MaHuyen = models.ForeignKey(
        BangDonViHanhChinhCapHuyen, 
        on_delete=models.DO_NOTHING, # NO ACTION
        editable=False, # NO UPDATE
        null=False,
        default=1
    )

    class Meta:
        verbose_name_plural = "Bảng chủ tàu"

    def __str__(self):
        return f"{self.IDChuTau}-{self.HoTen}"


class BangThuyenTruong(models.Model):
    '''
    Đối tượng thuyền trưởng

    ID
    IDThuyenTruong: Guid, bắt buộc: mã định danh của thuyền trưởng
    HoTen: string (1-500), bắt buộc: Họ tên thuyền trưởng
    CMND: string (1-20), bắt buộc: Chứng minh nhân dân của thuyền trưởng
    NgaySinh: string (1-10), bắt buộc: Ngày tháng năm sinh của thuyền trưởng
    DiaChi: string (1-500), bắt buộc: Địa chỉ thuyền trưởng
    DienThoai: string (1-20), bắt buộc: Số điện thoại thuyền trưởng
    Fax: string (1-20), không bắt buộc: Số Fax của thuyền trưởng
    Email: string (1-100), không bắt buộc: Email của thuyền trưởng

    Mối quan hệ: trong một huyện có nhiều thuyền trưởng,
    một thuyền trưởng thuộc một huyện
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDThuyenTruong = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid.uuid4,
        help_text='Mã định danh chủ tàu'
    )
    HoTen = models.CharField(
        max_length=500, null=False, default='', 
        help_text='Họ tên thuyền trưởng'
    )
    CMND_CCCD = models.CharField(
        max_length=20, 
        null=False, 
        default='', 
        help_text='Chứng minh nhân dân thuyền trưởng'
    )
    NgaySinh = models.DateField(null=False, 
        validators=[
            MinValueValidator(limit_value=date(1900, 1, 1)),
            MaxValueValidator(limit_value=date.today())
        ], 
        help_text='Ngày tháng năm sinh thuyền trưởng', 
        default=date(1900, 1, 1)
    )
    DiaChi = models.CharField(
        max_length=500, null=False, default='', 
        help_text='Địa chỉ thuyền trưởng'
    )
    DienThoai = models.CharField(
        max_length=20, null=False, default='', 
        help_text='Số điện thoại thuyền trưởng'
    )
    Fax = models.CharField(max_length=20, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)

    # Tham chiếu Mã Huyện
    MaHuyen = models.ForeignKey(
        BangDonViHanhChinhCapHuyen,
        on_delete=models.DO_NOTHING,
        editable=False,
        null=False,
        default=1
    )

    class Meta:
        verbose_name_plural = "Bảng thuyền trưởng"

    def __str__(self):
        return f"{self.IDThuyenTruong}-{self.HoTen}"


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
    DiaChi = models.CharField(max_length=500, 
        null=False, default='', help_text='Địa chỉ cảng cá')
    DienThoai = models.CharField(max_length=20, 
        null=True, blank=True, help_text='Điện thoại cảng cá')
    ViDo = models.DecimalField(null=False, decimal_places=4, 
        default=0, help_text='Vĩ độ cảng cá', max_digits=8)
    KinhDo = models.DecimalField(null=False, decimal_places=4, 
        default=0, help_text='Kinh độ cảng cá', max_digits=8)
    
    # các trường tự thêm
    Fax = models.CharField(max_length=20, 
        null=True, blank=True, help_text='Fax cảng cá')
    Email = models.CharField(max_length=128, 
        null=True, blank=True, help_text='Email cảng cá')
    # các trường tự thêm
    
    # Cảng trưởng nên thêm model vào User ()
    TenCangTruong = models.CharField(max_length=128, 
        null=True, blank=True, help_text='Tên cảng trưởng')
    DienThoaiCangTruong = models.CharField(max_length=20, 
        null=True, blank=True, help_text='Điện thoại cảng trưởng')

    # Quan hệ 1 - n với bảng đơn vị hành chính cấp tỉnh
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
    

class BangThietBiNhatKyKhaiThac(models.Model):
    '''
    ID
    IDThietBi: string (6), bắt buộc: Mã định danh của thiết bị
    SerialNumber: string (10), bắt buộc: Số serial của thiết bị
    NgaySanXuat: string (10), không bắt buộc: Ngày sản xuất
    FWVersion: string (10), không bắt buộc: Version Firmware
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDThietBi = models.UUIDField(
        unique=True,
        editable=False, 
        default=uuid.uuid4,
        help_text='Mã định danh thiết bị'
    )
    SerialNumber = models.CharField(max_length=10, null=False, 
        default='', help_text='Số serial của thiết bị')
    NgaySanXuat = models.DateField(
        null=True, blank=True, 
        help_text='Ngày sản xuất', 
        validators=[
            MinValueValidator(limit_value=date(1900, 1, 1)),
            MaxValueValidator(limit_value=date.today())
        ]
    )
    FWVersion = models.CharField(max_length=10, null=False, 
        default='', help_text='Version Firmware')

    # is_active

    class Meta:
        verbose_name_plural = "Bảng thiết bị nhật ký khai thác"

    def __str__(self):
        return f"{self.IDThietBi}-{self.SerialNumber}"


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
    ) # số đăng ký giống như biển số của tàu
    TenTau = models.CharField(max_length=128, 
        null=False, default='', help_text='Tên tàu')
    HoHieu = models.CharField(max_length=128, 
        null=False, default='', help_text='Hô hiệu')
    CoHieu = models.CharField(max_length=128, 
        null=True, blank=True, help_text='Cờ hiệu')
    IMO = models.CharField(max_length=128, null=False, default='', 
        help_text='IMO - International Maritime Organization - Tổ chức hàng hải quốc tế'
    )
    # tham chiếu đến bảng đơn vị hành chính cấp tỉnh
    # một tàu thuộc về một tỉnh, một tỉnh có nhiều tàu
    NoiDangKy = models.ForeignKey(
        BangDonViHanhChinhCapTinh,
        on_delete=models.DO_NOTHING,
        editable=False,
        null=False,
        default=1
    )
    # tham chiếu đến bảng cảng cá
    # một cảng cá quản lý nhiều tàu, một tàu thuộc một cảng cá 
    # (tàu đăng ký bắt đầu hoạt động ở một cảng cá nhưng vẫn có thể đến các cảng cá khác)
    CangCaDangKy = models.ForeignKey(
        related_name='cangcadangky',
        to=BangCangCa,
        on_delete=models.DO_NOTHING,
        editable=False,
        null=False,
        default=1
    )
    # tham chiếu đến cả cá phụ của bảng cảng cá
    CangCaPhu = models.ForeignKey(
        related_name='cangcadangky_2',
        to=BangCangCa,
        on_delete=models.DO_NOTHING,
        editable=False,
        null=False,
        default=1
    )
    # tham chiếu đến bảng ngành nghề khai thác
    NgheChinh = models.ForeignKey(
        related_name='nghechinh',
        to=BangNganhNgheKhaiThac,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )

    # tham chiếu đến bảng ngành nghề khai thác
    NghePhu1 = models.ForeignKey(related_name='nghephu_1', 
        to=BangNganhNgheKhaiThac,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    ) 
    # tham chiếu đến bảng ngành nghề khai thác
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

    # tham chiếu đến bảng mã loại tàu
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
    
    # tham chiếu đến bảng thiết bị nhật ký khai thác
    IDDevice = models.OneToOneField(
        BangThietBiNhatKyKhaiThac,
        on_delete=models.DO_NOTHING,
        null=False, 
        default=1
    )  
    # tham chiếu đến bảng chủ tàu
    IDChuTau = models.ForeignKey(
        BangChuTau,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )  
    # tham chiếu đến bảng thuyền trưởng
    IDThuyenTruong = models.OneToOneField(
        BangThuyenTruong,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )
    # tham chiếu đến tỉnh
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
        return f"{self.ID}-{self.SoDangKy}-{self.IDChuTau.HoTen}"


class BangLoaiCaDanhBat(models.Model):
    '''
    ID
    IDCa: string, (2-6), bắt buộc: Mã định danh của loại cá
    Ten: string, (1-128), bắt buộc: Tên loại cá
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDCa = models.CharField(
        max_length=6,
        null=False,
        default='',
        unique=True,
        editable=False,
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


class BangChuyenBien(models.Model):
    '''
    Đối tượng chuyến biển

    ID
    IDChuyenBien: Guid, bắt buộc: Mã định danh chuyển biến
    ChuyenBienSo: Integer, bắt buộc: Số thứ tự chuyến biển trong năm
    NgayXuatBen: string (10), bắt buộc: Ngày xuất bến, định dạng dd/MM/yyyy
    CangXuatBen: string (2-3), bắt buộc: Mã cảng xuất bến
    VungBienDanhBat: string (1-500), bắt buộc: Tên vùng biển đánh bắt
    NgayVeBen: string (10), bắt buộc: Ngày về bến
    CangVeBen: string (2-3), bắt buộc: Mã cảng về bến
    KhoiLuongChuyenTai: integer, không bắt buộc: Khối lượng chuyển tải
    IDTau: Guid, bắt buộc: Mã định danh tàu cá
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDChuyenBien = models.UUIDField(
        unique=True,editable=False,default=uuid.uuid4,
        help_text='Mã định danh chuyến biển'
    )
    ChuyenBienSo = models.IntegerField(null=False, 
        default=0, help_text='Số thứ tự chuyến biển trong năm')
    NgayXuatBen = models.DateField(
        null=False, validators=[
            MinValueValidator(limit_value=date(1900, 1, 1)),
            MaxValueValidator(limit_value=date.today())
        ], 
        default=date(1900, 1, 1), help_text='Ngày xuất bến'
    )
    CangXuatBen = models.ForeignKey(
        BangCangCa, 
        on_delete=models.DO_NOTHING,
        null=False, 
        default=1,
        related_name='cangxuatben'
    )
    VungBienDanhBat = models.ForeignKey(
        BangVungBienDanhBat,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )

    # CangXuatBen = models.CharField(max_length=6, null=False, 
    #     default='', help_text='Mã cảng xuất bến') # tham chiếu đến bảng cảng cá
    # VungBienDanhBat = models.CharField(max_length=500, null=False, 
    #     default='', help_text='Tên vùng biển đánh bắt') # tham chiếu đến bảng vùng biển đánh bắt
    NgayVeBen = models.DateField(null=False, validators=[
        MinValueValidator(limit_value=date(1900, 1, 1)),
        MaxValueValidator(limit_value=date.today())
    ], default=date(1900, 1, 1), help_text='Ngày về bến')
    CangVeBen = models.ForeignKey(BangCangCa, on_delete=models.DO_NOTHING, 
        default=1, help_text='Mã cảng về bến', related_name='cangveben') # tham chiếu đến bảng cảng cá
    KhoiLuongChuyenTai = models.IntegerField(null=True, 
        blank=True, help_text='Khối lượng chuyến tải')
    # chuyến biển của tàu nào
    IDTau = models.ForeignKey(
        BangTau,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    ) 

    class Meta:
        verbose_name_plural = "Bảng chuyến biển"

    def __str__(self):
        return f"{self.ID}-{self.IDTau.SoDangKy}-{self.ChuyenBienSo}"


class BangMeLuoi(models.Model):
    '''
    Đối tượng mẻ lưới

    ID
    IDChuyenBien: Guid, bắt buộc: Mã định danh chuyến biển
    IDMeLuoi: Guid, bắt buộc: Mã định danh mẻ lưới
    STT: Integer, bắt buộc: Số thứ tự của mẻ lưới của chuyến biển
    ThoiDiemThaNguCu: string (16), bắt buộc: Thời điểm thả ngư cụ (ngày tháng năm giờ phút)
    ViDoThaNguCu: Float, bắt buộc: Vĩ độ thả ngư cụ, làm tròn 4 chữ số phần thập phân
    KinhDoThaNguCu: Float, bắt buộc: Kinh độ thả ngư cụ
    ThoiDiemThuNguCu: String (16), bắt buộc: Thời điểm thu ngư cụ
    ViDoThuNguCu: Float, bắt buộc: Vĩ độ thu ngư cụ
    KinhDoThuNguCu: Float, bắt buộc: Kinh độ thu ngư cụ
    TongSanLuong: Integer, bắt buộc: Tổng sản lượng của mẻ lưới
    '''
    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    # một chuyến biển có nhiều mẻ lưới, một mẻ lưới xác định thuộc về một chuyến biển
    IDChuyenBien = models.ForeignKey(
        BangChuyenBien,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )
    IDMeLuoi = models.UUIDField( 
        unique=True, editable=False,
        default=uuid.uuid4, help_text='Mã định danh của mẻ lưới'    
    )
    STT = models.IntegerField(null=False, default=0, 
        help_text='Số thứ tự của mẻ lưới của chuyến biển')
    ThoiDiemThaNguCu = models.DateTimeField(null=False,
        default='01/01/1900 00:00',
        validators=[
            MinValueValidator(limit_value='01/01/1900 00:00'),
            MaxValueValidator(limit_value='31/12/2099 23:59')
        ]
    )
    # Hoặc sử dụng MaxValue như sau:
    # MaxValueValidator(limit_value=timezone.now().replace(second=0, microsecond=0)),
    ViDoThaNguCu = models.DecimalField(null=False, default=0, max_digits=8,
        decimal_places=4, help_text='Vĩ độ thả ngư cụ')
    KinhDoThaNguCu = models.DecimalField(null=False, default=0, max_digits=8,
        decimal_places=4, help_text='Kinh độ thả ngư cụ')
    ThoiDiemThuNguCu = models.DateTimeField(null=False,
        default='01/01/1900 00:00',
        validators=[
            MinValueValidator(limit_value='01/01/1900 00:00'),
            MaxValueValidator(limit_value='31/12/2099 23:59')
        ]
    )
    ViDoThuNguCu = models.DecimalField(max_digits=8, null=False, default=0, 
        decimal_places=4, help_text='Vĩ độ thu ngư cụ')
    KinhDoThuNguCu = models.DecimalField(max_digits=8, null=False, default=0, 
        decimal_places=4, help_text='Kinh độ thu ngư cụ')
    TongSanLuong = models.IntegerField(null=False, 
        default=0, help_text='Tổng sản lượng của mẻ lưới')

    class Meta:
        verbose_name_plural = "Bảng mẻ lưới"

    def __str__(self):
        return f"{self.ID}-{self.IDMeLuoi}"


class BangLoaiCaDuocDanhBatTrongMeLuoi(models.Model):
    '''
    Đối tượng loại cá được đánh bắt trong một mẻ lưới (mẻ lưới - loại cá)

    ID
    IDMeLuoi: Guid, bắt buộc: Mã định danh mẻ lưới
    STT: Integer, bắt buộc: Số thứ tự của loại cá của mẻ lưới
    IDLoaiCa: string (2-6), bắt buộc: Mã loại cá
    SanLuong: Integer, bắt buộc: Sản lượng loại cá được đánh bắt trong một mẻ lưới
    '''

    ID = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
    )
    IDMeLuoi = models.ForeignKey(
        BangMeLuoi,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )
    STT = models.IntegerField(null=False, default=0, 
        help_text='Số thứ tự của loại cá của mẻ lưới')
    IDLoaiCa = models.ForeignKey(
        BangLoaiCaDanhBat,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )
    SanLuong = models.IntegerField(null=False, 
        default=0, help_text='Sản lượng loại cá được đánh bắt trong mẻ lưới')

    class Meta:
        verbose_name_plural = "Bảng loại cá được đánh bắt"

    def __str__(self):
        return f"{self.ID}-{self.IDMeLuoi.IDMeLuoi}"


class BangViTriTau(models.Model):
    ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    IDTau = models.ForeignKey(
        BangTau,
        on_delete=models.DO_NOTHING,
        default=1,
    )
    ViDo = models.DecimalField(decimal_places=4, default=0, max_digits=8)
    KinhDo = models.DecimalField(decimal_places=4, default=0, max_digits=8)
    Ngay = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Bảng vị trí tàu"

    def __str__(self):
        return f"{self.IDTau.SoDangKy}-{self.ViDo}:{self.KinhDo}"
     

class BangNhatKy(models.Model):
    ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    IDThietBi = models.ForeignKey(
        BangTau,
        on_delete=models.DO_NOTHING,
        default=1
    )
    IDChuyenBien = models.ForeignKey(
        BangChuyenBien,
        on_delete=models.DO_NOTHING,
        default=1
    )

    class Meta:
        verbose_name_plural = "Bảng nhật ký"

    def __str__(self):
        return f"{self.ID}-{self.IDThietBi.SerialNumber}"

