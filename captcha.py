from PIL import Image, ImageDraw, ImageFont
import cStringIO, random

def getCaptcha():
    im = Image.new("RGB", (175, 60))
    draw = ImageDraw.Draw(im)

    for x in range(0, 175):
        for y in range(0, 60):
            draw.point((x, y), (135, 191, 107))

    font = ImageFont.truetype('static/ZXX Camo.otf', 50)

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    word = ''
    for i in range(5):
        word = word + alphabet[random.randint(0, len(alphabet) -1)]
        
    draw.text((5, 5), word, font=font, fill=(0, 0, 0))

    f = cStringIO.StringIO()
    im.save(f, "GIF")
    f.seek(0)
    return word, f