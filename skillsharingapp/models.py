from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    password=models.CharField(max_length=50,null=True,blank=True)
    confirm_password=models.CharField(max_length=50,null=True,blank=True)
    GENDER_CHOICES = [
        ('M','male'),
        ('F','female'),
    ]
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES,null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    dob=models.DateField(auto_now_add=True,null=True,blank=True)
    skillsets = models.TextField(blank=True, null=True)
    image=models.FileField(upload_to='images/',null=True,blank=True)
    STATE_CHOICES=[
        ('K','KERALA'),
        ('J&K','JAMMU&KASHMIR'),
        ('P','PUNJAB'),
    ]
    state=models.CharField(max_length=3,choices=STATE_CHOICES,null=True,blank=True)
    DISTRICT_CHOICES=[
        ('T','THIRUVANANTHAPURAM'),
        ('K','KOLLAM'),
        ('P','PATHANAMTHITTA'),
        ('A','ALAPPUZHA'),
        ('K','KOTTAYAM'),
        ('I','IDUKKI'),
        ('E','ERANAMKULAM'),
        ('TH','THRISSUR'),
        ('P','PALAKKAD'),
        ('M','MALAPPURAM'),
        ('KH','KOZHIKODE'),
        ('W','WAYANAD'),
        ('KA','KANNUR'),
        ('KS','KASARGOD'),
     ]
    district=models.CharField(max_length=5,choices=DISTRICT_CHOICES,null=True,blank=True)
 

from django.db import models

# Create your models here.







from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)          
    description = models.TextField(blank=True)       
    icon = models.CharField(max_length=50, default='star')  
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name

    





    

    
    
from django.db import models

class Institute(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    INSTITUTE_TYPE_CHOICES = (
        ('it_training', 'IT Training'),
        ('arts_science', 'Arts & Science College'),
        ('polytechnic', 'Polytechnic'),
        ('skill_training', 'Skill Training'),
        ('coaching', 'Coaching Center'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    institute_type = models.CharField(
        max_length=50,
        choices=INSTITUTE_TYPE_CHOICES
    )

    registration_certificate = models.FileField(upload_to='certificates/')

    password = models.CharField(max_length=100)  # plain text (as requested)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Course(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    skill_tag = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='course_videos/', null=True, blank=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.title








class CoursePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        default='Pending'
    )
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.title}"
