from django.db import models
from .device import * 


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
        max_length=255, null=False, 
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
        max_length=255, null=False, 
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
        null=False,
        default=1
    )

    class Meta:
        verbose_name_plural = "Bảng chủ tàu"

    def __str__(self):
        return f"{self.HoTen}-CMND:{self.CMND_CCCD}-Phone:{self.DienThoai}"


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
        max_length=255, null=False, default='', 
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
        null=False,
        default=1
    )
    hasShip = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Bảng thuyền trưởng"

    def __str__(self):
        return f"{self.HoTen}-CMND:{self.CMND_CCCD}-Phone:{self.DienThoai}"
