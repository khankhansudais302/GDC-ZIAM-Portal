# GDC ZIAM Secure Portal — Django Starter Project

Sudais bhai, yeh current static HTML demo se agla step hai: **Django + SQLite backend starter**. Is mein asli role-based login aur private record permissions ka starter implementation hai.

## Is project mein kya hai?

- Student, Teacher aur Principal/Admin ke alag dashboard.
- Login ID (student roll number ya staff ID) + password. Login page par role choose nahi hota; role database se aata hai.
- Public sign-up band hai.
- Principal account se Student aur Teacher accounts banane ka form.
- Student sirf apni complaints aur re-admission requests dekh sakta hai.
- Teacher dashboard se `principal_only` complaints query level par exclude hoti hain.
- Principal dashboard sab complaints aur re-admission applications dekh sakta hai.
- Notices, class timetables aur BISE Peshawar past-paper links.
- College photo aur dono timetable images project ke static folder mein.
- Automated tests for role permissions/privacy.

## Windows / PyCharm mein chalane ka tareeqa

1. ZIP ko extract karein.
2. Folder `GDC_ZIAM_Secure_Portal_Project` ko PyCharm mein open karein.
3. PyCharm Terminal kholein.
4. Virtual environment banayein aur activate karein:

```bat
py -m venv .venv
.venv\Scripts\activate
```

5. Dependencies install karein:

```bat
python -m pip install -r requirements.txt
```

6. App ki initial migration banayein aur database tayyar karein:

```bat
python manage.py makemigrations portal
python manage.py migrate
```

7. Principal/Admin account banayein. `createsuperuser` is project mein Principal role assign karta hai:

```bat
python manage.py createsuperuser
```

Login ID set karein (username), email optional nahin maanga jayega; phir strong password dein.

8. Development server start karein:

```bat
python manage.py runserver
```

9. Browser mein `http://127.0.0.1:8000/` kholein. Admin panel: `http://127.0.0.1:8000/admin/`.

## Accounts kaise banenge?

- Pehla Principal account command line se `createsuperuser` ke zariye banega. Is account ko sirf Principal/authorized admin ke paas rakhein.
- Principal dashboard ke `Create student / teacher account` se students aur teachers ke accounts banayein.
- Student login ID mein college roll number; teacher login ID mein college-approved staff ID use karein.
- Principal-only permission se sirf Student/Teacher roles ban sakte hain. Extra principal accounts sirf superuser admin se banayein.
- Temporary password ko safe channel se asal account owner tak pahunchayein. Reuse na karein; real use se pehle password reset/change workflow add karna chahiye.

## Privacy rules implemented in app views

- Student routes `role_required(student)` ke zariye protected hain.
- Teacher routes `role_required(teacher)` ke zariye protected hain.
- Principal routes `role_required(principal)` ke zariye protected hain.
- Login role user ke database account se check hota hai, form se nahi.
- Student dashboard uses `request.user` ke apne complaints/applications.
- Teacher query `visibility=general` filter lagati hai, so principal-only complaint server response mein include nahin hoti.
- Re-admission review principal-only hai.

## Important limitations (please read)

- Yeh **development starter** hai, abhi live college system nahin. Real student records/passwords ko bina college approval use na karein.
- Rs. 700 request mein user-provided amount ke mutabiq sample setting hai; college se amount aur payment rules confirm karein.
- College image and timetable text can be unclear; official details college se verify karein.
- Past-paper links external education websites hain; official announcements ke liye BISE Peshawar ki site verify karein.
- Study help yahan resources ka link hai; AI tutor integration is starter mein connected nahin.
- `DEBUG=1`, local secret key and SQLite are for local development only. Public hosting se pehle secure secret key, `DJANGO_DEBUG=0`, valid `DJANGO_ALLOWED_HOSTS`, HTTPS, PostgreSQL, backups, rate limiting, audit logs, staff account recovery, student import approval, and security review configure karein.
- Existing HTML demo is kept at `static/portal/legacy_student_portal_demo.html` for reference; Django pages are connected to backend routes. It is not embedded inside the Django login pages because its old form interactions were prototype-only.

## Tests

After migrations:

```bat
python manage.py test portal
```

These tests check students cannot open teacher dashboards, teachers cannot open principal dashboards, teacher queries do not show principal-only complaint text, and students see only their own complaints.
