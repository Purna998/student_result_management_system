from urllib.parse import _ResultMixinBytes
from django.db.models.fields import return_None
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    notices=Notice.objects.all().order_by('-id')
    return render(request,'index.html',locals())

def notice_detail(request,notice_id):
    notice=Notice.objects.get(id=notice_id)   #or get_object_or_404(Notice,id=notice_id)
    return render(request,'notice_detail.html',locals())


@csrf_exempt
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error=None
    if request.method=='POST':
        username=request.POST.get('username') # it store as dictionary in KEY form
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('admin_dashboard')
        else:
            error="Invalid Credentials or not authorized."

    return render(request,'admin_login.html',locals()) 

@csrf_exempt
def admin_dashboard(request):
    if not request.user.is_authenticated:        # if session not exitst, it will redirect to login page to prevent direct access to dashboard
        return redirect('admin_login')
    else:
        classes=Class.objects.all()
        subjects=Subject.objects.all()
        students=Student.objects.all()
        results=Result.objects.all()

        total_students=students.count()
        total_results=results.values('student').distinct().count()
        total_classes=classes.count()
        total_subjects=subjects.count()

        
    return render(request,'admin_dashboard.html',locals())

def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required                 # to prevent direct access to create_class page through URL
def create_class(request):
    if request.method=='POST':
        try:
            class_name=request.POST.get('classname')
            class_numeric=request.POST.get('classnamenumeric')
            section=request.POST.get('section')
            Class.objects.create(class_name=class_name,class_numeric=class_numeric,section=section)
            messages.success(request,"Class Created Successfully")
            return redirect('create_class')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            pass

    return render(request,'create_class.html')

from django.shortcuts import get_object_or_404

def manage_classes(request):
    classes=Class.objects.all()
    if request.GET.get('delete'):
        try:
            class_id=request.GET.get('delete')
            class_obj=get_object_or_404(Class,id=class_id) #we can write pk instead of id as parameter
            class_obj.delete()
            messages.success(request,"Class Deleted Successfully")
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('manage_classes')
    return render(request,'manage_classes.html',locals()) 

def edit_class(request,class_id):
    class_obj=get_object_or_404(Class,id=class_id)
    if request.method=='POST':
        class_name=request.POST.get('classname')
        class_numeric=request.POST.get('classnamenumeric')
        section=request.POST.get('section')
        try:
            Class.objects.update(class_name=class_name,class_numeric=class_numeric,section=section)
            messages.success(request,"Class Updated Successfully")
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            pass

    return render(request,'edit_class.html',locals())

@login_required                 # to prevent direct access to create_class page through URL
def create_subject(request):
    if request.method=='POST':
        try:
            subjectname=request.POST.get('subjectname')
            subjectcode=request.POST.get('subjectcode')
            Subject.objects.create(subject_name=subjectname,subject_code=subjectcode)
            messages.success(request,"Subject Added Successfully")
            return redirect('create_subject')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            pass

    return render(request,'create_subject.html')

@login_required
def manage_subjects(request):
    subjects=Subject.objects.all()
    if request.GET.get('delete'):
        try:
            subject_id=request.GET.get('delete')
            subject_obj=get_object_or_404(Subject,id=subject_id) #we can write pk instead of id as parameter
            subject_obj.delete()
            messages.success(request,"Subject Deleted Successfully")
            return redirect('manage_subjects')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('manage_subjects')
    return render(request,'manage_subjects.html',locals()) 

def edit_subject(request,subject_id):
    subject_obj=get_object_or_404(Subject,id=subject_id)
    if request.method=='POST':
        subject_name=request.POST.get('subjectname')
        subject_code=request.POST.get('subjectcode')
        try:
            Subject.objects.update(subject_name=subject_name,subject_code=subject_code)
            subject_obj.save()
            messages.success(request,"Subject Updated Successfully")
            return redirect('manage_subjects')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            pass

    return render(request,'edit_subject.html',locals())

