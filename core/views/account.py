from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 

from core.models import * 

from django.contrib.auth import get_user_model 
from django.contrib.auth.hashers import make_password
from django.db.models import Q 
from django.contrib import messages 
from django.core.paginator import Paginator


@login_required(login_url='/login/')
def account_view(request):
    if request.user.user_type == '1' or request.user.is_staff:
        titles = ["STT", "Tên tài khoản", "Cấp độ tài khoản", "Tình trạng", "Loại tài khoản", "Địa chỉ", "Email", "Số điện thoại", "Thao tác"]
        UserModel = get_user_model()
        items = UserModel.objects.all().order_by('username').exclude(username='admin')
        
        items_per_page = 6 
        p = Paginator(items, items_per_page)
        page = request.GET.get('page')
        items = p.get_page(page)
        current = items.number
        start = max(current - 2, 1)
        end = min(current + 2, items.paginator.num_pages)
        page_range = range(start, end)
        start_number = (current - 1) * items_per_page
        return render(request, 'core/account.html', {
            'titles': titles,
            'items': items,
            'start': start, 
            'end': end, 
            'page_range': page_range,
            'start_number': start_number
        }, status=200)
    else:
        return render(request, '403.html', {}, status=403)


@login_required(login_url='/login/')
def add_new_account_view(request):
    if request.user.user_type == '1' or request.user.is_staff:
        if request.method == 'POST':
            UserModel = get_user_model()
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')

            username = request.POST.get('username')
            # check username xem đã tồn tại hay chưa?
            if UserModel.objects.filter(username=username).exists():
                messages.info(request, f"Tên người dùng '{username}' đã tồn tại")
                return redirect('add-account')
            email = request.POST.get('email')
            # check email đã tồn tại hay chưa?
            if email != '':
                if UserModel.objects.filter(email=email).exists():
                    messages.info(request, f"Email '{email}' đã tồn tại")
                    return redirect('add-account')

            password = request.POST.get('password')
            userType = request.POST.get('levelManager')
            # print(userType)
            hash_password = make_password(password)
            user = CustomUser.objects.create(
                username=username, 
                password=hash_password,
                user_type=userType
            )
            if first_name != '':
                user.first_name = first_name
            if last_name != '':
                user.last_name = last_name 
            if email != '':
                user.email = email

            # print(user.user_type, type(user.user_type))
            # Admin thêm is_staff bằng True
            if user.user_type == '1':
                # print("TEST 1")
                user.is_staff = True
                user.save() 

            # Quản lý cảng thêm phần cảng
            if user.user_type == '2':
                # print("TEST")
                pk = request.POST.get('tenCangCa')
                print(pk)
                try:
                    gateName = BangCangCa.objects.get(pk=pk)
                except BangCangCa.DoesNotExist:
                    messages.error(request, f"Lỗi không tìm thấy thông tin")
                    return redirect('account-view')
                
                staff = Staff.objects.create(admin=user)
                staff.cangca = gateName
                staff.save()
                user.save()
                # print(user.staff.cangca)


            # Quản lý thiết bị
            if user.user_type == '3':
                user.save()

            messages.success(request, "Tạo user thành công!")
            return redirect('account-view')     
        else:
            gate_list = BangCangCa.objects.all().order_by('Ten')
            return render(request, 'core/add-new-account.html', {'gate_list': gate_list}, status=200) 
    else:
        return render(request, '403.html', {}, status=403)


@login_required(login_url='/login/')
def delete_account_view(request, pk):
    if request.user.user_type == '1' or request.user.is_staff:
        try:
            UserModel = get_user_model()
            user = UserModel.objects.get(pk=pk)
            user.delete()

            messages.success(request, f"Xóa user thành công!!")
            return redirect('account-view')
        except UserModel.DoesNotExist:
            messages.error(request, f"User với id = '{pk}' không tồn tại!!")
            return redirect('account-view')
    else:
        return render(request, '403.html', {}, status=403) 


