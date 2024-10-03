from sqlite3 import IntegrityError
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import *
from django.contrib.auth import login as auth_login ,logout
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import timedelta
from django.utils import timezone

# Create your views here.


class login(View):
    def get(self,request):
        return render(request,'login.html')
    
    
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=None
        print(email,password)
        if email and password  :
            if Student.objects.filter(email=email).exists():
                    user=Student.objects.get(email=email)
                    if not check_password( password ,user.password):
                            user=None
            elif  Teacher.objects.filter(email=email).exists():
                user=Teacher.objects.get(email=email)
                if not check_password( password ,user.password):
                    user=None
        else:
            return render(request,'login.html')
        # print(user.pk)
        if user != None:
            auth_login(request,user)
    
            return redirect(reverse('index'))
        else:
            messages.error(request,'Login failed')
            return render(request,'login.html')
    



class signup(View):
    def get(self,request):
        return render(request,'signup.html')
    
    
    def post(self,request):
            email = request.POST.get('email')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            age = request.POST.get('age')
            mobile = request.POST.get('mobile')
            image = request.FILES.get('image')
            user_type = request.POST.get('type')
            certificas = ""
            Academic_stage = ""
            user=None
            if user_type == "student":
                if Student.objects.filter(email=email).exists():
                    messages.error(request, 'The email already exists')
                    return render(request, 'signup.html')
                Academic_stage = request.POST.get('Academic_stage')
            else:
                if Teacher.objects.filter(email=email).exists():
                    messages.error(request, 'The email already exists')
                    return render(request, 'signup.html')
                certificas = request.POST.get('certificas')

            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return render(request, 'signup.html')
            if type ==  'student':
                user = Student.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password1),
                    age=age,
                    Academic_stage=Academic_stage,
                    image=image,
                    mobile=mobile
                )
            else:
                   user = Teacher.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password1),
                    age=age,
                    certificas=certificas,
                    image=image,
                    mobile=mobile
                )

            if user !=None:
                print(user)
                auth_login(request,user)
                return render(request, 'login.html')
            else:
                messages.error(request, 'Your data is not valid')
                return render(request, 'signup.html')
            


class profilet(View):
    def get(self,request):
        user=request.user
        print(user.username)
        user=Teacher.objects.get(pk=user.pk)
        return render(request,'profile.html',{'user':user})
    def post(self,request):
        user=request.user
        user=Teacher.objects.get(pk=user.pk)

        try:
            user.username=request.POST.get('username')
            user.mobile=request.POST.get('mobile')
            user.age=request.POST.get('age')
            # user.password=request.POST.get('')
            user.certificas=request.POST.get('certificas')
            # print(request.FILES.get('image'))
            user.image=request.FILES.get('image')
            p1=request.POST.get('password1')
            p2=request.POST.get('password2')
            if p1 == p2 :
                if p1 !="":
                    user.password=make_password(p1)
                if CustomUser.objects.filter(email=request.POST.get('email')).exists() and request.POST.get('email')!=user.email:
                        messages.error(request,'email already exist')
                        return render(request,'profile.html',{'user':user})   
                else:
                    user.email=request.POST.get('email')
                    user.save()
            else: 
                messages.error(request, 'Passwords do not match')
                return render(request,'profile.html',{'user':user})
        except :
            messages.error(request,'email already exist')
        return render(request,'profile.html',{'user':user})   
    
    
    
    
    
    
    


class profiles(View):
    def get(self,request):
        user=request.user
        user=Student.objects.get(pk=user.pk)
        return render(request,'profile.html',{'user':user})
    def post(self,request):
        user=request.user
        user=Student.objects.get(pk=user.pk)

        try:
            user.username=request.POST.get('username')
            user.mobile=request.POST.get('mobile')
            user.age=request.POST.get('age')
            # user.password=request.POST.get('')
            user.Academic_stage=request.POST.get('Academic_stage')
            # print(request.FILES.get('image'))
            user.image=request.FILES.get('image')
            p1=request.POST.get('password1')
            p2=request.POST.get('password2')
            if p1 == p2 :
                if p1 !="":
                    user.password=make_password(p1)
                if CustomUser.objects.filter(email=request.POST.get('email')).exists() and request.POST.get('email')!=user.email:
                        messages.error(request,'email already exist')
                        return render(request,'profile.html',{'user':user})   
                else:
                    user.email=request.POST.get('email')
                    user.save()
            else: 
                messages.error(request, 'Passwords do not match')
                return render(request,'profile.html',{'user':user})
        except :
            messages.error(request,'email already exist')
        return render(request,'profile.html',{'user':user})   
    
    
    
    
def logout_view(request):
    logout(request)
    return redirect('login')
############################################################