@login_required                 # to prevent direct access to create_class page through URL
def add_subject_combination(request):
    classes=Class.objects.all()
    subjects=Subject.objects.all()
    if request.method=='POST':
        try:
            class_id=request.POST.get('class')
            subject_id=request.POST.get('subject')
            # classes=Class.objects.get(id=class_id)            #We can get id through this or we can use id directly
            # subjects=Subject.objects.get(id=subject_id)
            
            SubjectCombination.objects.create(student_class_id=class_id,subject_id=subject_id,status=1) # we can use id directly
            messages.success(request,"Subject Combination Added Successfully")
            return redirect('add_subject_combination')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('add_subject_combination')

    return render(request,'add_subject_combination.html',locals())


def manage_subject_combination(request):
    combinations=SubjectCombination.objects.all()
    if request.GET.get('activate_id'):
        activate_id=request.GET.get('activate_id')
        try:
            subject_combination_obj=SubjectCombination.objects.filter(id=activate_id)
            subject_combination_obj.update(status=1)
            messages.success(request,"Subject Combination Activated Successfully")
            
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
        return redirect('manage_subject_combination')
    
    if request.GET.get('deactivate_id'):
        deactivate_id=request.GET.get('deactivate_id')
        try:
            subject_combination_obj=SubjectCombination.objects.filter(id=deactivate_id)
            subject_combination_obj.update(status=0)
            messages.success(request,"Subject Combination Deactivated Successfully")
            
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
        return redirect('manage_subject_combination')
    return render(request,'manage_subject_combination.html',locals()) 


@login_required                 # to prevent direct access to create_class page through URL
def add_student(request):
    classes=Class.objects.all()
    subjects=Subject.objects.all()
    if request.method=='POST':
        try:
            fullname=request.POST.get('fullname')
            rollid=request.POST.get('rollid')
            gender=request.POST.get('gender')
            emailid=request.POST.get('emailid')
            class_id=request.POST.get('class')
            dob=request.POST.get('dob')
            # classes=Class.objects.get(id=class_id)            #We can get id through this or we can use id directly
            # subjects=Subject.objects.get(id=subject_id)
            
            Student.objects.create(name=fullname,roll_id=rollid,gender=gender,email=emailid,student_class_id=class_id,dob=dob,status=1) # we can use id directly
            messages.success(request,"Student Added Successfully")
            return redirect('add_student')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('add_student')

    return render(request,'add_student.html',locals())

def manage_students(request):
    students=Student.objects.all() 
    return render(request,'manage_students.html',locals()) 

@login_required
def edit_student(request,student_id):
    student_obj=get_object_or_404(Student,id=student_id)
    classes=Class.objects.all()
    if request.method=='POST':
        try:
            student_obj.name=request.POST.get('fullname')       #Updation using object/another way of updation instead of using .update()
            student_obj.roll_id=request.POST.get('rollid')
            student_obj.gender=request.POST.get('gender')
            student_obj.email=request.POST.get('emailid')
            student_obj.student_class_id=request.POST.get('class')
            student_obj.dob=request.POST.get('dob')
            student_obj.status=request.POST.get('status')
            student_obj.save()
            messages.success(request,"Student Updated Successfully")
            return redirect('manage_students')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('edit_student')
    return render(request,'edit_student.html',locals()) 


@login_required                 # to prevent direct access to create_class page through URL
def add_notice(request):
    if request.method=='POST':
        try:
            notice_title=request.POST.get('title')
            notice_description=request.POST.get('description')
            # classes=Class.objects.get(id=class_id)            #We can get id through this or we can use id directly
            # subjects=Subject.objects.get(id=subject_id)
            Notice.objects.create(title=notice_title,description=notice_description)
            messages.success(request,"Notice Added Successfully")
            return redirect('add_notice')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('add_notice')

    return render(request,'add_notice.html',locals())

@login_required
def manage_notices(request):
    notices=Notice.objects.all()
    if request.GET.get('delete'):
        try:
            notice_id=request.GET.get('delete')
            notice_obj=get_object_or_404(Notice,id=notice_id) #we can write pk instead of id as parameter
            notice_obj.delete()
            messages.success(request,"Notice Deleted Successfully")
            return redirect('manage_notices')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('manage_notices')
    return render(request,'manage_notices.html',locals()) 


