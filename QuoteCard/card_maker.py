import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class CardMaker:
    def __init__(self, json_data, font_path):
        self.data = json.loads(json_data)
        self.font_path = font_path

    def create_card(self, output_path):
        # 加载封面图片并应用模糊滤镜
        cover_image = Image.open(self.data["book_cover"])
        cover_image = cover_image.filter(ImageFilter.GaussianBlur(40))

        # 计算合适的尺寸以填充背景
        width, height = cover_image.size
        target_width, target_height = 800, 600
        ratio = max(target_width / width, target_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        cover_image = cover_image.resize(new_size, Image.Resampling.LANCZOS)

        # 如果尺寸不匹配，则进行裁剪
        if new_size[0] != target_width or new_size[1] != target_height:
            cover_image = self.crop_to_fit(cover_image, target_width, target_height)

        # 创建一个同样大小的图像用于绘画
        img = Image.new("RGB", (800, 600))
        img.paste(cover_image)

        # 继续之前的步骤
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font_path, 24)

        # 添加文本和图片，文本颜色改为白色提高对比度
        d.text((60, 50), self.data["quote"], fill="black", font=font)
        d.text((610, 240), self.data["speaker"], fill="black", font=font)

        # 粘贴书籍封面的缩略图
        cover_thumbnail = Image.open(self.data["book_cover"])
        cover_thumbnail.thumbnail((150, 200))
        img.paste(cover_thumbnail, (50, 290), cover_thumbnail.convert("RGBA"))

        # 添加书籍信息文本
        d.multiline_text(
            (220, 300), self.data["book_info"], fill="black", font=font, spacing=5
        )

        # 保存图像
        img.save(output_path)

    def crop_to_fit(self, image, target_width, target_height):
        """
        图片按比例缩放后，如果不符合目标尺寸，则从中间裁剪到目标大小。
        """
        width, height = image.size
        top = (height - target_height) // 2
        left = (width - target_width) // 2
        right = (width + target_width) // 2
        bottom = (height + target_height) // 2
        return image.crop((left, top, right, bottom))


if __name__ == "__main__":
    # 假设JSON数据和字体文件路径如下
    json_data = """
    {
        "quote": "这里是引用的内容...",
        "speaker": "发言人姓名",
        "book_cover": "QuoteCard/classroom-of-the-elite.webp",
        "book_info": "书名 作者 出版社"
    }
    """
    font_path = "fonts/SourceHanSansSC-VF.ttf"

    # 创建CardMaker实例
    card_maker = CardMaker(json_data, font_path)

    # 生成卡片，并保存到文件
    card_maker.create_card("book_summary.png")
