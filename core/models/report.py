from django.db import models 
from .device import * 


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
    ViDoXuatBen = models.DecimalField(decimal_places=6, max_digits=12, null=True, blank=True)
    KinhDoXuatBen = models.DecimalField(decimal_places=6, max_digits=12, null=True, blank=True)
    VungBienDanhBat = models.ForeignKey(
        BangVungBienDanhBat,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    NgayVeBen = models.DateField(null=False, validators=[
        MinValueValidator(limit_value=date(1900, 1, 1)),
        MaxValueValidator(limit_value=date.today())
    ], default=date(1900, 1, 1), help_text='Ngày về bến')
    CangVeBen = models.ForeignKey(BangCangCa, on_delete=models.DO_NOTHING, 
        default=1, help_text='Mã cảng về bến', related_name='cangveben') 
    ViDoVeBen = models.DecimalField(decimal_places=6, max_digits=12, null=True, blank=True)
    KinhDoVeBen = models.DecimalField(decimal_places=6, max_digits=12, null=True, blank=True)
    KhoiLuongChuyenTai = models.IntegerField(null=True, 
        blank=True, help_text='Khối lượng chuyến tải')
    KhoiLuongDanhBat = models.IntegerField(default=0)

    IDTau = models.ForeignKey(
        BangTau,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    ) 

    class Meta:
        verbose_name_plural = "Bảng chuyến biển"

    def __str__(self):
        return f"{self.ID}-{self.IDTau.SoDangKy}-Chuyến biển: {self.ChuyenBienSo}-Khối lượng: {self.KhoiLuongChuyenTai}"


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
    IDChuyenBien = models.ForeignKey(
        BangChuyenBien,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    MeLuoiSo = models.IntegerField(default=0, 
        help_text='Số thứ tự của mẻ lưới của chuyến biển')
    ThoiDiemThaNguCu = models.DateTimeField()
    ViDoThaNguCu = models.DecimalField(null=False, default=0, max_digits=12,
        decimal_places=6, help_text='Vĩ độ thả ngư cụ')
    KinhDoThaNguCu = models.DecimalField(null=False, default=0, max_digits=12,
        decimal_places=6, help_text='Kinh độ thả ngư cụ')
    ThoiDiemThuNguCu = models.DateTimeField()
    ViDoThuNguCu = models.DecimalField(max_digits=12, null=False, default=0, 
        decimal_places=6, help_text='Vĩ độ thu ngư cụ')
    KinhDoThuNguCu = models.DecimalField(max_digits=12, null=False, default=0, 
        decimal_places=6, help_text='Kinh độ thu ngư cụ')
    TongSanLuong = models.IntegerField(null=False, 
        default=0, help_text='Tổng sản lượng của mẻ lưới')

    class Meta:
        verbose_name_plural = "Bảng mẻ lưới"

    def __str__(self):
        return f"{self.ID}-Tàu: {self.IDChuyenBien.IDTau.SoDangKy}-Chuyến biển: {self.IDChuyenBien.ChuyenBienSo}-{self.IDChuyenBien.KhoiLuongChuyenTai}-Mẻ lưới: {self.MeLuoiSo}-Sản lượng: {self.TongSanLuong}"


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
        null=True,
        blank=True
    )
    # STT = models.IntegerField(default=0, 
    #     help_text='Số thứ tự của loại cá của mẻ lưới')
    IDLoaiCa = models.ForeignKey(
        BangLoaiCaDanhBat,
        on_delete=models.DO_NOTHING,
        null=False,
        default=1
    )
    SanLuong = models.IntegerField(null=False, 
        default=0, help_text='Sản lượng loại cá được đánh bắt trong mẻ lưới')

    class Meta:
        verbose_name_plural = "Bảng loại cá đánh bắt được trong mẻ lưới"

    def __str__(self):
        return f"{self.ID}-ID mẻ lưới: {self.IDMeLuoi.MeLuoiSo}-Tổng mẻ lưới: {self.IDMeLuoi.TongSanLuong}-Loại cá: {self.IDLoaiCa.Ten}-Sản lượng: {self.SanLuong}"