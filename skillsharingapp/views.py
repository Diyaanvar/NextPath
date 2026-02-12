from django.shortcuts import render,HttpResponse,redirect
from .import models
from django.contrib import messages
from .models import Student,Institute,Course,Lesson,Skill

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        state = request.POST.get('State')
        district = request.POST.get('District')
        phone = request.POST.get('phone')
        dob = request.POST.get('DOB')
        image =request.FILES.get('image')

        if password != confirm_password:
            
            return HttpResponse("""
            <script>
                alert('Passwords do not match');
                window.history.back();
            </script>
            """)
        if models.Student.objects.filter(email=email).exists():
           return render(request, 'register.html', {
                'error': 'Email already exists'
            })
        else:
            user = models.Student(
                name=name,
                email=email,
                password=password,
                confirm_password=confirm_password,
                gender=gender,
                phone=phone,
                dob=dob,
                state=state,
                district=district,
                image=image,
            )
            user.save()
            return redirect('login')
       
    return render(request, 'register.html')


def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=models.Student.objects.get(email=email)
            if user.password == password:
                request.session['email']=email
                return redirect('home')
            else:
                return HttpResponse('Invalid password')
        except models.Student.DoesNotExist:
            return HttpResponse('Invalid user')
    return render(request,'login.html')

def home(request):
    if 'email' not in request.session:
        return redirect('login')
    return render(request,'home.html')

def profile(request):
    if 'email' in request.session:
        email=request.session['email']
        try:
            user=models.Student.objects.get(email=email)
            return render(request,'profile.html',{'user':user})
        except models.User.DoesNotExist:
            return HttpResponse("User not found")
    else:
        return redirect('login')          




def logout(request):
    request.session.flush()
    return redirect('index')                             


from django.shortcuts import render, redirect


def editprofile(request):
    if 'email' in request.session:
        email = request.session['email']
        user = Student.objects.get(email=email)

        if request.method == 'POST':
            # Update user fields
            user.name = request.POST.get('name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.gender = request.POST.get('gender')
            user.dob = request.POST.get('dob')
            user.state = request.POST.get('state')
            user.district = request.POST.get('district')

            # Update image if uploaded
            if 'image' in request.FILES:
                user.image = request.FILES['image']

            # Remove image if requested
            if 'remove_image' in request.POST and user.image:
                user.image = None

            user.save()
            return redirect('profile')

        return render(request, 'editprofile.html', {'user': user})
    
    return redirect('login')







def adminlogin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        adminusername="ADMIN"
        adminpassword="admin" 
        try:
            if adminusername==username:
                if adminpassword==password:
                    request.session['adminusername']=adminusername
                    return redirect('adminhome')
                else:
                    return redirect('adminlogin')
                
            else:
                return redirect('adminlogin')
            
        except models.User.DoesNotExist:
            return HttpResponse("Admin does not exist")
    else:
        return render(request,'adminlogin.html')

def adminhome(request):
    if 'adminusername'not in request.session:
        return redirect('adminlogin')
    return render(request,'adminhome.html')


def studentlist(request):
    students=models.Student.objects.all()
    return render(request,'studentlist.html',{'students':students})



def delete_student(request,id):
    students = models.Student.objects.get(id=id)
    students.delete()
    return redirect('studentlist')





from django.shortcuts import render, get_object_or_404


def course_detail(request, course_id):
    # This fetches the course with the specific ID or returns a 404 error if not found
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course_detail.html', {'course': course})

from .models import Course  # Make sure Course is imported at the top

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def test_base(request):
    return render(request, 'base.html')


from django.shortcuts import render, get_object_or_404, redirect




from django.shortcuts import render

# (Ensure you have @login_required decorators if needed)

def admin_course_list(request):
    # Fetch ALL courses from the database
    all_courses = Course.objects.all()
    return render(request, 'admin_course_list.html', {'courses': all_courses})



def institute_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        institute_type = request.POST.get('institute_type')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        certificate = request.FILES.get('certificate')

        # Validations
        if password != confirm_password:
            return render(request, 'institute/register.html', {
                'error': 'Passwords do not match'
            })
        
        if len(password) < 8:
            return render(request, 'institute/register.html', {
                'error': 'password have atleast 8 characters'
            })

        if Institute.objects.filter(email=email).exists():
            return render(request, 'institute/register.html', {
                'error': 'Email already registered'
            })

        Institute.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            institute_type=institute_type,
            password=password,
            registration_certificate=certificate,
            status='pending'
        )

        return redirect('institute_login')

    return render(request, 'institute/register.html')
