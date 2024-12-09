from django.db import models

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)  
    full_name = models.CharField(max_length=255)  
    email = models.EmailField(max_length=255, unique=True)  
    password = models.CharField(max_length=255)  
    role = models.CharField(
        max_length=50,
        choices=[
            ('Khai thác phim', 'Khai thác phim'),
            ('Dịch phim', 'Dịch phim'), 
            ('Phát hành phim', 'Phát hành phim'),
            ('Quản lý', 'Quản lý'),
             ('Quản lý khách hàng', 'Quản lý khách hàng')
        ],
    ) 

class Partner(models.Model):
    partner_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(
        max_length=50,
        choices=[
            ('Khách hàng', 'Khách hàng'),
        ],
    )
  
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
class Release(models.Model):
    release_id = models.AutoField(primary_key=True)  
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    release_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[('Chưa phát hành', 'Chưa phát hành'), 
                 ('Đang phát hành', 'Đang phát hành'), 
                 ('Đã phát hành', 'Đã phát hành')]
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
class Translation(models.Model):
    translation_id = models.AutoField(primary_key=True)  
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    translated_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[('Chưa hoàn thành', 'Chưa hoàn thành'),
                 ('Đang dịch', 'Đang dịch'),
                 ('Hoàn thành', 'Hoàn thành')]
    )

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)  
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    
  
