from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from home.models import TeamMember
from relay.models import Relay, RelaySlot

@login_required # 로그인한 유저만 접근 가능
# 나중에 로그인 기능 만들고 다시 활성화
def home(request):
    user = request.user # 현재 로그인한 유저 객체

    # 로그인 안 된 상태면 임시 빈 데이터로 처리
    if not user.is_authenticated:
        context = {
            'user': None,
            'team': None,
            'relay': None,
            'slots': [],
            'current_slot': None,
            'current_user_slot': None,
            'today': timezone.now(),
        }
        return render(request, 'home/home.html', context)


    # 1. 소속 팀 가져오기
    team_member = user.teammember_set.first()
    team = team_member.team if team_member else None

    # 2. 현재 진행 중인 릴레이 가져오기
    relay = Relay.objects.filter(
        team=team,
        is_active=True
    ).first()

    # 3. 릴레이 슬롯 가져오기 (순서대로)
    slots = RelaySlot.objects.filter(
        relay=relay
    ).order_by('order') if relay else []

    # 4. 현재 running 중인 슬롯 (카운트다운용)
    current_slot = RelaySlot.objects.filter(
        relay=relay,
        status='running'
    ).first() if relay else None

    # 5. 현재 유저가 몇 번째 주자인지
    current_user_slot = RelaySlot.objects.filter(
        relay=relay,
        runner=user
    ).first() if relay else None

    context = {
        'user': user,
        'team': team,
        'relay': relay,
        'slots': slots,
        'current_slot': current_slot,
        'current_user_slot': current_user_slot,
        'today': timezone.now(),
    }

    return render(request, 'home/home.html', context)
