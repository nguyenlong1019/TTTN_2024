from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt 


@csrf_exempt
def login_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if username == 'admin':
                if password == '@Long1705':
                    return JsonResponse({
                        'message': 'Login successfully!', 
                        'passed': True, 
                        'username': 'Long02'
                    }, status=200)
                else:
                    return JsonResponse({
                        'message': 'Password is not correct!',
                        'passed': False,
                        'username': 'Anonymous'
                    }, staus=401) 
            else:
                return JsonResponse({
                    'message': 'Username does not exits!',
                    'passed': False,
                    'username': 'Anonymous'
                })
        except Exception as e:
            return JsonResponse({
                'message': 'Server error!',
                'passed': False,
                'username': 'Anonymous'
            })
    else:
        return JsonResponse({
            'message': 'Method not allowed!',
            'passed': False,
            'username': 'Anonymous'
        })

    
def test_api_mobile(request):
    return JsonResponse({
        'message': 'Hello World!',
        'status': 200
    }, status=200)


def ship_name_list(request):
    return JsonResponse({
        'message': 'Danh sách tàu cá',
        'status': 200,
        'data': [
            {
                'so_hieu_tau': 'KH-12235',
                'chu_tau': 'Nguyễn Văn Long'
            },
            {
                'so_hieu_tau': 'BĐ-12935',
                'chu_tau': 'Nguyễn Văn Long'
            },
            {
                'so_hieu_tau': 'HP-99999',
                'chu_tau': 'Nguyễn Văn Long'
            },
            {
                'so_hieu_tau': 'HN-29299',
                'chu_tau': 'Nguyễn Văn Long'
            },
        ]
    }, status=200)


def ship_realtime_location(request):
    now = datetime.now()
    formatted_date = now.strftime("%d %b, %Y %H:%M:%S")
    print(formatted_date)
    # 16.344088, 108.599521 [16.408051, 108.489041, 16.415336, 108.251537, 16.583879, 107.982372]
    # 13.811880, 109.594370 [13.658198, 109.478250, 13.509807, 109.674731, 13.100527, 109.479232]
    # 12.963734, 109.654796 [12.824108, 109.441995, 12.655258, 109.672265, 12.336105, 109.328733]
    # 11.457285, 109.207992 [11.636259, 109.196456, 11.819430, 109.472452, 11.992313, 109.358127]
    return JsonResponse({
        'message': 'Vị trí tàu cá hiện tại.',
        'status': 200,
        'ship_list': [
            {
                'so_hieu_tau': 'KH-12235',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '1705',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-123455',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 16.344088,
                    'lng': 108.599521,
                },
                'time': formatted_date,
            },
            {
                'so_hieu_tau': 'BĐ-12935',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '1777',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-129455',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 13.811880,
                    'lng': 109.594370,
                },
                'time': formatted_date,
            },
            {
                'so_hieu_tau': 'HP-99999',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '2000',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-129955',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 12.963734,
                    'lng': 109.654796,
                },
                'time': formatted_date,
            },
            {
                'so_hieu_tau': 'HN-29299',
                'thuyen_truong': 'Nguyễn Văn A',
                'chu_tau': 'Nguyễn Văn Long',
                'loai_thiet_bi': 'VSM',
                'ten_thiet_bi': 'VHK-S',
                'IMO': '1723',
                'ngay_dang_ky': '2017-01-01',
                'ngay_het_han_dang_ky': '2027-01-01',
                'so_kep_chi': 'VHK-123685',
                'ngay_niem_phong': '20/02/2006',
                'location': {
                    'lat': 11.457285,
                    'lng': 109.207992,
                },
                'time': formatted_date,
            },
        ],
    }, status=200) 


