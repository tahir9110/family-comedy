import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

def create_crisp_watermark():
    # Create an ultra-clean, broadcast-grade corner watermark bug for 9:16 vertical videos
    # Like HUM TV or ARY Digital corner bugs: circular glass badge with the 3D gold/emerald family emblem
    logo = Image.open("output/branding/channel_logo.jpg").convert("RGBA")
    
    # 512 x 512 high resolution
    size = 512
    badge = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(badge)
    
    # Rounded rectangular / circular translucent glass capsule
    # Margin 15px
    box = [20, 20, size - 20, size - 20]
    
    # Subtle dark emerald-black translucent glass backing with gold border
    b_draw.rounded_rectangle(box, radius=90, fill=(10, 25, 20, 190), outline=(245, 197, 24, 230), width=4)
    # Inner accent line
    inner_box = [30, 30, size - 30, size - 30]
    b_draw.rounded_rectangle(inner_box, radius=80, outline=(40, 110, 85, 160), width=2)
    
    # Crop the central 3D emblem and text from channel_logo.jpg
    # In 1024x1024 channel_logo.jpg, the emblem & text occupy roughly (200, 120, 824, 880)
    logo_crop = logo.crop((180, 120, 844, 890))
    logo_resized = logo_crop.resize((size - 80, size - 80), Image.Resampling.LANCZOS)
    
    # Make a circular/rounded mask for the logo content so it fits cleanly inside the badge
    mask = Image.new("L", (logo_resized.width, logo_resized.height), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, logo_resized.width, logo_resized.height], radius=70, fill=255)
    
    badge.paste(logo_resized, (40, 40), mask)
    
    out_wm = "output/branding/channel_logo_watermark_9_16.png"
    badge.save(out_wm, "PNG")
    print("Created broadcast-grade transparent watermark badge at:", out_wm)

