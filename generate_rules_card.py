import os
import sys
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def get_font_path():
    font_candidates = [
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for p in font_candidates:
        if os.path.exists(p):
            return p
    return "C:/Windows/Fonts/arial.ttf"

def reshape_urdu(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def create_card():
    font_path = get_font_path()
    
    # Crisp 1200 x 2050 resolution
    width = 1200
    height = 2050
    
    # Rich Dark Emerald & Gold Luxury Theme
    bg_color = (10, 26, 20)          # Ultra dark emerald
    card_bg = (16, 40, 31)           # Elegant emerald card
    gold = (245, 197, 24)            # Radiant Gold
    gold_border = (190, 150, 30)
    white = (255, 255, 255)
    light_gray = (220, 230, 225)
    accent_green = (34, 197, 94)
    
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Double Outer Borders
    draw.rectangle([20, 20, width - 20, height - 20], outline=gold_border, width=3)
    draw.rectangle([30, 30, width - 30, height - 30], outline=(30, 75, 60), width=2)
    
    # Fonts setup
    title_font = ImageFont.truetype(font_path, 48)
    sub_font = ImageFont.truetype(font_path, 26)
    card_title_font = ImageFont.truetype(font_path, 34)
    badge_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 32)
    text_font = ImageFont.truetype(font_path, 23)
    footer_font = ImageFont.truetype(font_path, 30)
    
    # Header Section
    header_box = [60, 55, width - 60, 215]
    draw.rounded_rectangle(header_box, radius=20, fill=(15, 38, 30), outline=gold, width=2)
    
    t1 = reshape_urdu("یوٹیوب مونیٹائزیشن کے ۴ سنہری اصول")
    t2 = reshape_urdu("پاکستانی فیملی کامیڈی شارٹس کو محفوظ، وائرل اور مونیٹائز کروانے کے لیے")
    
    bbox1 = draw.textbbox((0, 0), t1, font=title_font)
    draw.text(((width - (bbox1[2] - bbox1[0])) // 2, 75), t1, font=title_font, fill=gold)
    
    bbox2 = draw.textbbox((0, 0), t2, font=sub_font)
    draw.text(((width - (bbox2[2] - bbox2[0])) // 2, 150), t2, font=sub_font, fill=light_gray)
    
    cards_data = [
        {
            "num": "1",
            "title": "ویڈیو ایڈیٹنگ میں انسانی محنت کا اضافہ",
            "points": [
                "کیپ کٹ یا پریمیئر میں اردو کے اینیمیٹڈ سب ٹائٹلز لازمی لگائیں۔",
                "پیلے، سفید یا سرخ رنگ کے پاپ اپ فونٹس استعمال کریں۔",
                "ہر مزاحیہ پنچ لائن پر بلبلے اسٹائل ساؤنڈ افیکٹ یا ہنسی کی آواز ڈالیں۔",
                "اس ایڈیٹنگ سے یوٹیوب سسٹم اسے اصلی انسانی تخلیق مانے گا۔"
            ]
        },
        {
            "num": "2",
            "title": "چینل کی اپنی برانڈنگ اور واٹر مارک",
            "points": [
                "ہر ویڈیو کے ایک کونے پر چینل کا لوگو یا واٹر مارک لازمی لگائیں۔",
                "شروع یا آخر میں ایک سیکنڈ کا چینل انٹرو یا کارڈ لگائیں۔",
                "اس سے کوئی دوسرا چینل آپ کی ویڈیو چرا کر ری اپلوڈ نہیں کر سکے گا۔",
                "یوٹیوب پالیسی میں ویڈیو آپ کا اوریجنل مواد ثابت ہوگی۔"
            ]
        },
        {
            "num": "3",
            "title": "اپلوڈ کرتے وقت لازمی سیٹنگ",
            "points": [
                "ویڈیو اپلوڈ کے دوران سوال آتا ہے: Altered or synthetic content",
                "اس سوال پر ہمیشہ لازمی 'YES' منتخب کریں۔",
                "اس سے یوٹیوب ویڈیو کو محفوظ اور پالیسی کے مطابق تسلیم کرے گا۔",
                "چینل کو کبھی بھی اسٹرائیک یا ری یوزڈ کونٹینٹ کا مسئلہ نہیں آئے گا!"
            ]
        },
        {
            "num": "4",
            "title": "ٹائٹل، ڈسکرپشن اور قسط کا نمبر",
            "points": [
                "ٹائٹل میں قسط نمبر لازمی لکھیں: جیسے 'رشتہ انکار ہو گیا! :12 Ep'",
                "ڈسکرپشن میں ہر بار یہ واضح کریڈٹ لائن لازمی شامل کریں:",
                "Original Pakistani Family Sitcom. Script & Direction by Our Channel.",
                "اس سے یوٹیوب کو واضح پتہ چلے گا کہ یہ ایک مستقل اوریجنل ویب سیریز ہے۔"
            ]
        }
    ]
    
    start_y = 245
    card_height = 370
    gap = 25
    
    card_content_right = width - 110
    
    for i, c in enumerate(cards_data):
        y1 = start_y + i * (card_height + gap)
        y2 = y1 + card_height
        box = [60, y1, width - 60, y2]
        
        # Card body
        draw.rounded_rectangle(box, radius=18, fill=card_bg, outline=(40, 95, 75), width=2)
        
        # Badge on top right
        badge_box = [card_content_right - 45, y1 + 18, card_content_right + 15, y1 + 74]
        draw.rounded_rectangle(badge_box, radius=28, fill=gold, outline=gold_border, width=1)
        draw.text((card_content_right - 25, y1 + 22), c["num"], font=badge_font, fill=(15, 30, 20))
        
        # Card Title
        rtitle = reshape_urdu(c["title"])
        t_w = draw.textbbox((0, 0), rtitle, font=card_title_font)[2]
        draw.text((card_content_right - 65 - t_w, y1 + 24), rtitle, font=card_title_font, fill=gold)
        
        # Divider line
        draw.line([85, y1 + 86, width - 85, y1 + 86], fill=(32, 72, 58), width=1)
        
        # Points
        point_y = y1 + 104
        for p in c["points"]:
            # Check if line is english credit line
            if p.startswith("Original Pakistani"):
                # English text centered/aligned nicely
                e_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
                draw.rectangle([85, point_y + 2, width - 130, point_y + 40], fill=(22, 55, 42), outline=(45, 110, 85))
                draw.text((105, point_y + 10), "• " + p, font=e_font, fill=(245, 220, 110))
                point_y += 56
                continue
                
            rp = reshape_urdu(p)
            text_w = draw.textbbox((0, 0), rp, font=text_font)[2]
            
            # Green bullet dot on right
            draw.ellipse([card_content_right - 10, point_y + 12, card_content_right, point_y + 22], fill=accent_green)
            
            # Urdu text right aligned
            draw.text((card_content_right - 28 - text_w, point_y + 5), rp, font=text_font, fill=white)
            point_y += 56
            
    # Bottom Guarantee Banner
    footer_y = start_y + 4 * (card_height + gap) + 10
    footer_box = [60, footer_y, width - 60, footer_y + 105]
    draw.rounded_rectangle(footer_box, radius=18, fill=gold, outline=gold_border, width=2)
    
    footer_text = reshape_urdu("ان ۴ اصولوں پر عمل کریں تو چینل ۱۰۰ فیصد محفوظ طریقے سے مونیٹائز ہوگا!")
    f_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    draw.text(((width - (f_bbox[2] - f_bbox[0])) // 2, footer_y + 32), footer_text, font=footer_font, fill=(10, 25, 18))
    
    out_path = "D:/Family Comedy/output/youtube_monetization_rules_urdu.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        img.save(f, "PNG", quality=95)
    print("Successfully created polished HD image at:", out_path)

if __name__ == "__main__":
    create_card()