def ship_location_log(request):
    return JsonResponse({
        'message': 'Lịch sử vị trí tàu cá',
        'status': 200,
        'log': {
            'tc1': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'KH-12235',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '1705',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-123455',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 16.408051,
                        'lng': 108.489041,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 16.415336,
                        'lng': 108.251537,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 16.583879,
                        'lng': 107.982372,
                        'date': '29-11-2023',
                    },
                ]
            },


            'tc2': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'BĐ-12935',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '1777',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-129455',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 13.658198,
                        'lng': 109.478250,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 13.509807,
                        'lng': 109.674731,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 13.100527,
                        'lng': 109.479232,
                        'date': '29-11-2023',
                    },
                ]
            },


            'tc3': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'HP-99999',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '2000',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-129955',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 12.824108,
                        'lng': 109.441995,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 12.655258,
                        'lng': 109.672265,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 12.336105,
                        'lng': 109.328733,
                        'date': '29-11-2023',
                    },
                ]
            },


            'tc4': {
                'thong_tin_chung': {
                    'so_hieu_tau': 'HN-29299',
                    'thuyen_truong': 'Nguyễn Văn A',
                    'chu_tau': 'Nguyễn Văn Long',
                    'loai_thiet_bi': 'VSM',
                    'ten_thiet_bi': 'VHK-S',
                    'IMO': '1723',
                    'ngay_dang_ky': '2017-01-01',
                    'ngay_het_han_dang_ky': '2027-01-01',
                    'so_kep_chi': 'VHK-123685',
                    'ngay_niem_phong': '20/02/2006',
                },
                'journal': [
                    {
                        'lat': 11.636259,
                        'lng': 109.196456,
                        'date': '13-01-2024',
                    },
                    {
                        'lat': 11.819430,
                        'lng': 109.472452,
                        'date': '29-12-2023',
                    },
                    {
                        'lat': 11.992313,
                        'lng': 109.358127,
                        'date': '29-11-2023',
                    },
                ]
            },
        },  
    }, status=200)


def mining_log(request):
    return JsonResponse({
        'message': 'Nhật ký khai thác điện tử',
        'status': 200,
        'data': [
            {
                'so_hieu_tau': 'KH-12235',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
            {
                'so_hieu_tau': 'HN-29299',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá bơn',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá bơn',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá bò hoa vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá nục thuôn',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
            {
                'so_hieu_tau': 'HP-99999',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Hồng Lang',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Nóc Chóp',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
            {
                'so_hieu_tau': 'BĐ-12935',
                'danh_sach_chuyen_bien': [
                    {
                        'chuyen_bien_so': 1,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Ồ',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chấm',
                                        'khoi_luong': 5500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2310,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2550,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Vằn',
                                        'khoi_luong': 2000,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1025,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Vằn',
                                        'khoi_luong': 5010,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 2,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3200,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chấm',
                                        'khoi_luong': 1100,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chấm',
                                        'khoi_luong': 1400,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 5505,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2220,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1110,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá Ngừ Chù',
                                        'khoi_luong': 3300,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3490,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1235,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2305,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 3,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2300,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1450,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1255,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2315,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 3555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1055,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2015,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1545,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3455,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1035,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1450,
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        'chuyen_bien_so': 4,
                        'danh_sach_me_ca': [
                            {
                                'me_ca': 1,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 2150,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1050,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1500,
                                    },
                                ]
                            },
                            {
                                'me_ca': 2,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1250,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2350,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2555,
                                    },
                                ]
                            },
                            {
                                'me_ca': 3,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 2030,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 1540,
                                    },
                                ]
                            },
                            {
                                'me_ca': 4,
                                'du_lieu_me_ca': [
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây vàng',
                                        'khoi_luong': 3550,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá ngừ vây xanh',
                                        'khoi_luong': 1020,
                                    },
                                    {
                                        'ten_loai_ca': 'Cá thu',
                                        'khoi_luong': 2110,
                                    },
                                ]
                            },

                        ]
                    },
                ]
            },
        ]
    }, status=200)
    


# RESTful API
@login_required(login_url='/login/')
def get_location_view_api(request, pk):
    try:
        ship = BangTau.objects.get(pk=pk)
    except Exception as e:
        return JsonResponse({
            'status': 404,
            'message': 'Ship not Found!',
            'bundle': {}
        }, status=404)

    location = BangViTriTau.objects.filter(IDTau=ship).order_by('-Ngay')[0]
    return JsonResponse({
        'status': 200,
        'message': f'Get info of ship: {ship.SoDangKy} successfully!',
        'bundle': {
            'shipowner': ship.IDChuTau.HoTen,
            'captain': ship.IDThuyenTruong.HoTen,
            'lat': location.ViDo,
            'lng': location.KinhDo,
            'date': location.Ngay,
        }
    }, status=200)