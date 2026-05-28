from django.utils import timezone
from unittest import runner

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from home.models import User, Team, TeamMember
from relay.models import Relay, RelaySlot


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
        password_confirm = request.POST['password_confirm']
        nickname = request.POST['nickname']
        email = request.POST['email']

        # 비밀번호 확인
        if password != password_confirm:
            return render(request, 'accounts/signup.html', {'error' : '비밀번호가 일치하지 않습니다.'})

        # 아이디 중복 체크 (username)
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {'error' : '이미 사용 중인 아이디입니다.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            nickname=nickname,
            email=email,
        )

        login(request, user)
        return redirect('team_name')

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

        # request.session['goal'] = selected_goal # 나중에 팀 생성 화면이 만들어지면 그때 Relay 모델에 제대로 저장되도록 수정
        # # 지금은 팀 생성 화면이 없으니까 세션에 임시 보관

        # 현재 유저의 팀 가져오기
        team_member = request.user.teammember_set.first()
        team = team_member.team if team_member else None

        if team:
            # 이미 Relay가 있으면 새로 만들지 않음
            existing_relay = Relay.objects.filter(team=team, is_active=True).first()

            # Relay 생성
            if not existing_relay:
                relay = Relay.objects.create(  # ← relay 변수에 저장
                    team=team,
                    goal=selected_goal,
                    days_per_runner=3,
                    started_at=timezone.now(),
                    is_active=True,
                    consecutive_count=0
                )
            else:
                relay = existing_relay

            # # 3명 다 모였고 RelaySlot이 아직 없으면 생성
            # member_count = TeamMember.objects.filter(team=team).count()
            # slot_count = RelaySlot.objects.filter(relay=relay).count()
            #
            # print(f"member_count: {member_count}")  # 추가
            # print(f"slot_count: {slot_count}")  # 추가
            # print(f"relay: {relay}")  # 추가
            #
            # if member_count == 3 and slot_count == 0:
            #     print("슬롯 생성 시작!")
            #     _create_relay_slots(team, relay)

        return redirect('home')

    return render(request, 'accounts/goal.html', {'popular_goals': popular_goals})


# 목표 직접 입력
def goal_custom_view(request):
    if request.method == 'POST':
        custom_goal = request.POST['goal']

        # request.session['goal'] = custom_goal

        # 현재 유저의 팀 가져오기
        team_member = request.user.teammember_set.first()
        team = team_member.team if team_member else None

        if team:
            # 이미 Relay가 있으면 새로 만들지 않음
            existing_relay = Relay.objects.filter(team=team, is_active=True).first()

            if not existing_relay:
                relay = Relay.objects.create(  # ← relay = 추가
                    team=team,
                    goal=custom_goal,
                    days_per_runner=3,
                    started_at=timezone.now(),
                    is_active=True,
                    consecutive_count=0
                )
            else:
                relay = existing_relay

            # # 3명 다 모였고 RelaySlot이 아직 없으면 생성
            # member_count = TeamMember.objects.filter(team=team).count()
            # slot_count = RelaySlot.objects.filter(relay=relay).count()
            #
            # if member_count == 3 and slot_count == 0:
            #     _create_relay_slots(team, relay)

        return redirect('home')


    return render(request, 'accounts/goal_custom.html')

# 팀 이름 정하기 (팀장-1번째)
def team_name_view(request):
    if request.method == 'POST':
        team_name = request.POST['team_name']

        # Team 생성
        team = Team.objects.create(name=team_name)

        # TeamMember 생성
        TeamMember.objects.create(
            team=team,
            user=request.user,
            role='leader',
        )

        # 팀장은 order=1로 저장해서 첫 번째 주자로 자동 설정
        request.session['team_id'] = team.id # 나중에 쓸 팀 id 세션 저장
        return redirect('goal')
    return render(request, 'accounts/team_name.html')


# 팀 참여하기 (팀원 - 순서대로 2번째, 3번째 주자)
def team_join_view(request):
    if request.method == 'POST':
        invite_code = request.POST['invite_code']

        # 초대 코드로 팀 찾기
        try:
            team = Team.objects.get(invite_code=invite_code)
        except Team.DoesNotExist:
            return render(request, 'accounts/team_join.html', {'error' : '유효하지 않은 초대 코드입니다.'})

        # 이미 팀에 속해있는지 확인
        if TeamMember.objects.filter(user=request.user, team=team).exists():
            return render(request, 'accounts/team_join.html', {'error' : '이미 해당 팀에 속해있습니다.'})

        # 현재 팀 인원 수 확인해서 order 결정
        current_count = TeamMember.objects.filter(team=team).count()
        print(f"current_count: {current_count}")  # 추가

        if current_count >= 3:
            return render(request, 'accounts/team_join.html', {'error': '팀 인원이 가득 찼습니다.'})

        # TeamMember 등록
        TeamMember.objects.create(
            user=request.user,
            team=team,
            role='member',
        )

        # 3명 다 모이면 RelaySlot 생성
        if current_count + 1 == 3:
            print("3명 조건 충족!")  # 추가
            relay = Relay.objects.filter(team=team, is_active=True).first()
            print(f"relay: {relay}")  # 추가
            if relay:
                slot_count = RelaySlot.objects.filter(relay=relay).count()
                print(f"slot_count: {slot_count}")  # 추가
                if slot_count == 0:
                    _create_relay_slots(team, relay)

        return redirect('home')
    return render(request, 'accounts/team_join.html')


# RelaySlot 생성 함수 (들어온 순서대로)
def _create_relay_slots(team, relay):
    from django.utils import timezone
    members = TeamMember.objects.filter(team=team).order_by('id') # id 순서 = 들어온 순서

    print(f"members: {members}")  # 추가
    print(f"members count: {members.count()}")  # 추가

    for index, member in enumerate(members):
        print(f"슬롯 생성: {member.user.nickname} order={index + 1}")  # 추가
        order = index + 1
        start_date = relay.started_at.date() + timezone.timedelta(days=(order-1) * relay.days_per_runner)
        end_date = start_date + timezone.timedelta(days=relay.days_per_runner - 1)

        RelaySlot.objects.create(
            relay=relay,
            runner=member.user,
            order=order,
            status='running' if order == 1 else 'waiting', # 1번째만 running
            start_date=start_date,
            end_date=end_date,
        )