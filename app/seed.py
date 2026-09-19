from sqlalchemy import select
from .models import Category, Poster, Prize, ParticipantGroup, SocialLink, Winner

def seed_database(db):
    if db.scalar(select(Category).limit(1)):
        return

    categories = [
        Category(slug="photo", title="عکس", icon="📷",
                 description="لحظه‌هایی واقعی از عشق، خانواده، امید و زندگی.",
                 rules="اثر باید متعلق به شرکت‌کننده باشد. ارسال عکس با کیفیت مناسب و بدون محتوای خلاف قوانین جشنواره انجام شود."),
        Category(slug="caricature", title="کاریکاتور", icon="🎨",
                 description="نگاهی خلاقانه، طنزآمیز و انسانی به زندگی و آینده.",
                 rules="اثر باید اصیل باشد و حقوق پدیدآورنده رعایت شود. آثار توهین‌آمیز یا ناقض حقوق اشخاص پذیرفته نمی‌شوند."),
        Category(slug="poster", title="پوستر", icon="🖼️",
                 description="یک پیام تصویری برای ساختن فردایی روشن‌تر.",
                 rules="پوستر باید خوانا، خلاقانه و مرتبط با موضوع جشنواره باشد. استفاده از محتوای دارای حق نشر بدون اجازه مجاز نیست."),
        Category(slug="drawing", title="نقاشی", icon="🖌️",
                 description="تصویری از آینده از نگاه کودکان، نوجوانان و هنرمندان.",
                 rules="آثار دستی یا دیجیتال پذیرفته می‌شوند. در آثار کودکان، اطلاعات قیم یا سرپرست باید با اجازه ارسال شود."),
        Category(slug="short-media", title="رسانه کوتاه", icon="🎬",
                 description="کلیپ کوتاه، روایت تصویری و لحظه‌ای که نفس امید را زنده می‌کند.",
                 rules="ویدئو باید کوتاه و با فرمت MP4، MOV یا WEBM باشد. موسیقی و تصاویر دارای حق نشر باید مجوز مناسب داشته باشند."),
        Category(slug="short-story", title="داستان کوتاه", icon="📖",
                 description="روایتی کوتاه از عشق، خانواده، امید و آینده.",
                 rules="داستان باید اصیل باشد و قبلاً بدون اجازه صاحب اثر منتشر نشده باشد. متن فارسی در قالب PDF ارسال شود."),
    ]
    db.add_all(categories)

    posters = [
        Poster(title="نفس‌های آینده", subtitle="برای فردایی روشن‌تر", image_path="/static/images/posters/poster-1.svg"),
        Poster(title="آغاز یک زندگی", subtitle="قصه‌ای برای همیشه", image_path="/static/images/posters/poster-2.svg"),
        Poster(title="امن‌ترین پناه", subtitle="خانواده", image_path="/static/images/posters/poster-3.svg"),
        Poster(title="نسل‌های کنار هم", subtitle="از لبخند تا خاطره", image_path="/static/images/posters/poster-4.svg"),
    ]
    db.add_all(posters)

    prizes = [
        Prize(title="نفر اول هر محور", description="تندیس جشنواره، لوح تقدیر و جایزه ویژه نقدی.", icon="🥇", sort_order=1),
        Prize(title="نفر دوم هر محور", description="لوح تقدیر و جایزه نقدی.", icon="🥈", sort_order=2),
        Prize(title="نفر سوم هر محور", description="لوح تقدیر و هدیه یادبود جشنواره.", icon="🥉", sort_order=3),
    ]
    db.add_all(prizes)

    groups = [
        ParticipantGroup(title="کودکان و نوجوانان", description="با همراهی والدین یا سرپرست قانونی.", icon="🧒"),
        ParticipantGroup(title="جوانان", description="برای علاقه‌مندان به هنر، رسانه و روایت.", icon="🌱"),
        ParticipantGroup(title="خانواده‌ها", description="ارسال آثار خانوادگی و تجربه‌های مشترک.", icon="👨‍👩‍👧‍👦"),
        ParticipantGroup(title="هنرمندان و فعالان فرهنگی", description="برای عکاسان، طراحان، نویسندگان و تولیدکنندگان محتوا.", icon="🎭"),
    ]
    db.add_all(groups)

    socials = [
        SocialLink(title="اینستاگرام", url="https://instagram.com/", icon="◎"),
        SocialLink(title="تلگرام", url="https://t.me/", icon="✈"),
        SocialLink(title="آپارات", url="https://www.aparat.com/", icon="▶"),
        SocialLink(title="لینکدین", url="https://www.linkedin.com/", icon="in"),
    ]
    db.add_all(socials)

    db.commit()