class addquestionset(View):
    def get(self,request):
        return render(request,'addquestionset.html')
    def post(self,request):
        form_data = request.POST

      
        questions = {}
        if request.POST.get("title")!="" and request.POST.get("Limit_of_success")!="":
            teacher=Teacher.objects.get(email=request.user.email)
            newquestionset=Questionset.objects.create(title=request.POST.get("title"),
                                                   Limit_of_success=request.POST.get("Limit_of_success"),
                                                   teacher=teacher,
                                                   Number_of_successful=0,
                                                   Number_of_failures=0)
            for key, value in form_data.items():
                if key.startswith("content-"):
                    question_id = key.split('-')[1]
                    questions[question_id] = {
                        "content": value,
                        "true_answer": form_data.get(f"1-{question_id}"),
                        "false_answer1": form_data.get(f"2-{question_id}"),
                        "false_answer2": form_data.get(f"3-{question_id}"),
                        "grade": form_data.get(f"4-{question_id}"),
                    }
                    quas=Question.objects.create(content=value,
                                                grade=questions[question_id]["grade"],
                                                questionset=newquestionset
                                                )
                

                    ans1=Answer.objects.create(content=questions[question_id]["true_answer"],question=quas,is_true=True)
                    ans2=Answer.objects.create(content=questions[question_id]["false_answer1"],question=quas,is_true=False)
                    ans3=Answer.objects.create(content=questions[question_id]["false_answer2"],question=quas,is_true=False)
        
        return render(request,'addquestionset.html')

    










class index(View):
    def post(self,request):
        if request.POST.get("search"):
            search=request.POST.get("search")
            all_quastionset=Questionset.objects.filter(title=search)
            paginator=Paginator(all_quastionset,1) 
            page_number=request.GET.get("page")
            try:
                all_quastionset=paginator.page(page_number)
            except PageNotAnInteger: 
                all_quastionset=paginator.page(1)
            except EmptyPage: 
                all_quastionset=paginator.page(1)
            
            user=None
            if Student.objects.filter(email=request.user.email).exists():
                user=Student.objects.get(email=request.user.email)
            else:
                user=Teacher.objects.get(email=request.user.email)

            context={
                'user':user,
                'all_quastionset':all_quastionset
            }
            return render(request,'index.html',context)
        else:
            all_quastionset=Questionset.objects.all()
            paginator=Paginator(all_quastionset,1) 
            page_number=request.GET.get("page")
            try:
                all_quastionset=paginator.page(page_number)
            except PageNotAnInteger: 
                all_quastionset=paginator.page(1)
            except EmptyPage: 
                all_quastionset=paginator.page(1)
            
            user=None
            if Student.objects.filter(email=request.user.email).exists():
                user=Student.objects.get(email=request.user.email)
            else:
                user=Teacher.objects.get(email=request.user.email)

            context={
                'user':user,
                'all_quastionset':all_quastionset
            }
            return render(request,'index.html',context)
    
    
    def get(self,request):
        all_quastionset=Questionset.objects.all()
        paginator=Paginator(all_quastionset,1) 
        page_number=request.GET.get("page")
        try:
            all_quastionset=paginator.page(page_number)
        except PageNotAnInteger: 
            all_quastionset=paginator.page(1)
        except EmptyPage: 
            all_quastionset=paginator.page(1)
        
        user=None
        if Student.objects.filter(email=request.user.email).exists():
            user=Student.objects.get(email=request.user.email)
        else:
            user=Teacher.objects.get(email=request.user.email)

        context={
            'user':user,
            'all_quastionset':all_quastionset
        }
        return render(request,'index.html',context)
    
    
    
    
class exam(View):
    def post(self,request,pk):
        user=None
        if Student.objects.filter(email=request.user.email).exists():
            user=Student.objects.get(email=request.user.email)
        else:
            user=Teacher.objects.get(email=request.user.email)
        form_data = request.POST
        result=0
        questions = {}
        for key, value in form_data.items():
                if key.startswith("question-"):
                    question_id = key.split('-')[1]
                    ch="no"
                    qu=Question.objects.get(id=value)
                    try:
                        ch=Answer.objects.get(pk=form_data.get(question_id))
                        if ch.is_true == 1:
                            result+=qu.grade
                    except:
                        ch="no"
                    questions[question_id] = {
                        "question": qu,
                        "answers": Answer.objects.filter(question=value),
                        "ch": ch,
                    }
                Limit_of_success=    Questionset.objects.get(pk=pk).Limit_of_success
                questionset= Questionset.objects.get(pk=pk)
                if result>=Limit_of_success:
                  questionset.Number_of_successful+=1
                  questionset.save()
                else:
                   questionset.Number_of_failures+=1
                   questionset.save()     
                
                exam=Exam.objects.get(student=user,questionset=questionset)
                exam.end=exam.start
                exam.save()
                if not Exams_Results.objects.filter(name_questionset=questionset.title,student=user).exists():
                    Exams_Results.objects.create(name_questionset=questionset.title,grade=result,is_succeed=(result>=questionset.Limit_of_success),student=user)
                context={
                      'user':user,
                    'questions':questions,
                    'post':"post",
                    'result': result,
                   'Limit_of_success': Limit_of_success
                }      
        return render(request,'exam.html',context)
        
   
    def get(self, request, pk):
        context={}
        user=None
        if Student.objects.filter(email=request.user.email).exists():
            user=Student.objects.get(email=request.user.email)
        else:
            user=Teacher.objects.get(email=request.user.email)
        if Student.objects.filter(email=request.user.email):
            student = Student.objects.get(email=request.user.email)
            questionset = Questionset.objects.get(pk=pk)
            qus_count = Question.objects.filter(questionset=questionset).count()
            
        
            exam, created = Exam.objects.get_or_create(
                student=student,
                questionset=questionset,
                defaults={'end': timezone.now() + timedelta(minutes=qus_count / 2 + 1)}
            )
            
        
            time_remaining = (exam.end - timezone.now()).total_seconds()

            allquestions = Question.objects.filter(questionset=questionset)
            question_with_answer = {}
            for i in allquestions:
                answer = Answer.objects.filter(question=i)
                question_with_answer[i] = answer

        

            context = {
                'user':user,
                'question_with_answer': question_with_answer,
                'time': time_remaining 
            }
        else :
            questionset = Questionset.objects.get(pk=pk)
            allquestions = Question.objects.filter(questionset=questionset)
            question_with_answer = {}
            for i in allquestions:
                answer = Answer.objects.filter(question=i)
                question_with_answer[i] = answer
            context = {
                'user':user,
                'question_with_answer': question_with_answer,
                
            }
        return render(request, 'exam.html', context)
    
    
    
