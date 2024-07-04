from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json


class CardMaker:
    def __init__(self, json_data, font_path):
        self.data = json.loads(json_data)
        self.font_path = font_path

    def create_card(self, output_path):
        # 加载封面图片并应用模糊滤镜
        cover_image = Image.open(self.data["book_cover"])
        cover_image = cover_image.filter(ImageFilter.GaussianBlur(10))  # 增加的模糊效果

        # 调整封面图片到卡片的大小，并用作背景
        cover_image = cover_image.resize((800, 600))

        # 创建一个同样大小的图像用于绘画
        img = Image.new("RGB", (800, 600))
        img.paste(cover_image)  # 使用模糊后的封面图片作为背景
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font_path, 24)

        # 绘制“引用内容”，这里不再绘制边框
        d.text(
            (60, 50), self.data["quote"], fill=(255, 255, 255), font=font
        )  # text color changed to white for visibility

        # 绘制发言人名称，不再绘制边框
        d.text(
            (610, 240), self.data["speaker"], fill=(255, 255, 255), font=font
        )  # text color changed to white for visibility

        # 缩小并粘贴封面图片到指定位置
        cover_image_small = Image.open(self.data["book_cover"])
        cover_image_small.thumbnail((150, 200))
        img.paste(
            cover_image_small, (50, 290), cover_image_small.convert("RGBA")
        )  # Use alpha channel for pasting

        # 绘制书籍信息, 不再绘制边框
        d.multiline_text(
            (220, 300),
            self.data["book_info"],
            fill=(255, 255, 255),
            font=font,
            spacing=5,
        )  # text color changed to white for visibility

        # 保存图像
        img.save(output_path)


if __name__ == "__main__":
    # 假设JSON数据和字体文件路径如下
    json_data = """
    {
        "quote": "这里是引用的内容...",
        "speaker": "发言人姓名",
        "book_cover": "book_cover.jpg",
        "book_info": "书名\n作者\n出版社"
    }
    """
    font_path = "path_to_your_font_file.ttf"

    # 创建CardMaker实例
    card_maker = CardMaker(json_data, font_path)

    # 生成卡片，并保存到文件
    card_maker.create_card("book_summary.png")
