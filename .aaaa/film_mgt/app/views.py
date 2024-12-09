from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Employee
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Movie, Partner
import json

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
            template_name = 'partners.html'
        case _:
            template_name = 'default.html'
    template = loader.get_template(template_name)
    return HttpResponse(template.render({'user': acc}))
    
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def login_view(request):
    return render(request, 'login.html') 

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
            movie.save()

            return JsonResponse({'message': 'Thông tin phim đã được cập nhật thành công!'}, status=200)

        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Phim không tồn tại!'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ!'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ!'}, status=405)