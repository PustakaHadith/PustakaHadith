"""Jana logo Store untuk MSIX — guna Pillow untuk kertas PNG."""

from PIL import Image, ImageDraw, ImageFont
import os

ASSETS = os.path.join(os.path.dirname(__file__), "Assets")
os.makedirs(ASSETS, exist_ok=True)

# Saiz logo yang diperlukan
LOGOS = {
    "Square44x44Logo.png": 44,
    "Square71x71Logo.png": 71,
    "Square150x150Logo.png": 150,
    "Square310x310Logo.png": 310,
    "Wide310x150Logo.png": (310, 150),
    "SplashScreen.png": (620, 300),
    "StoreLogo.png": 50,
}

def jana_logo(nama, saiz, warna="#1B5E20", teks="PH"):
    """Jana PNG logo ringkas dengan teks."""
    if isinstance(saiz, tuple):
        img = Image.new("RGBA", saiz, (0, 0, 0, 0))
    else:
        img = Image.new("RGBA", (saiz, saiz), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Latar belakang bulat/petak
    if isinstance(saiz, tuple):
        draw.rectangle([0, 0, w-1, h-1], fill=warna)
    else:
        draw.ellipse([0, 0, w-1, h-1], fill=warna)
    
    # Teks
    try:
        font_size = int(min(w, h) * 0.4)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), teks, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (w - tw) // 2
    y = (h - th) // 2
    draw.text((x, y), teks, fill="white", font=font)
    
    path = os.path.join(ASSETS, nama)
    img.save(path, "PNG")
    print(f"  OK {nama} ({w}x{h})")

if __name__ == "__main__":
    print("Menjana logo Store...")
    for nama, saiz in LOGOS.items():
        jana_logo(nama, saiz)
    print("Selesai! Logo disimpan di msix/Assets/")