def create_polished_vertical_cover():
    banner = Image.open("output/branding/channel_banner_cover.jpg").convert("RGBA")
    logo = Image.open("output/branding/channel_logo.jpg").convert("RGBA")
    
    # 9:16 Vertical HD Canvas (1080 x 1920)
    w, h = 1080, 1920
    
    # 1. Background: Warm luxury Pakistani living room gradient
    bg = Image.new("RGBA", (w, h), (14, 28, 22, 255))
    draw = ImageDraw.Draw(bg)
    
    # Smooth vertical gradient (rich dark emerald at edges to warm illuminated glow in center)
    for y in range(h):
        # Calculate lighting curve
        if y < 600:
            factor = y / 600.0
            r = int(12 + factor * 22)
            g = int(24 + factor * 28)
            b = int(20 + factor * 22)
        elif y < 1400:
            factor = (y - 600) / 800.0
            r = int(34 - factor * 14)
            g = int(52 - factor * 22)
            b = int(42 - factor * 18)
        else:
            factor = (y - 1400) / 520.0
            r = int(20 - factor * 10)
            g = int(30 - factor * 16)
            b = int(24 - factor * 12)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
    # Add a warm ambient radial glow in the center for the family
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    center_y = 1050
    for rad in range(650, 0, -25):
        alpha = int(35 * (1.0 - rad / 650.0))
        g_draw.ellipse([w//2 - rad, center_y - rad, w//2 + rad, center_y + rad], fill=(230, 190, 110, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    bg = Image.alpha_composite(bg, glow)
    
    # 2. Extract Family from banner cleanly
    # In 1376 x 768 banner, the family is at x: 190 to 1180, y: 220 to 768
    chars = banner.crop((190, 220, 1180, 768))
    # Scale family to fill 1000px width
    target_w = 1000
    target_h = int(chars.height * (target_w / chars.width))
    chars_resized = chars.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Smooth blend mask for family so bottom and top fade into the background seamlessly
    char_mask = Image.new("L", (target_w, target_h), 255)
    c_draw = ImageDraw.Draw(char_mask)
    # Feather top
    for y in range(40):
        c_draw.line([(0, y), (target_w, y)], fill=int(255 * (y / 40.0)))
    # Feather bottom
    for y in range(target_h - 140, target_h):
        c_draw.line([(0, y), (target_w, y)], fill=int(255 * (1.0 - (y - (target_h - 140)) / 140.0)))
        
    chars_resized.putalpha(char_mask)
    char_x = (w - target_w) // 2
    char_y = 660
    bg.paste(chars_resized, (char_x, char_y), chars_resized)
    
    # 3. Top Branding Section: 3D Channel Logo & Title
    # Use the pristine emblem & typography from channel_logo.jpg
    # Crop central emblem
    logo_crop = logo.crop((150, 100, 874, 900))
    l_w = 480
    l_h = int(logo_crop.height * (l_w / logo_crop.width))
    logo_resized = logo_crop.resize((l_w, l_h), Image.Resampling.LANCZOS)
    
    # Circular soft drop shadow behind the logo
    l_x = (w - l_w) // 2
    l_y = 110
    
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    sh_draw.ellipse([l_x - 30, l_y - 20, l_x + l_w + 30, l_y + l_h + 30], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(25))
    bg = Image.alpha_composite(bg, shadow)
    
    # Paste logo cleanly
    # Mask to keep only the circular emblem & typography
    l_mask = Image.new("L", (l_w, l_h), 255)
    lm_draw = ImageDraw.Draw(l_mask)
    for y in range(20):
        lm_draw.line([(0, y), (l_w, y)], fill=int(255 * (y / 20.0)))
        lm_draw.line([(0, l_h - 1 - y), (l_w, l_h - 1 - y)], fill=int(255 * (y / 20.0)))
    logo_resized.putalpha(l_mask)
    bg.paste(logo_resized, (l_x, l_y), logo_resized)
    
    # 4. Text and Badges
    final_draw = ImageDraw.Draw(bg)
    font_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
    font_urdu = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 34)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
    
    # Top subtitle under logo
    tagline = "OFFICIAL PAKISTANI COMEDY SITCOM"
    t_bbox = final_draw.textbbox((0, 0), tagline, font=font_small)
    t_w = t_bbox[2] - t_bbox[0]
    final_draw.text(((w - t_w) // 2, l_y + l_h + 10), tagline, font=font_small, fill=(245, 197, 24))
    
    # Bottom container (Shorts UI Safe Area)
    bot_y = 1480
    final_draw.rounded_rectangle([70, bot_y, w - 70, bot_y + 250], radius=28, fill=(10, 24, 18, 235), outline=(210, 165, 30), width=2)
    
    h1 = "DAILY COMEDY SHORTS"
    h1_bbox = final_draw.textbbox((0, 0), h1, font=font_bold)
    final_draw.text(((w - (h1_bbox[2] - h1_bbox[0])) // 2, bot_y + 35), h1, font=font_bold, fill=(255, 215, 0))
    
    # Urdu line
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        u_text = get_display(arabic_reshaper.reshape("ہنسی اور مزاح سے بھرپور فیملی ڈراما"))
        u_bbox = final_draw.textbbox((0, 0), u_text, font=font_urdu)
        final_draw.text(((w - (u_bbox[2] - u_bbox[0])) // 2, bot_y + 100), u_text, font=font_urdu, fill=(255, 255, 255))
    except:
        pass
        
    p_text = "YouTube Shorts  •  Instagram Reels  •  TikTok"
    p_bbox = final_draw.textbbox((0, 0), p_text, font=font_small)
    final_draw.text(((w - (p_bbox[2] - p_bbox[0])) // 2, bot_y + 180), p_text, font=font_small, fill=(180, 215, 195))
    
    # Outer luxury gold border
    final_draw.rectangle([18, 18, w - 18, h - 18], outline=(200, 160, 40), width=3)
    final_draw.rectangle([28, 28, w - 28, h - 28], outline=(35, 80, 60), width=2)
    
    out_cover = "output/branding/channel_banner_cover_9_16.jpg"
    bg.convert("RGB").save(out_cover, quality=95)
    print("Created polished 9:16 vertical cover at:", out_cover)

if __name__ == "__main__":
    create_crisp_watermark()
    create_polished_vertical_cover()
