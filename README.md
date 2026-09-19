# جشنواره نفس‌های آینده

سامانه RTL فارسی جشنواره با FastAPI، Jinja2، SQLAlchemy و JavaScript خام.

## امکانات پیاده‌سازی‌شده
- طراحی بصری بهبود‌یافته، micro-animation و پشتیبانی `prefers-reduced-motion`
- گالری پوستر با fullscreen/lightbox و کلیدهای جهت‌دار
- پیش‌نمایش تصویر/ویدئو/PDF، نمایش حجم فایل و progress واقعی آپلود
- احراز هویت مدیر با session، رمز عبور و CSRF برای عملیات مدیریتی
- مدیریت آثار: جستجو، فیلتر وضعیت/محور و تغییر وضعیت
- مدیریت برگزیدگان: افزودن، انتشار/مخفی‌سازی و حذف
- آمار مدیریتی آثار، وضعیت‌ها و برگزیدگان
- انتقال خودکار سه‌مرحله‌ای `countdown → festival → winners`
- جلوگیری از ارسال اثر بعد از پایان جشنواره
- Docker + PostgreSQL + Nginx و آماده‌سازی HTTPS/domain
- endpoint سلامت `/health`
- responsive/mobile improvements

## اجرا
```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

سپس `http://127.0.0.1:8000` را باز کنید.

## ورود مدیر
`/admin/login`

مقادیر `ADMIN_USERNAME` و `ADMIN_PASSWORD` را در `.env` تغییر دهید. برای محیط production بهتر است به جای `ADMIN_PASSWORD` از `ADMIN_PASSWORD_HASH` استفاده شود:

```bash
python scripts_generate_password_hash.py "your-password"
```

## Docker production
1. `.env.example` را به `.env` تبدیل کنید و secretها، دامنه و تاریخ‌ها را تغییر دهید.
2. در `docker-compose.yml` رمز PostgreSQL را نیز تغییر دهید.
3. `deploy/nginx.conf` را با دامنه واقعی تنظیم کنید.
4. certificate معتبر Let's Encrypt برای دامنه بگیرید و بخش HTTPS کانفیگ Nginx را فعال کنید.
5. اجرا:

```bash
docker compose up -d --build
```

`SESSION_HTTPS_ONLY=true` فقط زمانی فعال باشد که سایت واقعاً پشت HTTPS سرو شود.

## Winner selection workflow

From the admin dashboard, approve a submission and then select it under **انتخاب و مدیریت برگزیدگان**. The winner is created from that submission automatically:

- participant name is reused
- category is reused
- work title is reused
- the original uploaded file is reused (no second upload)
- the original description is used unless the admin enters replacement text
- a preview is shown before confirmation
- the source submission ID is stored so the same submission cannot be selected twice

Published winners are visible immediately on `/winners` and in the home-page winner preview by default. Set `WINNERS_VISIBLE_BEFORE_END=false` in `.env` if public winner visibility should wait until the festival end date.
