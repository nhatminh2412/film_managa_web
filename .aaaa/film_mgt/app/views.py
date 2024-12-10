from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Employee
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Movie, Partner,Translation,Release,Order
import json
from datetime import datetime

def authorize(request):
    acc = None
    try:    
        acc = Employee.objects.get(email=request.GET.get('email', ''), password=request.GET.get('password', ''))    
    except Employee.DoesNotExist:
        try:
            acc = Partner.objects.get(email=request.GET.get('email', ''), password=request.GET.get('password', ''))
        except Partner.DoesNotExist:
            acc = None
    if not acc:
        return HttpResponse("không có tài khoản")
    
    role = acc.role  
    match role:
        case 'Khai thác phim':
            template_name = 'employee_mine.html'
        case 'Dịch phim':
            template_name = 'employee_trans.html'
        case 'Phát hành phim':
            template_name = 'employee_release.html'
        case 'Quản lý':
            template_name = 'employee_management.html'
        case 'Khách hàng':
            template_name = 'form_partner.html'
        case 'Quản lý khách hàng':
            template_name = 'manager_partner.html'
        case _:
            template_name = 'default.html'
    template = loader.get_template(template_name)
    return HttpResponse(template.render({'user': acc}))
    
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def login_view(request):
    return render(request, 'login.html') 

def parteners_view(request):
    return render(request,'partners.html')

def statics_view(request):
    return render(request,'statics.html')
def orderpartner_view(request):
    return render(request,'view_order.html')

def get_employee(request):
    employees = Employee.objects.all()
    data = [
        {
            "employee_id": emp.employee_id,
            "full_name": emp.full_name,
            "email": emp.email,
            "role": emp.role,
        }
        for emp in employees
    ]
    return JsonResponse(data, safe=False)