class view_myqestionsset(View):
    def post(self,request):
        pass
    def get(self,request):
        user=Teacher.objects.get(email=request.user.email)
        all_quastionset=Questionset.objects.filter(teacher=user)
        paginator=Paginator(all_quastionset,1) 
        page_number=request.GET.get("page")
        try:
            all_quastionset=paginator.page(page_number)
        except PageNotAnInteger: 
            all_quastionset=paginator.page(1)
        except EmptyPage: 
            all_quastionset=paginator.page(1)
        
        

        context={
            'user':user,
            'all_quastionset':all_quastionset
        }
        return render(request,'view_myquestionsset.html',context)
    
    
    
class edite_myquestionset(View):
    def post(self,request,pk):
        form_data = request.POST
        Questionset.objects.get(pk=pk).delete()
        questions = {}
        if request.POST.get("title")!="" and request.POST.get("Limit_of_success")!="":
            teacher=Teacher.objects.get(email=request.user.email)
            newquestionset=Questionset.objects.create(title=request.POST.get("title"),
                                                   Limit_of_success=request.POST.get("Limit_of_success"),
                                                   teacher=teacher,
                                                   Number_of_successful=0,
                                                   Number_of_failures=0)
            for key, value in form_data.items():
                if key.startswith("content-"):
                    question_id = key.split('-')[1]
                    questions[question_id] = {
                        "content": value,
                        "true_answer": form_data.get(f"1-{question_id}"),
                        "false_answer1": form_data.get(f"2-{question_id}"),
                        "false_answer2": form_data.get(f"3-{question_id}"),
                        "grade": form_data.get(f"4-{question_id}"),
                    }
                    quas=Question.objects.create(content=value,
                                                grade=questions[question_id]["grade"],
                                                questionset=newquestionset
                                                )
                

                    ans1=Answer.objects.create(content=questions[question_id]["true_answer"],question=quas,is_true=True)
                    ans2=Answer.objects.create(content=questions[question_id]["false_answer1"],question=quas,is_true=False)
                    ans3=Answer.objects.create(content=questions[question_id]["false_answer2"],question=quas,is_true=False)
        
        return redirect(reverse('myquestionset'))

    def get(self,request,pk):
        questionset=Questionset.objects.get(pk=pk)
        questions=Question.objects.filter(questionset=questionset)
        all_questions={}
        
        for i in questions:
            ans=Answer.objects.filter(is_true=False,question=i)
            ans1 = None
            ans2 = None
            if ans.count() >= 2:
                ans1 = ans[0] 
                ans2 = ans[1] 
              
            print(ans)
            all_questions[i.pk]={
                'qus':i,
                'true':Answer.objects.get(is_true=True,question=i),
                'false1':ans1,
                'false2':ans2
            }
        context={
                'all_questions':all_questions,
                'title':questionset.title,
                'Limit_of_success':questionset.Limit_of_success
            }
        return render(request,'edit_questionset.html',context)
        
      
        
        
def view_myexams(request):
    user=Student.objects.get(email=request.user.email)
    all_Exam=Exams_Results.objects.filter(student=user)
    paginator=Paginator(all_Exam,1) 
    page_number=request.GET.get("page")
    try:
        all_Exam=paginator.page(page_number)
    except PageNotAnInteger: 
        all_Exam=paginator.page(1)
    except EmptyPage: 
        all_Exam=paginator.page(1)
        
    context={
            'user':user,
            'all_Exam':all_Exam
        }
    return render(request,'view_myexam.html',context)