# Render 배포 안내

이 문서는 노래방 점수 분석 프로그램 PLUS를 Render에 배포하는 방법을 정리한 문서입니다. 현재 제출용 웹사이트는 아래 주소로 배포되어 있습니다.

https://karaoke-score-analyzer.onrender.com

## 1. 배포 개요

이 프로젝트는 Flask로 만든 웹 애플리케이션이며, GitHub 저장소를 Render Web Service와 연결하여 외부에서 접속할 수 있도록 배포했습니다.

Render에 올리기 위해 프로젝트에는 다음 파일들이 포함되어 있습니다.

```text
requirements.txt
Procfile
runtime.txt
app.py
```

각 파일의 역할은 다음과 같습니다.

- `requirements.txt`: Flask와 Gunicorn 등 필요한 패키지 목록
- `Procfile`: Render에서 서버를 실행할 명령어 지정
- `runtime.txt`: Python 실행 버전 지정
- `app.py`: 실제 Flask 애플리케이션 파일

## 2. 현재 Render 설정값

Render에서 Web Service를 만들 때 사용한 주요 설정은 다음과 같습니다.

```text
Service Type: Web Service
Language: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Root Directory: 비워둠
Plan: Free
```

GitHub 저장소의 최상위 위치에 `app.py`, `requirements.txt`, `Procfile`, `runtime.txt`가 바로 보이는 구조이므로 Root Directory는 비워두었습니다.

## 3. 배포 후 접속 방법

배포가 완료되면 아래 주소로 접속할 수 있습니다.

https://karaoke-score-analyzer.onrender.com

Render 무료 플랜에서는 일정 시간 접속이 없으면 서버가 잠시 대기 상태가 됩니다. 이 경우 첫 접속 시 화면이 뜨기까지 약간의 시간이 걸릴 수 있습니다. 기다리면 서버가 다시 켜지고 정상적으로 접속됩니다.

## 4. 수정사항을 외부 사이트에 반영하는 방법

프로그램 파일을 수정한 경우 GitHub에 다시 올리고 커밋하면 Render가 자동으로 새 버전을 배포합니다.

일반적인 반영 순서는 다음과 같습니다.

```text
1. 로컬 컴퓨터에서 파일 수정
2. GitHub 저장소에 수정 파일 업로드
3. Commit changes 클릭
4. Render가 자동으로 배포 진행
5. 외부 URL에서 수정 결과 확인
```

자동 배포가 바로 진행되지 않을 경우 Render 대시보드에서 아래 메뉴를 사용할 수 있습니다.

```text
Manual Deploy → Deploy latest commit
```

## 5. 로컬 실행 방법

외부 배포 사이트와 별개로, 프로젝트는 로컬 컴퓨터에서도 실행할 수 있습니다.

```bash
py -m pip install -r requirements.txt
py app.py
```

그 후 브라우저에서 아래 주소로 접속합니다.

http://127.0.0.1:5000

이 방식은 외부 사이트가 일시적으로 느리거나 접속되지 않을 때를 대비한 예비 실행 방법입니다.
