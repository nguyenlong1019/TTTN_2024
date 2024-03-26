# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CoreAdminhod(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    admin = models.OneToOneField('CoreCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_adminhod'


class CoreBangcangca(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idcangca = models.CharField(db_column='IDCangCa', unique=True, max_length=6)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=128)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255)  # Field name made lowercase.
    dienthoai = models.CharField(db_column='DienThoai', max_length=20, blank=True, null=True)  # Field name made lowercase.
    vido = models.FloatField(db_column='ViDo')  # Field name made lowercase.
    kinhdo = models.FloatField(db_column='KinhDo')  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=128, blank=True, null=True)  # Field name made lowercase.
    tencangtruong = models.CharField(db_column='TenCangTruong', max_length=128, blank=True, null=True)  # Field name made lowercase.
    dienthoaicangtruong = models.CharField(db_column='DienThoaiCangTruong', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idtinh = models.ForeignKey('CoreBangdonvihanhchinhcaptinh', models.DO_NOTHING, db_column='IDTinh_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangcangca'


class CoreBangchitietchuyentai(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idchuyentai = models.ForeignKey('CoreBangchuyentai', models.DO_NOTHING, db_column='IDChuyenTai_id', blank=True, null=True)  # Field name made lowercase.
    idmaca = models.ForeignKey('CoreBangloaicadanhbat', models.DO_NOTHING, db_column='IDMaCa', blank=True, null=True)  # Field name made lowercase.
    khoiluongchuyentai = models.IntegerField(db_column='KhoiLuongChuyenTai', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangchitietchuyentai'


class CoreBangchitietvungbiendanhbat(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    stt = models.IntegerField(db_column='STT')  # Field name made lowercase.
    vido = models.DecimalField(db_column='ViDo', max_digits=8, decimal_places=4)  # Field name made lowercase.
    kinhdo = models.DecimalField(db_column='KinhDo', max_digits=8, decimal_places=4)  # Field name made lowercase.
    idvungbien = models.ForeignKey('CoreBangvungbiendanhbat', models.DO_NOTHING, db_column='IDVungBien_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangchitietvungbiendanhbat'


class CoreBangchutau(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idchutau = models.CharField(db_column='IDChuTau', unique=True, max_length=32)  # Field name made lowercase.
    hoten = models.CharField(db_column='HoTen', max_length=255)  # Field name made lowercase.
    cmnd_cccd = models.CharField(db_column='CMND_CCCD', max_length=20)  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NgaySinh')  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255)  # Field name made lowercase.
    dienthoai = models.CharField(db_column='DienThoai', max_length=20)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mahuyen = models.ForeignKey('CoreBangdonvihanhchinhcaphuyen', models.DO_NOTHING, db_column='MaHuyen_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangchutau'


class CoreBangchuyenbien(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idtau = models.ForeignKey('CoreBangtau', models.DO_NOTHING, db_column='IDTau_id')  # Field name made lowercase.
    chuyenbienso = models.IntegerField(db_column='ChuyenBienSo')  # Field name made lowercase.
    ngayxuatben = models.DateTimeField(db_column='NgayXuatBen')  # Field name made lowercase.
    vidoxuatben = models.FloatField(db_column='ViDoXuatBen', blank=True, null=True)  # Field name made lowercase.
    kinhdoxuatben = models.FloatField(db_column='KinhDoXuatBen', blank=True, null=True)  # Field name made lowercase.
    cangxuatben = models.ForeignKey(CoreBangcangca, models.DO_NOTHING, db_column='CangXuatBen_id')  # Field name made lowercase.
    ngayveben = models.DateTimeField(db_column='NgayVeBen')  # Field name made lowercase.
    vidoveben = models.FloatField(db_column='ViDoVeBen', blank=True, null=True)  # Field name made lowercase.
    cangveben_id = models.BigIntegerField(db_column='CangVeBen_id')  # Field name made lowercase.
    kinhdoveben = models.FloatField(db_column='KinhDoVeBen', blank=True, null=True)  # Field name made lowercase.
    vungbiendanhbat = models.ForeignKey('CoreBangvungbiendanhbat', models.DO_NOTHING, db_column='VungBienDanhBat_id')  # Field name made lowercase.
    khoiluongchuyentai = models.BigIntegerField(db_column='KhoiLuongChuyenTai', blank=True, null=True)  # Field name made lowercase.
    khoiluongdanhbat = models.BigIntegerField(db_column='KhoiLuongDanhBat', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangchuyenbien'


class CoreBangchuyentai(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    chuyenbien = models.ForeignKey(CoreBangchuyenbien, models.DO_NOTHING, db_column='ChuyenBien_id', blank=True, null=True)  # Field name made lowercase.
    chuyentaiso = models.BigIntegerField(db_column='ChuyenTaiSo', blank=True, null=True)  # Field name made lowercase.
    tauchuyentai = models.CharField(db_column='TauChuyenTai', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vidochuyentai = models.FloatField(db_column='ViDoChuyenTai', blank=True, null=True)  # Field name made lowercase.
    kinhdochuyentai = models.FloatField(db_column='KinhDoChuyentai', blank=True, null=True)  # Field name made lowercase.
    thoigianchuyentai = models.DateTimeField(db_column='ThoiGianChuyenTai', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangchuyentai'


class CoreBangdonvihanhchinhcaphuyen(models.Model):
    mahuyen = models.IntegerField(db_column='MaHuyen', primary_key=True)  # Field name made lowercase.
    tenhuyen = models.CharField(db_column='TenHuyen', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tenhuyenen = models.CharField(db_column='TenHuyenEn', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cap = models.CharField(db_column='Cap', max_length=50, blank=True, null=True)  # Field name made lowercase.
    matinh = models.ForeignKey('CoreBangdonvihanhchinhcaptinh', models.DO_NOTHING, db_column='MaTinh_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangdonvihanhchinhcaphuyen'


class CoreBangdonvihanhchinhcaptinh(models.Model):
    matinh = models.IntegerField(db_column='MaTinh', primary_key=True)  # Field name made lowercase.
    tentiengviet = models.CharField(db_column='TenTiengViet', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tenviettat = models.CharField(db_column='TenVietTat', max_length=6, blank=True, null=True)  # Field name made lowercase.
    tentienganh = models.CharField(db_column='TenTiengAnh', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cap = models.CharField(db_column='Cap', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangdonvihanhchinhcaptinh'


class CoreBangloaicadanhbat(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idca = models.CharField(db_column='IDCa', unique=True, max_length=6)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangloaicadanhbat'


class CoreBangloaicaduocdanhbattrongmeluoi(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idmeluoi = models.ForeignKey('CoreBangmeluoi', models.DO_NOTHING, db_column='IDMeLuoi_id')  # Field name made lowercase.
    idloaica_id = models.BigIntegerField(db_column='IDLoaiCa_id')  # Field name made lowercase.
    sanluong = models.IntegerField(db_column='SanLuong')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangloaicaduocdanhbattrongmeluoi'


class CoreBangmaloaitau(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idloaitau = models.CharField(db_column='IDLoaiTau', unique=True, max_length=8)  # Field name made lowercase.
    tenloaitau = models.CharField(db_column='TenLoaiTau', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangmaloaitau'


class CoreBangmeluoi(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idchuyenbien_id = models.BigIntegerField(db_column='IDChuyenBien_id')  # Field name made lowercase.
    meluoiso = models.IntegerField(db_column='MeLuoiSo')  # Field name made lowercase.
    thoidiemthangucu = models.DateTimeField(db_column='ThoiDiemThaNguCu')  # Field name made lowercase.
    vidothangucu = models.FloatField(db_column='ViDoThaNguCu')  # Field name made lowercase.
    kinhdothangucu = models.FloatField(db_column='KinhDoThaNguCu')  # Field name made lowercase.
    thoidiemthungucu = models.DateTimeField(db_column='ThoiDiemThuNguCu')  # Field name made lowercase.
    vidothungucu = models.FloatField(db_column='ViDoThuNguCu')  # Field name made lowercase.
    kinhdothungucu = models.FloatField(db_column='KinhDoThuNguCu')  # Field name made lowercase.
    tongsanluong = models.IntegerField(db_column='TongSanLuong')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangmeluoi'


class CoreBangnganhnghekhaithac(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idnganhnghe = models.CharField(db_column='IDNganhNghe', unique=True, max_length=5)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=128)  # Field name made lowercase.
    honghe = models.CharField(db_column='HoNghe', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangnganhnghekhaithac'


class CoreBangnhatky(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    manhatky = models.CharField(db_column='MaNhatKy', max_length=24, blank=True, null=True)  # Field name made lowercase.
    ngaytao = models.DateTimeField(db_column='NgayTao')  # Field name made lowercase.
    idchuyenbien = models.ForeignKey(CoreBangchuyenbien, models.DO_NOTHING, db_column='IDChuyenBien_id')  # Field name made lowercase.
    idthietbi = models.ForeignKey('CoreBangtau', models.DO_NOTHING, db_column='IDThietBi_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangnhatky'


class CoreBangtau(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idtau = models.CharField(db_column='IDTau', unique=True, max_length=32)  # Field name made lowercase.
    sodangky = models.CharField(db_column='SoDangKy', max_length=15)  # Field name made lowercase.
    tentau = models.CharField(db_column='TenTau', max_length=128)  # Field name made lowercase.
    hohieu = models.CharField(db_column='HoHieu', max_length=128)  # Field name made lowercase.
    cohieu = models.CharField(db_column='CoHieu', max_length=128, blank=True, null=True)  # Field name made lowercase.
    imo = models.CharField(db_column='IMO', max_length=128)  # Field name made lowercase.
    ngaydangky = models.DateField(db_column='NgayDangKy')  # Field name made lowercase.
    ngayhethandangky = models.DateField(db_column='NgayHetHanDangKy')  # Field name made lowercase.
    tongtaitrong = models.FloatField(db_column='TongTaiTrong')  # Field name made lowercase.
    chieudailonnhat = models.FloatField(db_column='ChieuDaiLonNhat')  # Field name made lowercase.
    chieuronglonnhat = models.FloatField(db_column='ChieuRongLonNhat')  # Field name made lowercase.
    congsuatmay = models.FloatField(db_column='CongSuatMay')  # Field name made lowercase.
    monnuoc = models.FloatField(db_column='MonNuoc')  # Field name made lowercase.
    sothuyenvien = models.IntegerField(db_column='SoThuyenVien')  # Field name made lowercase.
    ngaysanxuat = models.DateField(db_column='NgaySanXuat', blank=True, null=True)  # Field name made lowercase.
    ngayhethan = models.DateField(db_column='NgayHetHan', blank=True, null=True)  # Field name made lowercase.
    dungtichhamca = models.FloatField(db_column='DungTichHamCa', blank=True, null=True)  # Field name made lowercase.
    vantocdanhbat = models.FloatField(db_column='VanTocDanhBat')  # Field name made lowercase.
    vantochanhtrinh = models.FloatField(db_column='VanTocHanhTrinh')  # Field name made lowercase.
    thongsongucu = models.CharField(db_column='ThongSoNguCu', max_length=255)  # Field name made lowercase.
    cangcadangky = models.ForeignKey(CoreBangcangca, models.DO_NOTHING, db_column='CangCaDangKy_id')  # Field name made lowercase.
    cangcaphu = models.ForeignKey(CoreBangcangca, models.DO_NOTHING, db_column='CangCaPhu_id', related_name='corebangtau_cangcaphu_set')  # Field name made lowercase.
    idchutau = models.ForeignKey(CoreBangchutau, models.DO_NOTHING, db_column='IDChuTau_id', blank=True, null=True)  # Field name made lowercase.
    iddevice = models.OneToOneField('CoreBangthietbinhatkykhaithac', models.DO_NOTHING, db_column='IDDevice_id', blank=True, null=True)  # Field name made lowercase.
    idthuyentruong = models.OneToOneField('CoreBangthuyentruong', models.DO_NOTHING, db_column='IDThuyenTruong_id', blank=True, null=True)  # Field name made lowercase.
    idtinh = models.ForeignKey(CoreBangdonvihanhchinhcaptinh, models.DO_NOTHING, db_column='IDTinh_id')  # Field name made lowercase.
    loaitau = models.ForeignKey(CoreBangmaloaitau, models.DO_NOTHING, db_column='LoaiTau_id')  # Field name made lowercase.
    nghechinh = models.ForeignKey(CoreBangnganhnghekhaithac, models.DO_NOTHING, db_column='NgheChinh_id')  # Field name made lowercase.
    nghephu1 = models.ForeignKey(CoreBangnganhnghekhaithac, models.DO_NOTHING, db_column='NghePhu1_id', related_name='corebangtau_nghephu1_set', blank=True, null=True)  # Field name made lowercase.
    nghephu2 = models.ForeignKey(CoreBangnganhnghekhaithac, models.DO_NOTHING, db_column='NghePhu2_id', related_name='corebangtau_nghephu2_set', blank=True, null=True)  # Field name made lowercase.
    noidangky = models.ForeignKey(CoreBangdonvihanhchinhcaptinh, models.DO_NOTHING, db_column='NoiDangKy_id', related_name='corebangtau_noidangky_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangtau'


class CoreBangthietbinhatkykhaithac(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idthietbi = models.CharField(db_column='IDThietBi', unique=True, max_length=32)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber', max_length=20)  # Field name made lowercase.
    ngaysanxuat = models.DateField(db_column='NgaySanXuat', blank=True, null=True)  # Field name made lowercase.
    fwversion = models.CharField(db_column='FWVersion', max_length=10)  # Field name made lowercase.
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'core_bangthietbinhatkykhaithac'


class CoreBangthuyentruong(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idthuyentruong = models.CharField(db_column='IDThuyenTruong', unique=True, max_length=32)  # Field name made lowercase.
    hoten = models.CharField(db_column='HoTen', max_length=500)  # Field name made lowercase.
    cmnd_cccd = models.CharField(db_column='CMND_CCCD', max_length=20)  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NgaySinh')  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255)  # Field name made lowercase.
    dienthoai = models.CharField(db_column='DienThoai', max_length=20)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hasship = models.IntegerField(db_column='hasShip')  # Field name made lowercase.
    mahuyen = models.ForeignKey(CoreBangdonvihanhchinhcaphuyen, models.DO_NOTHING, db_column='MaHuyen_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangthuyentruong'


class CoreBangvitritau(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    vido = models.DecimalField(db_column='ViDo', max_digits=12, decimal_places=6)  # Field name made lowercase.
    kinhdo = models.DecimalField(db_column='KinhDo', max_digits=12, decimal_places=6)  # Field name made lowercase.
    ngay = models.DateTimeField(db_column='Ngay')  # Field name made lowercase.
    tocdo = models.DecimalField(db_column='TocDo', max_digits=12, decimal_places=2)  # Field name made lowercase.
    huong = models.IntegerField(db_column='Huong')  # Field name made lowercase.
    idtau = models.ForeignKey(CoreBangtau, models.DO_NOTHING, db_column='IDTau_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangvitritau'


class CoreBangvungbiendanhbat(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idvungbien = models.CharField(db_column='IDVungBien', unique=True, max_length=32)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=128)  # Field name made lowercase.
    ma = models.CharField(db_column='Ma', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_bangvungbiendanhbat'


class CoreCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    user_type = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'core_customuser'


class CoreCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(CoreCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_customuser_groups'
        unique_together = (('customuser', 'group'),)


class CoreCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(CoreCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class CorePackage(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    idtau = models.ForeignKey(CoreBangtau, models.DO_NOTHING, db_column='IDTau', blank=True, null=True)  # Field name made lowercase.
    class_field = models.ForeignKey('CorePackageclass', models.DO_NOTHING, db_column='Class_id', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    source = models.ForeignKey('CorePackagesource', models.DO_NOTHING, db_column='Source_id', blank=True, null=True)  # Field name made lowercase.
    package_data = models.TextField(db_column='Package_data', blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    state = models.ForeignKey('CorePackagestates', models.DO_NOTHING, db_column='State_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_package'


class CorePackageclass(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bytetype = models.TextField(db_column='ByteType', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_packageclass'


class CorePackagesource(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_packagesource'


class CorePackagestates(models.Model):
    id = models.SmallAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    node = models.CharField(db_column='Node', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_packagestates'


class CoreProvider(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    admin = models.OneToOneField(CoreCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_provider'


class CoreStaff(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    admin = models.OneToOneField(CoreCustomuser, models.DO_NOTHING)
    cangca = models.ForeignKey(CoreBangcangca, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_staff'


class CoreToado(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    vido = models.DecimalField(db_column='ViDo', max_digits=8, decimal_places=4)  # Field name made lowercase.
    kinhdo = models.DecimalField(db_column='KinhDo', max_digits=8, decimal_places=4)  # Field name made lowercase.
    idvungbien = models.ForeignKey(CoreBangchitietvungbiendanhbat, models.DO_NOTHING, db_column='IDVungBien_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_toado'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(CoreCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
