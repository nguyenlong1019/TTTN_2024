from django.db import models 


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

    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Bảng thiết bị nhật ký khai thác"

    def __str__(self):
        return f"{self.IDThietBi}-{self.SerialNumber}"
