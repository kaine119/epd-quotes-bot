from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_quote_image(path, text: str, author: str = "wuping"):
    image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    font_size = 85
    quote_array = f'"{text}"'.split(" ")
    current_year = datetime.now().year
    yr = str(current_year)
    if yr[-3] == '0':
        yr = yr[:-3] + 'k' + yr[-2:]

    while font_size > 10:

        stroke = int(font_size*0.142)
        font = ImageFont.truetype("./DINCondensed-Regular.ttf", font_size)
        current_text = ""

        for word in quote_array:
            _, _, right, _ = draw.textbbox((20, 400), current_text + word + " ", stroke_width=stroke, font=font)
            if right > 512:
                current_text += "\n"
            current_text += word + " "

        ### BYLINE
        byline = f"-{author}, {yr}"
        max_line = len(byline)
        right = 0
        _, _, right, _ = draw.textbbox((20, 400), byline, stroke_width=stroke, font=font)
        if right > 512-stroke:
            font_size = font_size//1.1
            continue
        while right < 512-stroke:
            max_line += 1
            _, _, right, _ = draw.textbbox((20, 400), byline.rjust(max_line), stroke_width=stroke, font=font)
        current_text += '\n' + byline.rjust(max_line)
        
        ### CHECK BOUNDS

        _, top, _, bottom = draw.textbbox((20, 400), current_text, stroke_width=stroke, font=font)
        if bottom - top > 512:
            font_size = font_size//1.1
        else:
            break

    _, _, _, height = draw.textbbox((12, -5), current_text, stroke_width=stroke, font=font)
    draw.text((20, (512 - height) / 2), current_text, fill=(37, 33, 58, 255), stroke_fill=(255, 255, 255, 255), stroke_width=stroke, font=font)

    image.save(path)


if __name__ == "__main__":
    create_quote_image("./out.png", "just believe what I talk about")
