from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import * 

class UserModel(UserAdmin):
    list_display = ('username','email', 'user_type', 'first_name', 'last_name')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, UserModel)

admin.site.register(BangDonViHanhChinhCapTinh)
admin.site.register(BangDonViHanhChinhCapHuyen)
admin.site.register(BangMaLoaiTau)
admin.site.register(BangChuTau)
admin.site.register(BangThuyenTruong)
admin.site.register(BangCangCa)
admin.site.register(BangNganhNgheKhaiThac)
admin.site.register(BangThietBiNhatKyKhaiThac)
admin.site.register(BangTau)
admin.site.register(BangLoaiCaDanhBat)
admin.site.register(BangVungBienDanhBat)
admin.site.register(BangChiTietVungBienDanhBat)
admin.site.register(BangToaDo)
admin.site.register(BangViTriTau)
admin.site.register(BangChuyenBien)
admin.site.register(BangMeLuoi)
admin.site.register(BangLoaiCaDuocDanhBatTrongMeLuoi)
admin.site.register(BangNhatKy)

# admin
# admin@gmail.com
# @admin123 