def add_employee(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if Employee.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'Email đã tồn tại!'}, status=400)

            new_employee = Employee.objects.create(
                full_name=data['full_name'],
                email=data['email'],
                role=data['role'],
                password=data['password'],
            )
            return JsonResponse({'message': 'Nhân viên đã được thêm thành công!', 'employee_id': new_employee.employee_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def delete_employee(request, employee_id):
    print(f"Request method: {request.method}")  # In ra phương thức của yêu cầu
    if request.method == 'DELETE':  # Kiểm tra phương thức DELETE
        try:
            employee = Employee.objects.get(pk=employee_id)
            employee.delete()
            return JsonResponse({'message': 'Nhân viên đã được xóa thành công!'})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Nhân viên không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def edit_employee(request, employee_id):
    if request.method == 'PUT':  # Xử lý yêu cầu PUT trực tiếp
        try:
            data = json.loads(request.body)
            employee = Employee.objects.get(pk=employee_id)
            employee.full_name = data.get('full_name', employee.full_name)
            employee.email = data.get('email', employee.email)
            employee.role = data.get('role', employee.role)
            employee.password = data.get('password', employee.password)
            employee.save()
            return JsonResponse({'message': 'Thông tin nhân viên đã được cập nhật thành công!'})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Nhân viên không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def get_movies(request):
    movies = Movie.objects.all()
    data = [
        {
            "movie_id": mv.movie_id,
            "title": mv.title,
            "release_year": mv.release_year,
            "genre": mv.genre,
            "description": mv.description,
            "price": mv.price,
        }
        for mv in movies
    ]
    return JsonResponse(data, safe=False)

def add_movie(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_movie = Movie.objects.create(
                title=data['title'],
                release_year=data['release_year'],
                genre=data.get('genre', ''),
                description=data.get('description', ''),
                price=data.get('price', 0.0),
            )
            return JsonResponse({'message': 'Phim đã được thêm thành công!', 'movie_id': new_movie.movie_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)

def delete_movie(request, movie_id):
    if request.method == 'DELETE':
        try:
            movie = Movie.objects.get(pk=movie_id)
            movie.delete()
            return JsonResponse({'message': 'Phim đã được xóa thành công!'})
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)

def edit_movie(request, movie_id):
    if request.method == 'PUT':
        try:
            # Lấy dữ liệu từ request
            data = json.loads(request.body)

            # Tìm phim dựa vào ID
            movie = Movie.objects.get(pk=movie_id)

            # Cập nhật thông tin phim
            movie.title = data.get('title', movie.title)
            movie.release_year = data.get('release_year', movie.release_year)
            movie.genre = data.get('genre', movie.genre)
            movie.description = data.get('description', movie.description)
            movie.price = data.get('price', movie.price) 
            movie.save()

            return JsonResponse({'message': 'Thông tin phim đã được cập nhật thành công!'}, status=200)

        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ!'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)



def get_translations(request):
    translations = Translation.objects.select_related('movie', 'translated_by').all()
    data = [
        {
            "translation_id": t.translation_id,
            "movie_title": t.movie.title,
            "language": t.language,
            "translator_name": t.translated_by.full_name,
            "status": t.status,
        }
        for t in translations
    ]
    return JsonResponse(data, safe=False)


def add_translation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            movie = Movie.objects.get(pk=data['movie_id'])
            translator = Employee.objects.get(pk=data['translator_id'])

            new_translation = Translation.objects.create(
                movie=movie,
                language=data['language'],
                translated_by=translator,
                status=data['status'],
            )
            return JsonResponse({'message': 'Bản dịch đã được thêm thành công!', 'translation_id': new_translation.translation_id})

        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Người dịch không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def delete_translation(request, translation_id):
    if request.method == 'DELETE':
        try:
            translation = Translation.objects.get(pk=translation_id)
            translation.delete()
            return JsonResponse({'message': 'Bản dịch đã được xóa thành công!'})

        except Translation.DoesNotExist:
            return JsonResponse({'error': 'Bản dịch không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def edit_translation(request, translation_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            translation = Translation.objects.get(pk=translation_id)

            if 'movie_id' in data:
                translation.movie = Movie.objects.get(pk=data['movie_id'])
            if 'language' in data:
                translation.language = data['language']
            if 'translator_id' in data:
                translation.translated_by = Employee.objects.get(pk=data['translator_id'])
            if 'status' in data:
                translation.status = data['status']

            translation.save()
            return JsonResponse({'message': 'Thông tin bản dịch đã được cập nhật thành công!'})

        except Translation.DoesNotExist:
            return JsonResponse({'error': 'Bản dịch không tồn tại!'}, status=404)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Người dịch không tồn tại!'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ!'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)



def get_releases(request):
    releases = Release.objects.select_related('movie', 'employee').all()
    data = [
        {
            "release_id": r.release_id,
            "movie_title": r.movie.title,
            "release_date": r.release_date,
            "status": r.status,
            "employee_name": r.employee.full_name,
        }
        for r in releases
    ]
    return JsonResponse(data, safe=False)



def add_release(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            movie = Movie.objects.get(pk=data['movie_id'])
            employee = Employee.objects.get(pk=data['employee_id'])

            new_release = Release.objects.create(
                movie=movie,
                release_date=data['release_date'],
                status=data['status'],
                employee=employee,
            )
            return JsonResponse({'message': 'Phát hành đã được thêm thành công!', 'release_id': new_release.release_id})

        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Nhân viên không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)



def delete_release(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            release_ids = data.get('release_ids', [])
            releases = Release.objects.filter(release_id__in=release_ids)

            if releases.exists():
                releases.delete()
                return JsonResponse({'message': 'Các bản phát hành đã được xóa thành công!'})
            else:
                return JsonResponse({'error': 'Không có bản phát hành nào để xóa!'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)



def edit_release(request, release_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            release = Release.objects.get(pk=release_id)

            if 'movie_id' in data:
                release.movie = Movie.objects.get(pk=data['movie_id'])
            if 'release_date' in data:
                release.release_date = data['release_date']
            if 'status' in data:
                release.status = data['status']
            if 'employee_id' in data:
                release.employee = Employee.objects.get(pk=data['employee_id'])

            release.save()
            return JsonResponse({'message': 'Thông tin phát hành đã được cập nhật thành công!'})

        except Release.DoesNotExist:
            return JsonResponse({'error': 'Phát hành không tồn tại!'}, status=404)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Nhân viên không tồn tại!'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ!'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)



def get_partners(request):
    try:
        partners = Partner.objects.all()
        data = [
            {
                "partner_id": partner.partner_id,
                "full_name": partner.full_name,
                "email": partner.email,
                "phone": partner.phone,
                "address": partner.address,
                "role": partner.role,
            }
            for partner in partners
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def add_partner(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data['full_name']
            email = data['email']
            password = data['password']
            phone = data.get('phone', '')
            address = data.get('address', '')
            
            new_partner = Partner.objects.create(
                full_name=full_name,
                email=email,
                password=password,
                phone=phone,
                address=address,
                role='Khách hàng'
            )
            
            return JsonResponse({'message': 'Khách hàng đã được thêm thành công!', 'partner_id': new_partner.partner_id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def edit_partner(request, partner_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            partner = Partner.objects.get(partner_id=partner_id)
            
            partner.full_name = data.get('full_name', partner.full_name)
            partner.email = data.get('email', partner.email)
            partner.password = data.get('password', partner.password)
            partner.phone = data.get('phone', partner.phone)
            partner.address = data.get('address', partner.address)
            partner.save()

            return JsonResponse({'message': 'Thông tin khách hàng đã được cập nhật thành công!'})
        
        except Partner.DoesNotExist:
            return JsonResponse({'error': 'Khách hàng không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def delete_partner(request, partner_id):
    if request.method == 'DELETE':
        try:
            partner = Partner.objects.get(partner_id=partner_id)
            partner.delete()
            return JsonResponse({'message': 'Khách hàng đã được xóa thành công!'})
        
        except Partner.DoesNotExist:
            return JsonResponse({'error': 'Khách hàng không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def get_partner(request, partner_id):
    try:
        partner = Partner.objects.get(pk=partner_id)
        return JsonResponse({'full_name': partner.full_name})
    except Partner.DoesNotExist:
        return JsonResponse({'error': 'Partner not found'}, status=404)
    

def get_orders(request):
    try:
        partner_id = request.GET.get('partnerId')
        if partner_id:
            orders = Order.objects.filter(partner__partner_id=partner_id).select_related('movie').all()
            data = [
                {
                    "order_id": order.order_id,
                    "movie_title": order.movie.title,
                    "order_date": order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for order in orders
            ]
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'partnerId is required'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def add_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Đọc dữ liệu JSON từ body
            partner_name = data.get('partner_name')  # Lấy partner_name thay vì partner_id
            movie_id = data.get('movie_id')
            order_date = data.get('order_date')

            # Chuyển đổi order_date từ chuỗi thành datetime
            order_date = datetime.strptime(order_date, '%Y-%m-%dT%H:%M')

            if not partner_name or not movie_id or not order_date:
                return JsonResponse({'error': 'Thiếu thông tin để tạo đơn đặt phim'}, status=400)

            # Lấy partner từ partner_name thay vì partner_id
            try:
                partner = Partner.objects.get(name=partner_name)
            except Partner.DoesNotExist:
                return JsonResponse({'error': 'Đối tác không tồn tại!'}, status=404)

            # Kiểm tra movie
            try:
                movie = Movie.objects.get(pk=movie_id)
            except Movie.DoesNotExist:
                return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)

            # Lấy giá trị movie_price từ Movie
            movie_price = movie.price if movie else 0.0

            # Tạo đơn đặt phim
            new_order = Order.objects.create(
                partner=partner,
                movie=movie,
                order_date=order_date,
                movie_price=movie_price
            )

            return JsonResponse({
                'message': 'Đơn đặt phim đã được thêm thành công!',
                'order_id': new_order.order_id,
                'order_date': new_order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                'movie_price': new_order.movie_price
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)



def delete_order(request, order_id):
    if request.method == 'DELETE':
        try:
            order = Order.objects.get(order_id=order_id)
            order.delete()
            return JsonResponse({'message': 'Đơn đặt phim đã được xóa thành công!'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Đơn đặt phim không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def edit_order(request, order_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            order = Order.objects.get(order_id=order_id)

            # Cập nhật thông tin đơn đặt phim
            if 'movie_id' in data:
                movie = Movie.objects.get(pk=data['movie_id'])
                order.movie = movie

            # Cập nhật giá trị movie_price (nếu có)
            if 'movie_price' in data:
                order.movie_price = data['movie_price']

            order.save()

            return JsonResponse({'message': 'Thông tin đơn đặt phim đã được cập nhật thành công!'})

        except Order.DoesNotExist:
            return JsonResponse({'error': 'Đơn đặt phim không tồn tại!'}, status=404)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ!'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)


def get_customer_info(request):
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({
            'customer': {
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.profile.phone,
                'password': user.password,  # Nếu muốn trả về mật khẩu, nhưng cần xử lý bảo mật tốt
            }
        })
    else:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    from django.shortcuts import render
from .models import Order

def order_statistics(request):
    # Lấy tất cả các đơn đặt hàng
    orders = Order.objects.select_related('movie', 'partner').all()
    
    # Tính tổng số tiền của các đơn đặt hàng
    total_revenue = sum(order.movie_price for order in orders)

    return render(request, 'order_statistics.html', {
        'orders': orders,
        'total_revenue': total_revenue,
    })

def partner_orders(request, partner_id):
    # Lấy tất cả các đơn đặt hàng của một khách hàng theo partner_id
    orders = Order.objects.filter(partner_id=partner_id).select_related('movie')

    return render(request, 'partner_orders.html', {
        'orders': orders,
    })