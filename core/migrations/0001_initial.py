# Generated by Django 4.2.9 on 2024-03-17 15:55

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'Admin'), (2, 'Staff'), (3, 'Provider')], default=1, max_length=15)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BangCangCa',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDCangCa', models.CharField(default='', help_text='Mã định danh của cảng cá theo quy định', max_length=6, unique=True)),
                ('Ten', models.CharField(default='', help_text='Tên cảng cá', max_length=128)),
                ('DiaChi', models.CharField(default='', help_text='Địa chỉ cảng cá', max_length=255)),
                ('DienThoai', models.CharField(blank=True, help_text='Điện thoại cảng cá', max_length=20, null=True)),
                ('ViDo', models.DecimalField(decimal_places=4, default=0, help_text='Vĩ độ cảng cá', max_digits=8)),
                ('KinhDo', models.DecimalField(decimal_places=4, default=0, help_text='Kinh độ cảng cá', max_digits=8)),
                ('Fax', models.CharField(blank=True, help_text='Fax cảng cá', max_length=20, null=True)),
                ('Email', models.CharField(blank=True, help_text='Email cảng cá', max_length=128, null=True)),
                ('TenCangTruong', models.CharField(blank=True, help_text='Tên cảng trưởng', max_length=128, null=True)),
                ('DienThoaiCangTruong', models.CharField(blank=True, help_text='Điện thoại cảng trưởng', max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Bảng cảng cá',
            },
        ),
        migrations.CreateModel(
            name='BangChiTietVungBienDanhBat',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('STT', models.IntegerField(default=1, help_text='Số thứ tự của các đỉnh đa giác tạo thành vùng biển')),
                ('ViDo', models.DecimalField(decimal_places=4, default=0, help_text='Vĩ độ của 1 đỉnh đa giác của vùng biển', max_digits=8)),
                ('KinhDo', models.DecimalField(decimal_places=4, default=0, help_text='Kinh độ của 1 đỉnh đa giác của vùng biển', max_digits=8)),
            ],
            options={
                'verbose_name_plural': 'Bảng chi tiết vùng biển đánh bắt',
            },
        ),
        migrations.CreateModel(
            name='BangChuTau',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDChuTau', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Mã định danh chủ tàu', unique=True)),
                ('HoTen', models.CharField(default='', help_text='Họ tên chủ tàu', max_length=255)),
                ('CMND_CCCD', models.CharField(default='', help_text='Chứng minh nhân dân chủ tàu', max_length=20)),
                ('NgaySinh', models.DateField(default=datetime.date(1900, 1, 1), help_text='Ngày tháng năm sinh chủ tàu', validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1900, 1, 1)), django.core.validators.MaxValueValidator(limit_value=datetime.date(2024, 3, 17))])),
                ('DiaChi', models.CharField(default='', help_text='Địa chỉ chủ tàu', max_length=255)),
                ('DienThoai', models.CharField(default='', help_text='Số điện thoại chủ tàu', max_length=20)),
                ('Fax', models.CharField(blank=True, help_text='Số Fax của chủ tàu', max_length=20, null=True)),
                ('Email', models.CharField(blank=True, help_text='Email của chủ tàu', max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Bảng chủ tàu',
            },
        ),
        migrations.CreateModel(
            name='BangDonViHanhChinhCapHuyen',
            fields=[
                ('MaHuyen', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('TenHuyen', models.CharField(blank=True, max_length=50, null=True)),
                ('TenHuyenEn', models.CharField(blank=True, max_length=50, null=True)),
                ('Cap', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Bảng đơn vị hành chính cấp huyện',
            },
        ),
        migrations.CreateModel(
            name='BangDonViHanhChinhCapTinh',
            fields=[
                ('MaTinh', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('TenTiengViet', models.CharField(blank=True, max_length=50, null=True)),
                ('TenVietTat', models.CharField(blank=True, max_length=6, null=True)),
                ('TenTiengAnh', models.CharField(blank=True, max_length=50, null=True)),
                ('Cap', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'verbose_name_plural': 'Bảng đơn vị hành chính cấp tỉnh',
            },
        ),
        migrations.CreateModel(
            name='BangLoaiCaDanhBat',
            fields=[
                ('IDLoaiCa', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaLoaiCa', models.CharField(default='', help_text='Mã định danh của loại cá', max_length=6, unique=True)),
                ('TenLoaiCa', models.CharField(default='', help_text='Tên loại cá', max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Bảng loại cá đánh bắt',
            },
        ),
        migrations.CreateModel(
            name='BangMaLoaiTau',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDLoaiTau', models.CharField(default='', max_length=8, unique=True)),
                ('TenLoaiTau', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Bảng mã loại tàu',
            },
        ),
        migrations.CreateModel(
            name='BangNganhNgheKhaiThac',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDNganhNghe', models.CharField(default='', help_text='Mã định danh của nghề theo quy định', max_length=5, unique=True)),
                ('Ten', models.CharField(default='', help_text='Tên nghề', max_length=128)),
                ('HoNghe', models.CharField(default='', help_text='Họ nghề', max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Bảng ngành nghề khai thác',
            },
        ),
        migrations.CreateModel(
            name='BangTau',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDTau', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Mã định danh tàu', unique=True)),
                ('SoDangKy', models.CharField(default='', help_text='Số đăng ký', max_length=15)),
                ('TenTau', models.CharField(default='', help_text='Tên tàu', max_length=128)),
                ('HoHieu', models.CharField(default='', help_text='Hô hiệu', max_length=128)),
                ('CoHieu', models.CharField(blank=True, help_text='Cờ hiệu', max_length=128, null=True)),
                ('IMO', models.CharField(default='', help_text='IMO - International Maritime Organization - Tổ chức hàng hải quốc tế', max_length=128)),
                ('NgayDangKy', models.DateField(default=datetime.date(1900, 1, 1), help_text='Ngày đăng ký', validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1900, 1, 1)), django.core.validators.MaxValueValidator(limit_value=datetime.date(2024, 3, 17))])),
                ('NgayHetHanDangKy', models.DateField(default=datetime.date(1900, 1, 1), help_text='Ngày hết hạn đăng ký')),
                ('TongTaiTrong', models.FloatField(default=0, help_text='Tổng trọng tải tàu')),
                ('ChieuDaiLonNhat', models.FloatField(default=0, help_text='Chiều dài tàu')),
                ('ChieuRongLonNhat', models.FloatField(default=0, help_text='Chiều rộng tàu')),
                ('CongSuatMay', models.FloatField(default=0, help_text='Công suất máy')),
                ('MonNuoc', models.FloatField(default=0, help_text='Mớn nước')),
                ('SoThuyenVien', models.IntegerField(default=0, help_text='Số thuyền viên')),
                ('NgaySanXuat', models.DateField(blank=True, help_text='Ngày sản xuất', null=True, validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1900, 1, 1)), django.core.validators.MaxValueValidator(limit_value=datetime.date(2024, 3, 17))])),
                ('NgayHetHan', models.DateField(blank=True, default=datetime.date(1900, 1, 1), help_text='Ngày hết hạn', null=True)),
                ('DungTichHamCa', models.FloatField(blank=True, help_text='Dung tích hầm cá', null=True)),
                ('VanTocDanhBat', models.FloatField(default=0, help_text='Vận tốc tàu chạy lúc đánh bắt')),
                ('VanTocHanhTrinh', models.FloatField(default=0, help_text='Vận tốc lớn nhất của tàu')),
                ('ThongSoNguCu', models.CharField(default='', help_text='Thông số ngư cụ', max_length=255)),
                ('CangCaDangKy', models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cangcadangky', to='core.bangcangca')),
                ('CangCaPhu', models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cangcadangky_2', to='core.bangcangca')),
                ('IDChuTau', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bangtau_chutau', to='core.bangchutau')),
            ],
            options={
                'verbose_name_plural': 'Bảng tàu',
            },
        ),
        migrations.CreateModel(
            name='BangThietBiNhatKyKhaiThac',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDThietBi', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Mã định danh thiết bị', unique=True)),
                ('SerialNumber', models.CharField(default='', help_text='Số serial của thiết bị', max_length=10)),
                ('NgaySanXuat', models.DateField(blank=True, help_text='Ngày sản xuất', null=True, validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1900, 1, 1)), django.core.validators.MaxValueValidator(limit_value=datetime.date(2024, 3, 17))])),
                ('FWVersion', models.CharField(default='', help_text='Version Firmware', max_length=10)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Bảng thiết bị nhật ký khai thác',
            },
        ),
        migrations.CreateModel(
            name='BangVungBienDanhBat',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDVungBien', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Mã định danh vùng biển', unique=True)),
                ('Ten', models.CharField(default='', help_text='Tên vùng biển', max_length=128)),
                ('Ma', models.CharField(default='', help_text='Mã vùng biển theo quy định', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Bảng vùng biển đánh bắt',
            },
        ),
        migrations.CreateModel(
            name='ToaDo',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ViDo', models.DecimalField(decimal_places=4, default=0, max_digits=8)),
                ('KinhDo', models.DecimalField(decimal_places=4, default=0, max_digits=8)),
                ('IDVungBien', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangchitietvungbiendanhbat')),
            ],
            options={
                'verbose_name_plural': 'Bảng tọa độ',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cangca', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangcangca')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BangViTriTau',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ViDo', models.DecimalField(decimal_places=6, default=0, max_digits=12)),
                ('KinhDo', models.DecimalField(decimal_places=6, default=0, max_digits=12)),
                ('Ngay', models.DateTimeField()),
                ('TocDo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('Huong', models.IntegerField(default=0)),
                ('IDTau', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangtau')),
            ],
            options={
                'verbose_name_plural': 'Bảng vị trí tàu',
            },
        ),
        migrations.CreateModel(
            name='BangThuyenTruong',
            fields=[
                ('ID', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDThuyenTruong', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Mã định danh chủ tàu', unique=True)),
                ('HoTen', models.CharField(default='', help_text='Họ tên thuyền trưởng', max_length=500)),
                ('CMND_CCCD', models.CharField(default='', help_text='Chứng minh nhân dân thuyền trưởng', max_length=20)),
                ('NgaySinh', models.DateField(default=datetime.date(1900, 1, 1), help_text='Ngày tháng năm sinh thuyền trưởng', validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1900, 1, 1)), django.core.validators.MaxValueValidator(limit_value=datetime.date(2024, 3, 17))])),
                ('DiaChi', models.CharField(default='', help_text='Địa chỉ thuyền trưởng', max_length=255)),
                ('DienThoai', models.CharField(default='', help_text='Số điện thoại thuyền trưởng', max_length=20)),
                ('Fax', models.CharField(blank=True, max_length=20, null=True)),
                ('Email', models.CharField(blank=True, max_length=100, null=True)),
                ('hasShip', models.BooleanField(default=False)),
                ('MaHuyen', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangdonvihanhchinhcaphuyen')),
            ],
            options={
                'verbose_name_plural': 'Bảng thuyền trưởng',
            },
        ),
        migrations.AddField(
            model_name='bangtau',
            name='IDDevice',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangthietbinhatkykhaithac'),
        ),
        migrations.AddField(
            model_name='bangtau',
            name='IDThuyenTruong',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangthuyentruong'),
        ),
        migrations.AddField(
            model_name='bangtau',
            name='IDTinh',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bang_tau_tinh', to='core.bangdonvihanhchinhcaptinh'),
        ),
        migrations.AddField(
            model_name='bangtau',
            name='LoaiTau',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangmaloaitau'),
        ),
        migrations.AddField(
            model_name='bangtau',
            name='NgheChinh',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nghechinh', to='core.bangnganhnghekhaithac'),
        ),
        migrations.AddField(
            model_name='bangtau',
            name='NghePhu1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nghephu_1', to='core.bangnganhnghekhaithac'),
        ),
        migrations.AddField(
            model_name='bangtau',
            name='NghePhu2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nghephu_2', to='core.bangnganhnghekhaithac'),
        ),
        migrations.AddField(
            model_name='bangtau',
            name='NoiDangKy',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangdonvihanhchinhcaptinh'),
        ),
        migrations.AddField(
            model_name='bangdonvihanhchinhcaphuyen',
            name='MaTinh',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangdonvihanhchinhcaptinh'),
        ),
        migrations.AddField(
            model_name='bangchutau',
            name='MaHuyen',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangdonvihanhchinhcaphuyen'),
        ),
        migrations.AddField(
            model_name='bangchitietvungbiendanhbat',
            name='IDVungBien',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangvungbiendanhbat'),
        ),
        migrations.AddField(
            model_name='bangcangca',
            name='IDTinh',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.bangdonvihanhchinhcaptinh'),
        ),
        migrations.CreateModel(
            name='AdminHod',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]