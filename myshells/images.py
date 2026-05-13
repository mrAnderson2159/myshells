from PIL import Image, ImageDraw, ImageFont
# Questo programma prende una stringa
# e la trasforma in un'immagine png

def create_image(name:str):
    width,height = 2160, 3840
    img = Image.new('RGBA',(width,height), color=(0,0,0,0))
    d = ImageDraw.Draw(img)
    fnt_size = 300
    fnt = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', fnt_size)
    offset = 1 * len(name)
    d.text((width - (fnt_size + offset * fnt_size * 0.5) ,height - fnt_size * 2), name, font=fnt, fill=(255,255,255))

    img.save(f"counter/image{name}.png")

for i in range(1, 101):
    create_image(str(i))
