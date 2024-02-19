from PIL import Image, ImageDraw, ImageFont

def create_quote_image(path, text: str, author: str = "wuping"):
    image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("./DINCondensed-Regular.ttf", 85)

    quote_array = f'"{text}"'.split(" ")
    current_text = ""

    for word in quote_array:
        left, top, right, bottom = draw.textbbox((20, 400), current_text + word + " ", stroke_width=12, font=font)
        if right > 512:
            current_text += "\n"
        current_text += word + " "

    current_text += f"\n    -{author} 2k24"

    _, _, _, height = draw.textbbox((12, -5), current_text, stroke_width=12, font=font)

    draw.text((20, (512 - height) / 2), current_text, fill=(37, 33, 58, 255), stroke_fill=(255, 255, 255, 255), stroke_width=12, font=font)

    image.save(path)


if __name__ == "__main__":
    create_quote_image("./out.png", "just believe what I talk about")
