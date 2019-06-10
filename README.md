# soMedia
<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangomade124x25.gif" border="0" alt="Made with Django." title="Made with Django." /></a>
![ScreenShot](/libs/static/images/page-shot.png)

A simple social Media Application for sharing images amongst users. This application was developed for teaching django to new learners and to expose them to the numerous functionalities of django.

## Features
- Registration
- Login
- Profile Editing
- Custom User Model
- Working with ModelForms and normal Forms
- Simple TemplateTags
- Managing Admin
- Simple Signals
- Add Posts
- Add Comments to Posts
- Follow other Users to view their Posts
- Unfollowing Followed Users
- Simple Bootstrap
- View Other Users Profile

## Installation
### Create a Virtualenv
- Windows
```bash
  pip install virtualenv
  virtualenv .venv
  .venv/Scripts/activate.bat
```

- Linux
```bash
  sudo pip3 install virtualenv
  virtualenv .venv -p python3
  source .venv/bin/activate
```

### Install Requirements
```bash
  pip install -r requirements.txt
```

### Start Up server
```bash
  python manage.py runserver
```
The application should be available at http://localhost:8000/ through your browser

## Todo
- More Documentation
- More Tests
