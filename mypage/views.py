from django.shortcuts import render

# 홈 페이지 제작을 위한 임시 코드
def mypage(request):
    return render(request, 'mypage/mypage.html')