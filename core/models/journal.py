from django.db import models 
from .device import * 
from .report import * 


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
        null=True,
        blank=True
    )
    MaNhatKy = models.CharField(max_length=24, null=True, blank=True)
    NgayTao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Bảng nhật ký"

    def __str__(self):
        return f"{self.ID}-{self.IDThietBi.SoDangKy}"