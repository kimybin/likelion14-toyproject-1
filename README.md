# 🚩 작심삼인
> 중도 포기 없는 완주 경험을 제공하는 릴레이 습관 서비스
<img width="3840" height="2160" alt="첫페이지" src="https://github.com/user-attachments/assets/10d21887-49ea-4fe6-bf24-f577ca3fb5b2" />
<br>


# ✅ 프로젝트 소개 
- **작심삼인**은 3인이 하나의 목표를 릴레이 방식으로 이어가며 습관을 형성하는 팀 기반 습관 관리 애플리케이션입니다. 혼자 목표를 실천하며 동기부여가 떨어지고 중도 포기하는 문제를 해결하기 위해 기획되었습니다. 사용자는 부담 없는 3일간의 짧은 목표를 수행한 뒤 다음 주자에게 바톤을 전달하며 목표를 이어 나갑니다. 팀원들은 서로의 진행 상황을 공유하고 응원하며 책임감과 성취감을 얻을 수 있고 이를 통해 **지속적인 습관 형성**을 경험할 수 있습니다. 
<br>

# 👩🏻‍💻 팀원 구성
| 역할 | 이름 |
| --- | --- | 
| PM/Design | 고은서 |
| Front-end | 김민솔 | 
| Back-end | 김유빈, 윤예원 | 
<br>

# 💻 기술 스택
- PM/Design | Figma
- Front-end | HTML, CSS, JavaScript
- Back-end | Python, Django
<br>

# ⏱️ 개발 기간
- 2026.05.13 ~ 2026.06.01
<br>

# 🔍 페이지 간단 소개

### 로그인/회원가입
<img width="3840" height="2160" alt="온보딩-7" src="https://github.com/user-attachments/assets/db330763-d494-441d-ab95-59d6d891f455" />

### 온보딩
<img width="3840" height="2160" alt="온보딩" src="https://github.com/user-attachments/assets/2f1b5ac6-f259-448b-a81a-7cfb5b967d5d" />
<img width="3840" height="2160" alt="온보딩-8" src="https://github.com/user-attachments/assets/79793139-63b7-4cf1-af83-76980bb94b2e" />

### 홈 페이지 
<img width="3840" height="2160" alt="온보딩-3" src="https://github.com/user-attachments/assets/2e5c649b-3b4c-432e-b789-8efaac28535b" />

### 랭킹 페이지 - 개발 미완료 
<img width="3840" height="2160" alt="온보딩-6" src="https://github.com/user-attachments/assets/ad9adc38-99fb-4e7b-b17d-9608c5465244" />

### 인증 페이지
<img width="3840" height="2160" alt="온보딩-3" src="https://github.com/user-attachments/assets/44183790-b9a0-4c18-8966-2718421abf40" />
<img width="3840" height="2160" alt="온보딩-4" src="https://github.com/user-attachments/assets/10830b7c-1f93-437e-973e-2923f0c7fabf" />

### 채팅 페이지 - 개발 미완료
<img width="3840" height="2160" alt="온보딩-5" src="https://github.com/user-attachments/assets/e55948d2-494e-4224-a2f6-de07ae71a63a" />
<br>

# ⚙️ 프로젝트 초기 세팅
```bash
1.프로젝트 클론
git clone https://github.com/kimybin/likelion14-toyproject-1.git
cd likelion14-toyproject-1

2. 가상환경 생성 및 실행
$ python -m venv venv
source venv/bin/activate

3. 필수 패키지 설치
pip install -r requirements.txt

4. 데이터베이스 마이그레이션
python manage.py migrate

5. 서버 실행
python manage.py runserver
```
<br>


# 📁 파일 구조
```bash
🦁 likelion14-toyproject-1/
├── 📁 accounts/     # 유저 계정 관련 앱
├── 📁 config/       # Django 프로젝트 설정 파일
├── 📁 home/         # 메인 홈 앱
├── 📁 media/        # 업로드 미디어 파일
├── 📁 mypage/       # 마이페이지 앱
├── 📁 rank/         # 랭킹 관련 앱 - 개발 미완료 
├── 📁 relay/        # 릴레이 인증 앱
├── 📁 static/       # 정적 파일 (css, js, 이미지)
├── 📁 templates/    # HTML 템플릿 파일
├── manage.py        # Django 프로젝트 관리 스크립트
├── .gitignore       # Git 제외 파일 목록
└── README.md        # 프로젝트 설명 파일
```