def institute_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            institute = Institute.objects.get(email=email, password=password)

            if institute.status != 'approved':
                return render(request, 'institute/login.html', {
                    'error': 'Your account is not approved by admin'
                })

            request.session['institute_id'] = institute.id
            request.session['user_type'] = 'institute'
            return render(request,'institute/dashboard.html')

        except Institute.DoesNotExist:
            return render(request, 'institute/login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'institute/login.html')



from django.shortcuts import render, redirect, get_object_or_404
from .models import Institute

# Admin view to list all institutes
def institutes_list(request):
    # Optional: restrict access to admin only


    institutes = Institute.objects.all().order_by('-id')  # newest first
    return render(request, 'institutelist.html', {'institutes': institutes})




# Approve institute
def approve_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    institute.status = 'approved'
    institute.save()
    return redirect('institutes_list')

# Reject institute
def reject_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    institute.status = 'rejected'
    institute.save()
    return redirect('institutes_list')

# Delete institute
def delete_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    institute.delete()
    return redirect('institutes_list')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Lesson, Institute

# --- Institute adds a course ---
def institute_add_course(request):
    if 'institute_id' not in request.session:
        return redirect('institute_login')  # Must login first

    from .models import Institute, Course
    institute_id = request.session['institute_id']
    institute = get_object_or_404(Institute, id=institute_id, status='approved')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        skill_tag = request.POST.get('skill_tag')
        thumbnail = request.FILES.get('thumbnail')

        Course.objects.create(
            institute=institute,
            title=title,
            description=description,
            price=price,
            skill_tag=skill_tag,
            thumbnail=thumbnail
        )
        return render(request,'institute/dashboard.html')

    return render(request, 'add_course.html')



# --- Institute edits a course ---
def institute_edit_course(request, course_id):
    institute = get_object_or_404(Institute, email=request.session.get('email'))
    course = get_object_or_404(Course, id=course_id, institute=institute)

    if request.method == 'POST':
        course.title = request.POST['title']
        course.description = request.POST['description']
        course.price = request.POST['price']
        course.skill_tag = request.POST.get('skill_tag')
        if request.FILES.get('thumbnail'):
            course.thumbnail = request.FILES['thumbnail']
        course.save()
        return redirect('institute_courses')

    return render(request, 'institute/edit_course.html', {'course': course})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Institute, Course

def institute_courses(request):
    # Make sure the institute is logged in
    if 'institute_id' not in request.session:
        return redirect('institute_login')

    institute_id = request.session['institute_id']
    # Only show courses for this logged-in institute
    courses = Course.objects.filter(institute_id=institute_id).order_by('-id')

    return render(request, 'courses_list.html', {'courses': courses})



def institute_delete_course(request, course_id):
    if 'institute_id' not in request.session:
        return redirect('institute_login')

    institute_id = request.session['institute_id']
    course = get_object_or_404(Course, id=course_id, institute_id=institute_id)
    course.delete()
    return redirect('institute_courses')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson

def institute_lessons_list(request, course_id):
    # Make sure institute is logged in
    if 'institute_id' not in request.session:
        return redirect('institute_login')

    course = get_object_or_404(Course, id=course_id)
    
    # Only the owner institute can access
    if course.institute.id != request.session['institute_id']:
        return redirect('institute_courses')

    lessons = course.lessons.all().order_by('order')

    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES.get('video_file')
        order = request.POST.get('order') or (lessons.count() + 1)

        Lesson.objects.create(
            course=course,
            title=title,
            video_file=video_file,
            order=order
        )
        return redirect('institute_lessons_list', course_id=course.id)

    return render(request, 'institute/lessons_list.html', {
        'course': course,
        'lessons': lessons
    })
def institute_delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Ensure only the owner can delete
    if lesson.course.institute.id != request.session.get('institute_id'):
        return redirect('institute_courses')

    course_id = lesson.course.id
    lesson.delete()
    return redirect('institute_lessons_list', course_id=course_id)

from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout

# Logout View
def institute_logout(request):
    # Clear the session and logout
    auth_logout(request)
    return redirect('institute_login')  # Redirect to login page



from django.shortcuts import render, get_object_or_404
from .models import Course

# List all courses
def userlistcourses(request):
    courses = Course.objects.all()  # You can add filtering if needed
    return render(request, 'userlistcourses.html', {'courses': courses})

# Show course details
def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

# Enroll in course (You can handle the actual enrollment logic here)
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Implement enrollment logic here, for example, creating a UserCourse object or similar.
    return render(request, 'enroll_success.html', {'course': course})

# Skillsets entry page
# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student  # Import your Student model

def enter_skills(request):
    if request.method == 'POST':
        skillsets = request.POST.get('skillsets')  # Get the entered skillsets
        email = request.session.get('email')  # Assuming user is logged in and their email is stored in session

        try:
            student = Student.objects.get(email=email)  # Find the student using email from session
            student.skillsets = skillsets  # Save the entered skillsets to the model
            student.save()  # Save the student record
            return HttpResponse('Skills saved successfully!')  # Return a success message
        except Student.DoesNotExist:
            return HttpResponse('User does not exist.', status=404)
    return render(request, 'userskillentry.html')  # Render the form template



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Recommend courses based on skillsets
def recommend_courses(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    student = Student.objects.get(email=email)
    courses = Course.objects.all()

    if not student.skillsets:
        return render(request, 'recommend_courses.html', {'courses': courses})

    # Prepare data for TF-IDF
    student_skills = student.skillsets
    course_skills = [course.skill_tag for course in courses]

    # TF-IDF vectorization
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(course_skills + [student_skills])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(vectors[-1], vectors[:-1])
    similarity_scores = cosine_sim.flatten()

    # Sort courses by similarity
    recommended_courses = [courses[i] for i in similarity_scores.argsort()[::-1]]

    return render(request, 'recommend_courses.html', {'courses': recommended_courses})



#user side course detail page 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course

def user_lessons_list(request, course_id):
    

    course = get_object_or_404(Course, id=course_id)

    lessons = course.lessons.all().order_by('order')

    

    return render(request, 'user_lessons_list.html', {
        'course': course,
        'lessons': lessons
    })




#chatbot 
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

def chatbot(request):
    if request.method == 'GET':
        return render(request, 'chatbot.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            payload = {
                "model": getattr(settings, "GROQ_MODEL2"),
                "messages": [
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.2,
                "max_tokens": 200
            }

            headers = {
                "Authorization": f"Bearer {getattr(settings, 'GROQ_API_KEY2')}",
                "Content-Type": "application/json"
            }

            resp = requests.post(getattr(settings,"GROQ_API_URL2"), 
                                 headers=headers, json=payload, timeout=60)

            resp_json = resp.json()

            reply = resp_json["choices"][0]["message"]["content"].strip()

            return JsonResponse({"response": reply})

        except Exception as e:
            return JsonResponse({"response": f"Error: {str(e)}"})

    return JsonResponse({'response': 'Invalid request method'}, status=405)



#payment
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, CoursePayment, Student

def course_payment(request, course_id):
    if 'email' not in request.session:
        return redirect('login')

    student = Student.objects.get(email=request.session['email'])
    course = get_object_or_404(Course, id=course_id)

    amount = float(course.price)
    amount_paise = int(amount * 100)

    client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
    )

    razorpay_order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1
    })

    CoursePayment.objects.create(
        student=student,
        course=course,
        amount=amount,
        razorpay_order_id=razorpay_order['id']
    )

    context = {
        'course': course,
        'student': student,
        'amount': amount,
        'razorpay_key': settings.RAZOR_KEY_ID,
        'order_id': razorpay_order['id']
    }

    return render(request, 'razorpay_checkout.html', context)





def payment_success(request):
    if 'email' not in request.session:
        return redirect('login')

    order_id = request.GET.get('razorpay_order_id')

    payment = CoursePayment.objects.get(
        razorpay_order_id=order_id
    )
    payment.status = 'Payment Success'
    payment.save()

    return render(request, 'paymentsuccess.html', {
        'payment': payment
    })