@login_required(login_url='/login/')
def edit_account_view(request, pk):
    if request.user.user_type == '1' or request.user.is_staff:
        if request.method == 'POST':
            UserModel = get_user_model()
            username = request.POST.get('username')
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            password = request.POST.get('password')
            email = request.POST.get('email')

            # level_manager = request.POST.get('levelManager') 
            try:
                user = UserModel.objects.get(pk=pk)
                if username != user.username:
                    # check username đã tồn tại hay chưa
                    if UserModel.objects.filter(username=username).exists():
                        messages.info(request, f'Username: {username} đã tồn tại!')
                        return redirect('edit-account', pk)
                    else:
                        user.username = username
                if first_name != '':
                    user.first_name = first_name 
                if last_name != '':
                    user.last_name = last_name 
                if email != '' and email != user.email:
                    if UserModel.objects.filter(email=email).exists():
                        messages.info(request, f"Email '{email}' đã tồn tại")
                        return redirect('edit-account', pk)
                    else:
                        user.email = email 
                
                if password:
                    user.set_password(password)
                user.save()
                messages.success(request, 'Cập nhật thông tin người dùng thành công!')
                return redirect('account-view')
            except UserModel.DoesNotExist:
                messages.error(request, "Người dùng không tồn tại")
                return redirect('account-view')        
        try:
            user = get_user_model().objects.get(pk=pk)
        except Exception as e:
            messages.error(request, f"Không tìm thấy thông tin user với id = '{pk}'")
            return redirect('index')
        gate = None 
        if user.user_type == '2':
            gate = user.staff.cangca.Ten 
        # print(gate)
        gate_list = BangCangCa.objects.all().order_by('Ten')

        return render(request, 'core/edit-account.html', {'gate_list': gate_list, 'user': user, 'gate': gate}, status=200)
    else:
        return render(request, '403.html', {}, status=403)


@login_required(login_url='/login/')
def search_account_view(request):
    if request.user.user_type == '1' or request.user.is_staff:
        query = request.GET.get('q')
        query_type = request.GET.get('query-type') 
        titles = ["STT", "Tên tài khoản", "Cấp độ tài khoản", "Tình trạng", "Loại tài khoản", "Địa chỉ", "Email", "Số điện thoại", "Thao tác"]

        UserModel = get_user_model()
        # fields = UserModel._meta.fields  # id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, user_type
        # for field in fields:
        #     print(field.name)
        
        if query_type == '1':
            # nhà cung cấp thiết bị: lv3
            items = UserModel.objects.filter((Q(user_type = '3') & Q(username__icontains=query)) | (Q(user_type = '3') & Q(first_name__icontains=query)) | (Q(user_type = '3') & Q(last_name__icontains=query)) | (Q(user_type = '3') & Q(email__icontains=query))).order_by('username').exclude(username='admin')
            if len(items) == 0:
                messages.info(request, f"Không tìm thấy user level 3 với query = '{query}'")
        elif query_type == '2':
            # quản lý cảng: lv2
            items = UserModel.objects.filter((Q(user_type = '2') & Q(username__icontains=query)) | (Q(user_type = '2') & Q(first_name__icontains=query)) | (Q(user_type = '2') & Q(last_name__icontains=query)) | (Q(user_type = '2') & Q(email__icontains=query))).order_by('username').exclude(username='admin')
            if len(items) == 0:
                messages.info(request, f"Không tìm thấy user level 2 với query = '{query}'") 
        elif query_type == '3':
            # chi cục thủy sản: lv1
            items = UserModel.objects.filter((Q(user_type = '1') & Q(username__icontains=query)) | (Q(user_type = '1') & Q(first_name__icontains=query)) | (Q(user_type = '1') & Q(last_name__icontains=query)) | (Q(user_type = '1') & Q(email__icontains=query))).order_by('username').exclude(username='admin')
            if len(items) == 0:
                messages.info(request, f"Không tìm thấy user level 1 với query = '{query}'") 
        elif query_type == '4':
            items = UserModel.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query)).order_by('username').exclude(username='admin')
            if len(items) == 0:
                messages.info(request, f"Không tìm thấy user với query = '{query}'")     
        else:
            items = UserModel.objects.all().order_by('username').exclude(username='admin')
        
        items_per_page = 6 
        p = Paginator(items, items_per_page)
        page = request.GET.get('page')
        items = p.get_page(page)
        current = items.number
        start = max(current - 2, 1)
        end = min(current + 2, items.paginator.num_pages)
        page_range = range(start, end)
        start_number = (current - 1) * items_per_page
        return render(request, 'core/account.html', {
            'titles': titles,
            'items': items,
            'start': start, 
            'end': end, 
            'page_range': page_range,
            'start_number': start_number
        }, status=200)
    else:
        return render(request, '403.html', {}, status=403)
