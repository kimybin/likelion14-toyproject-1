from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from home.models import User

# 맨 처음 화면
def login_home_view(request):
    return render(request, 'accounts/login_home.html')

# 로그인
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error' : '아이디 또는 비밀번호가 틀렸습니다.'})

    return render(request, 'accounts/login.html')

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('login')

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nickname = request.POST['nickname'] # 아직 미정

        # 아이디 중복 체크 (username)
        if User.objects.filter(username=username).exists():
            return render(request, 'account/signup.html', {'error' : '이미 사용 중인 아이디입니다.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            nickname=nickname
        )

        login(request, user)
        return redirect('goal')
    return render(request, 'accounts/signup.html')

# 인기 목표 선택
def goal_view(request):
    # 아이콘 이미지이름, 경로에 따라 수정될 수 있음
    popular_goals = [
        {'title': '오전 7시 전에 일어나기', 'icon': 'images/icon-bed.svg'},
        {'title': '하루 30분 걷기', 'icon': 'images/icon-walk.svg'},
        {'title': '하루 30분 영어 공부 하기', 'icon': 'images/icon-book.svg'},
        {'title': 'SNS 1시간 이하 사용하기', 'icon': 'images/icon-phone.svg'},
        {'title': '하루 한 페이지 글쓰기', 'icon': 'images/icon-pencil.svg'},
        {'title': '하루 물 2L 마시기', 'icon': 'images/icon-water.svg'},
        {'title': '하루 10분 스트레칭 하기', 'icon': 'images/icon-stretch.svg'},
        {'title': '하루 토익 단어 50개 외우기', 'icon': 'images/icon-study.svg'},
        {'title': '자기 전 독서 20분 하기', 'icon': 'images/icon-read.svg'},
    ]

    if request.method == 'POST':
        selected_goal = request.POST['goal']
        request.session['goal'] = selected_goal # 나중에 팀 생성 화면이 만들어지면 그때 Relay 모델에 제대로 저장되도록 수정
        # 지금은 팀 생성 화면이 없으니까 세션에 임시 보관

        return redirect('home')

    return render(request, 'accounts/goal.html', {'popular_goals': popular_goals})


# 목표 직접 입력
def goal_custom_view(request):
    if request.method == 'POST':
        custom_goal = request.POST['goal']
        request.session['goal'] = custom_goal
        return redirect('home')

    return render(request, 'accounts/goal_custom.html')