@login_required                 # to prevent direct access to create_class page through URL
def add_result(request):
    classes=Class.objects.all()
    subjects=Subject.objects.all()
    if request.method=='POST':
        try:
            class_id=request.POST.get('class')
            student_id=request.POST.get('student_id')
            marks_data={ key.split('_')[1]:value for key, value in request.POST.items() if key.startswith('marks_')}
            # classes=Class.objects.get(id=class_id)            #We can get id through this or we can use id directly
            # subjects=Subject.objects.get(id=subject_id)
            for subject_id,marks in marks_data.items():
                Result.objects.create(
                    student_id=student_id,
                    student_class_id=class_id,
                    subject_id=subject_id,
                    marks=marks
                )
            messages.success(request,"Result Added Successfully")
            return redirect('add_result')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('add_result')

    return render(request,'add_result.html',locals())


from django.http import JsonResponse
def get_students_subjects(request):
    class_id=request.GET.get('class_id')
    
    if class_id:
        students=list(Student.objects.filter(student_class_id=class_id).values('id','name','roll_id'))
        subject_combinations=SubjectCombination.objects.filter(student_class_id=class_id,status=1).select_related('subject')


        subjects=[{'id':sc.subject.id,'name':sc.subject.subject_name} for sc in subject_combinations]
        return JsonResponse({'students':students,'subjects':subjects})


    return JsonResponse({'students':[],'subjects':[]})


@login_required
def manage_results(request):
    results=Result.objects.select_related('student','student_class','subject').all()
    students={}
    for result in results:
        std_id=result.student.id
        if result.student.id not in students :
            students[std_id]={
                'student':result.student,
                'class':result.student_class,
                'reg_date':result.student.registration_date,
                'status':result.student.status
            }

    return render(request,'manage_results.html',{'results':students.values()}) 

@login_required
def edit_result(request,std_id):
    student_obj=get_object_or_404(Student,id=std_id)
    student_results=Result.objects.filter(student_id=std_id)
    if request.method=='POST':
        try:
            ids=request.POST.getlist('id[]')  #id[]:[5,6,7]
            marks=request.POST.getlist('marks[]')#marks[]:[50,60,70]

            for i in range(len(ids)):
                result_obj=get_object_or_404(Result,id=ids[i])
                result_obj.marks=marks[i]
                result_obj.save()
            messages.success(request,"Result Updated Successfully")
            # return redirect('edit_result',std_id) # This will redirect to the same page
            return redirect('manage_results')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('edit_result')
    return render(request,'edit_result.html',locals()) 

from django.contrib.auth import authenticate,update_session_auth_hash
@login_required
def change_password(request):
    if request.method=='POST':
            old_password=request.POST.get('old_password')
            new_password=request.POST.get('new_password')
            confirm_password=request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request,"New password and confirm password do not match.")
                return redirect('change_password')
            
            user=authenticate(username=request.user.username,password=old_password)
            if user:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request,user)
                messages.success(request,"Password Changed Successfully")
                return redirect('change_password')
            else:
                messages.error(request,"Old password is incorrect.")
                return redirect('change_password')
    return render(request,'change_password.html',locals()) 


def search_result(request):
    classes=Class.objects.all()

    return render(request,'search_result.html',locals()) 

@csrf_exempt
def check_result(request):
    classes=Class.objects.all()
    if request.method=='POST':
            roll_id=request.POST.get('rollid')
            class_id=request.POST.get('class')
            try:
                student=Student.objects.get(roll_id=roll_id,student_class_id=class_id)
                results=Result.objects.filter(student=student)

                total_marks=sum([result.marks for result in results])
                subject_count=results.count()
                max_total=subject_count*100
                percentage=(total_marks/max_total) if max_total>0 else 0
                percentage=round(percentage,2)

                return render(request,'result_page.html',locals()) 
            
            except Exception as e:
                messages.error(request,f"No result found for given Roll ID and Class.")
                return redirect('search_result')

    

