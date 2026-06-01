from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import TeamMember
from relay.models import Relay, RelaySlot, Certification
from django.utils import timezone

@login_required
def relay(request):
    user = request.user
    team_member = user.teammember_set.first()
    team = team_member.team if team_member else None
    relay_obj = Relay.objects.filter(team=team, is_active=True).first() if team else None

    # 슬롯 가져오기 (순서대로)
    slots = RelaySlot.objects.filter(relay=relay_obj).order_by('order') if relay_obj else []

    # 슬롯별 인증 사진 가져오기
    slot_data = []
    for slot in slots:
        # 오늘 날짜 기준 가장 최근 시작 인증 사진
        latest_cert = Certification.objects.filter(
            slot=slot,
            cert_type='start'
        ).order_by('-certified_at').first()

        # 완료된 일수 계산
        completed_days = 0
        for day in range(1, slot.relay.days_per_runner + 1):
            s = Certification.objects.filter(slot=slot, day_number=day, cert_type='start').exists()
            e = Certification.objects.filter(slot=slot, day_number=day, cert_type='end').exists()
            if s and e:
                completed_days += 1

        # 상태 텍스트 결정
        if slot.status == 'done':
            status_text = '바톤터치 완료'
        elif slot.status == 'waiting':
            status_text = '바톤 대기 중'
        elif completed_days > 0:
            status_text = f'{completed_days}일차 인증 완료'
        else:
            status_text = '진행 중'


        slot_data.append({
            'slot': slot,
            'latest_cert': latest_cert,
            'is_mine': slot.runner == user,  # 본인 슬롯 여부
            'status_text': status_text,
        })

    # 팀 인원 수 (+ 버튼 표시 여부)
    member_count = TeamMember.objects.filter(team=team).count() if team else 0

    print(f"member_count: {member_count}")

    context = {
        'team': team,
        'relay': relay_obj,
        'slot_data': slot_data,
        'member_count': member_count,
        'today': timezone.now(),
    }
    return render(request, 'relay/relay.html', context)


@login_required
def invite(request):
    user = request.user
    team_member = user.teammember_set.first()
    team = team_member.team if team_member else None

    context = {
        'team': team,
    }
    return render(request, 'relay/invite.html', context)


@login_required
def certification(request, slot_id):
    user = request.user
    slot = get_object_or_404(RelaySlot, id=slot_id, runner=user)  # 본인 슬롯만 접근 가능

    # 오늘 날짜 기준 day_number 계산
    today = timezone.now().date()
    day_number = (today - slot.start_date).days + 1

    # 오늘 인증 현황
    today_start = Certification.objects.filter(
        slot=slot, day_number=day_number, cert_type='start'
    ).first()
    today_end = Certification.objects.filter(
        slot=slot, day_number=day_number, cert_type='end'
    ).first()

    if request.method == 'POST':
        image = request.FILES.get('image')
        cert_type = request.POST.get('cert_type')  # 'start' or 'end'

        if image and cert_type:
            Certification.objects.create(
                slot=slot,
                image=image,
                day_number=day_number,
                cert_type=cert_type,
            )

            # 오늘 시작+종료 둘 다 완료됐는지 확인
            start_done = Certification.objects.filter(
                slot=slot, day_number=day_number, cert_type='start'
            ).exists()
            end_done = Certification.objects.filter(
                slot=slot, day_number=day_number, cert_type='end'
            ).exists()

            # 3일 다 완료됐는지 확인
            if start_done and end_done:
                completed_days = 0
                for day in range(1, slot.relay.days_per_runner + 1):
                    s = Certification.objects.filter(slot=slot, day_number=day, cert_type='start').exists()
                    e = Certification.objects.filter(slot=slot, day_number=day, cert_type='end').exists()
                    if s and e:
                        completed_days += 1

                if completed_days == slot.relay.days_per_runner:
                    # 바톤터치 완료
                    slot.status = 'done'
                    slot.save()

                    # 다음 주자 running으로 변경
                    next_slot = RelaySlot.objects.filter(
                        relay=slot.relay,
                        order=slot.order + 1
                    ).first()
                    if next_slot:
                        now = timezone.now()
                        next_slot.status = 'running'
                        next_slot.start_date = now.date()
                        next_slot.end_date = now.date() + timezone.timedelta(days=slot.relay.days_per_runner - 1)
                        next_slot.deadline = now + timezone.timedelta(days=slot.relay.days_per_runner)
                        next_slot.save()

        return redirect('certification', slot_id=slot.id)

    context = {
        'slot': slot,
        'day_number': day_number,
        'today_start': today_start,
        'today_end': today_end,
    }
    return render(request, 'relay/certification.html', context)