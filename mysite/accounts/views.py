# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import auth
from .models import CustomUser
from django.contrib import messages
from django.db import connection  # 여기에 추가하여 connection을 가져옴
from django.contrib.auth.hashers import check_password  # check_password 함수 가져오기


def home(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'accounts/home.html', context)

def register(request):
		# POST 요청 시, 사용자 생성(회원가입) 시도
    if request.method == "POST":
        id = request.POST['id']
        name = request.POST['name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
		            # 사용자 생성
                user = CustomUser.objects.create_user(
                    username=id,
                    id=id,
                    name=name,
                    password=password1
                )
                # 회원가입 후 자동 로그인
                auth.login(request, user)         
                return redirect('accounts:home')
                
            except Exception as e:
                # messages.error(request, f'회원가입 중 오류 발생: {str(e)}')
                return redirect('accounts:register')
        else:
            # messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('accounts:register')
    
    # GET 요청 시, 페이지 렌더링
    return render(request, 'accounts/register.html')

""" 로그인 과정 없이 단순히 값만 넘김 """
def login(request):
     if request.method == 'POST':
         id = request.POST.get('id')
         password = request.POST.get('password')
         context = {
             'id': id,
             'password': password
         }
         return render(request, 'polls/index.html', context)
     return render(request, 'accounts/login.html')


""" AUTH함수 사용해서 구현 """
def login_1(request):
    if request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']
        
        user = auth.authenticate(request, username=id, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('polls:index')

    return render(request, 'accounts/login.html')

"""방법 1: ID와 비교하여 사용자 조회"""
def login_method1(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            # SQL 쿼리로 사용자 정보 가져오기
            cursor.execute("SELECT id, password, name FROM users WHERE id = %s", [user_id])
            result = cursor.fetchone()  # 첫 번째 결과 가져오기
        
        if result is not None:
            db_id, db_password, db_name = result
            print("id is " , db_id)
            print("password is ", password)
            print("db_password is ", db_password)
            print("name is ", db_name)
            
            # check_password로 해시된 비밀번호 비교
            if check_password(password, db_password):  # 해시된 비밀번호 비교
                # 로그인 세션 시작
                request.session['user_id'] = db_id
                request.session['user_name'] = db_name
                return redirect('polls:index')
            else:
                messages.error(request, '비밀번호가 틀렸습니다.')
        else:
            messages.error(request, '존재하지 않는 ID입니다.')
    
    return render(request, 'accounts/login.html')


"""방법 2: ID와 비밀번호 모두 비교하여 사용자 조회"""
def login_method2(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            # ID와 해시된 비밀번호가 모두 일치하는지 확인
            cursor.execute("SELECT id, password, name FROM users WHERE id = %s AND password = %s", [user_id, password])
            result = cursor.fetchone()
        
        if result is not None:
            db_id, db_password, db_name = result
             # check_password로 해시된 비밀번호 비교
            if check_password(password, db_password):  # 해시된 비밀번호 비교
                # 로그인 세션 시작
                request.session['user_id'] = db_id
                request.session['user_name'] = db_name
                return redirect('polls:index')

            request.session['user_id'] = db_id
            return redirect('polls:index')
        else:
            messages.error(request, 'ID 또는 비밀번호가 잘못되었습니다.')
    
    return render(request, 'accounts/login.html')