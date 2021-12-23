# CHAT SERVER

## Purpose Of Project

[edit . 2021-12-23]

- Web Socket 을 이용한 백엔드 구성하는 것을 공부하기 위함

## Project Introduce

[edit . 2021-12-23]

- Django 를 asgi 를 이용한 Web Socket 를 구현
- wss 적용을 위한 daphne 사용

## Service Address

[edit . 2021-12-23]

??

## Project Duration

[edit . 2021-12-23]

2021-12-23 ~

## Technologies Used

[edit . 2021-12-23]

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

## Deploy

[edit . 2021-12-23]

![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) 

## CI/CD

[edit . 2021-12-23]

![GitHub Actions](https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Developer Information

[edit . 2021-12-23]

#### Developer

##### 👨‍🦱 이창우 (Lee Chang Woo)

- Github : https://github.com/cwadven

## Project Structure

[edit . 2021-12-23]

```
Project Root
├── 📂 config
│    ├── 📜 settings.py
│    ├── 🔒 ENV.py
│    ├── 📜 asgi.py
│    ├── 📜 urls.py
│    └── 📜 wsgi.py
│
├── 📂 App Name
│    ├── 📂 migrations                                                      
│    ├── 📜 admin.py                                
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    ├── 📜 tests.py
│    ├── 📜 urls.py
│    ├── 📜 views.py
│    └── 📜 modles.py                                     
│
├── 📂 App Name
│    ├── 📂 migrations                                     
│    ├── 📜 admin.py                                  
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    ├── 📜 tests.py
│    ├── 📜 urls.py
│    ├── 📜 views.py
│    └── 📜 modles.py  
│  
├── 📂 App Name
│    ├── 📂 migrations                                     
│    ├── 📜 admin.py                                  
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    └ .....
│
├── 📂 temp_static
│    ├── 🖼 XXXXX.png                                     
│    ├── 🖼 XXXXX.png                                  
│    ├── 🖼 XXXXX.png
│    ├── 🖼 XXXXX.png
│    └ .....
│
├── 📂 templates
│    └── base.html    
│
├── 🗑 .gitignore                                        # gitignore
├── 🗑 requirements.txt                                  # requirements.txt
└── 📋 README.md                                        # Readme
```

## Database Structure

[edit . 2021-12-23]

## 나도 만들고 싶다 하면!! 이용하는 방법

```text
1. ENV.py 를 만들어 자신의 SECRET_KEY 를 만들어라
2. "python manage.py migrate" 로 데이터베이스를 최신화 시켜줘라
3. "python manage.py createsuperuser" 로 슈퍼 유저를 만들어라
4. "python manage.py collectstatic" 로 정적 파일을 받아라
5. Redis 를 설치한 후, Redis 서버를 켜라
6. Daphne 를 설치하
.... 추후 추가
```
