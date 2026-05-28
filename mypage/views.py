from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import TeamMember
from relay.models import Relay, RelaySlot
from django.contrib.auth import logout

# 마이페이지 정보 가져오기
@login_required
def mypage(request):
    user = request.user
    team_member = user.teammember_set.first()
    team = team_member.team if team_member else None

    relay = Relay.objects.filter(team=team, is_active=True).first() if team else None

    current_user_slot = RelaySlot.objects.filter(
        relay=relay,
        runner=user
    ).first() if relay else None

    context = {
        'user': user,
        'team': team,
        'team_member': team_member,
        'current_user_slot': current_user_slot,
    }
    return render(request, 'mypage/mypage.html', context)

# 프로필 정보 수정
@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')  # 이미지 파일

        # 닉네임 수정
        if nickname:
            user.nickname = nickname

        # 비밀번호 수정
        if password:
            user.set_password(password)

        # 프로필 이미지 수정
        if profile_image:
            user.profile_image = profile_image

        user.save()

        # 비밀번호 바꾸면 로그인이 풀리므로 다시 로그인
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, user)

        return redirect('mypage')

    return render(request, 'mypage/profile_edit.html', {'user': user})

# 회원 탈퇴
@login_required
def delete_account(request):
    # GET 처리 없이 POST만 처리
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('login_home')
    # GET으로 접근하면 마이페이지로 돌려보내기
    return redirect('mypage')