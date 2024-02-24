import json
import os

from PIL import Image
from PIL import ImageDraw, ImageFont

try:
    from src.utils import *
except:
    from utils import *

def image_resize(size_to: tuple, image_path: str = None, img=None, save_as: str = None):
    img = img if image_path == None else Image.open(image_path)
    if img is None:
        raise Exception("image to resize not specified")

    left, bottom, right, top = get_size_to_fit_in_frame_w_ratio(
        original_frame_size=img.size, target_w_h_ratio=size_to, return_position=True
    )

    crop_img = img.crop((left, bottom, right, top))
    crop_img = crop_img.resize(size_to)
    # Shows the image in image viewer

    if save_as != None:
        crop_img.save(save_as)

    return crop_img


def paste_image_on_another(
    top_left_pos,
    bg_img_path=None,
    bg_img=None,
    paste_img_path=None,
    paste_img=None,
    save_as=None,
    transparency = 255,
):
    bg_img = Image.open(bg_img_path) if bg_img_path != None else bg_img
    paste_img = Image.open(paste_img_path) if paste_img_path != None else paste_img
    
    if bg_img == None or paste_img == None:
        raise Exception("bg_img or paste_img not specified")
    
    bg_img = bg_img.convert('RGB')
    paste_img = paste_img.convert('RGBA')
    paste_img.putalpha(transparency)
    bg_img.paste(paste_img, top_left_pos, mask=paste_img)

    if save_as != None:
        bg_img.save(save_as)

    return bg_img


def create_photobooth(
    config_path: str, background_photo: str, photos: list, save_as=None
):
    """
    background_photo path, best to resize before adding into this function, else no worries too
    photos paths, photo will be resize in thie function so do not worry just pass raw data in here
    """
    with open(config_path, "r") as json_file:
        # Load the JSON data
        config = json.load(json_file)

    print_size_inch_width = config["print_size_inch_width"]
    print_size_inch_height = config["print_size_inch_height"]
    dpi = config["dpi"]

    bg_image_width = print_size_inch_width * dpi
    bg_image_height = print_size_inch_height * dpi
    bg_img = Image.open(background_photo)
    if bg_img.size != (bg_image_width, bg_image_height):
        print("!!!resizing bg image!!! Please take a look!")
        bg_img = image_resize(
            image_path=background_photo, size_to=(bg_image_width, bg_image_height)
        )

    photo_configs = config["photos"]
    for i in range(len(photo_configs)):
        photo = photos[i]
        photo_config = photo_configs[i]
        image_to_paste = image_resize(
            size_to=(
                int(photo_config["photo_width_inch"] * dpi),
                int(photo_config["photo_height_inch"] * dpi),
            ),
            image_path=photo,
        )
        bg_img = paste_image_on_another(
            bg_img=bg_img,
            paste_img=image_to_paste,
            top_left_pos=(
                int(photo_config["photo_pos_left"] * dpi),
                int(photo_config["photo_pos_top"] * dpi),
            ),
        )

    if save_as != None:
        bg_img.save(save_as)


# def make_template_image(config_path: str, output_path: str = None):
#     with open(config_path, "r") as json_file:
#         # Load the JSON data
#         config = json.load(json_file)
#     off_set = 20
#     border_width = 20
#     print_size_inch_width = config["print_size_inch_width"]
#     print_size_inch_height = config["print_size_inch_height"]
#     dpi = config["dpi"]

#     # Create a blank image
#     image_width = print_size_inch_width * dpi + (off_set * 2)
#     image_height = print_size_inch_height * dpi + off_set * 2
#     blank_image = Image.new("RGB", (image_width, image_height), color="white")

#     # Create an ImageDraw object
#     draw = ImageDraw.Draw(blank_image)

#     # Draw Outer Borders
#     draw.rectangle(
#         (off_set, off_set, image_width - off_set, image_height - off_set),
#         outline="black",
#         width=border_width,
#     )

#     photo_boxes = []
#     for i in config["photos"]:
#         box_width = i["photo_width_inch"] * dpi
#         box_height = i["photo_height_inch"] * dpi
#         left = off_set + i["photo_pos_left"] * dpi + border_width / 2 + 1
#         right = off_set + i["photo_pos_left"] * dpi + box_width - (border_width / 2 + 1)
#         top = off_set + i["photo_pos_top"] * dpi + (border_width / 2 + 1)
#         bottom = (
#             off_set + i["photo_pos_top"] * dpi + box_height - (border_width / 2 + 1)
#         )
#         photo_boxes.append(
#             {
#                 "left": left,
#                 "right": right,
#                 "top": top,
#                 "bottom": bottom,
#             }
#         )

#     min_width = min([i["right"] - i["left"] for i in photo_boxes])
#     min_height = min([i["bottom"] - i["top"] for i in photo_boxes])
#     font_size = int(min(min_width, min_height) * 0.8)
#     font = ImageFont.truetype(
#         os.path.join(repo_dir, "assets", "ArialTh.ttf"), font_size
#     )
#     text_color = (0, 0, 0)
#     for ind, i in enumerate(photo_boxes):
#         text_to_draw = str(ind + 1)
#         draw.rectangle(
#             (i["left"], i["top"], i["right"], i["bottom"]),
#             outline="black",
#             width=border_width,
#         )
#         # text_width, text_height = draw.textsize(text_to_draw, font = font)
#         new_box = draw.textbbox((0, 0), text_to_draw, font)
#         draw.text(
#             xy=(
#                 (i["left"] + i["right"] - (new_box[2] - new_box[0])) / 2,
#                 (i["top"] + i["bottom"] - (new_box[3] - new_box[1])) / 2,
#             ),
#             text=str(ind + 1),
#             font=font,
#             align="center",
#             fill=text_color,
#         )

    # Save the image
    # if output_path:
    #     blank_image.save(output_path)


# class ImageProcessor:
#     raw_photo_input_dir = os.path.join(repo_dir, "photo_input")

#     raw_template_dir = os.path.join(repo_dir, "templates")
#     processed_template_dir = os.path.join(repo_dir, "assets", "processed_templates")
#     remove_folder(processed_template_dir)
#     template_methods = list_dirs(raw_template_dir)

#     def __init__(self) -> None:
#         pass

#     def create_template_demo_image(self):
#         print("creating template demo")
#         for template_method in self.template_methods:
#             config_file_path = os.path.join(
#                 self.raw_template_dir, template_method, "config.json"
#             )
#             processed_temple_folder = os.path.join(
#                 self.processed_template_dir, template_method
#             )
#             create_folder(processed_temple_folder)

#             demo_file_path = os.path.join(processed_temple_folder, "demo.jpg")
#             make_template_image(config_file_path, output_path=demo_file_path)

#     def process_photobooth_background_photos(self):
#         for template_method in self.template_methods:
#             config_file_path = os.path.join(
#                 self.raw_template_dir, template_method, "config.json"
#             )
#             with open(config_file_path, "r") as json_file:
#                 # Load the JSON data
#                 config = json.load(json_file)

#             raw_background_photo_dir = os.path.join(
#                 self.raw_template_dir, template_method, "background"
#             )
#             processed_background_photo_dir = os.path.join(
#                 self.processed_template_dir, template_method, "background"
#             )
#             create_folder(processed_background_photo_dir)

#             raw_all_bg_photos = list_files(raw_background_photo_dir, fp=False)
#             for bg_photo in raw_all_bg_photos:
#                 image_resize(
#                     image_path=os.path.join(raw_background_photo_dir, bg_photo),
#                     size_to=(
#                         config["print_size_inch_width"] * config["dpi"],
#                         config["print_size_inch_height"] * config["dpi"],
#                     ),
#                     save_as=os.path.join(processed_background_photo_dir, bg_photo),
#                 )

#     def create_photo_booths(self, session_id):
#         photo_booth_dir = os.path.join(repo_dir, "output", session_id, "photo_booth")
#         all_photos = list_files(self.raw_photo_input_dir, fp=True)

#         for template_method in self.template_methods:
#             config_file_path = os.path.join(
#                 self.raw_template_dir, template_method, "config.json"
#             )
#             with open(config_file_path, "r") as json_file:
#                 # Load the JSON data
#                 config = json.load(json_file)

#             background_imgs = list_files(
#                 os.path.join(self.processed_template_dir, template_method, "background")
#             )
#             for background_img in background_imgs:
#                 name, extension = os.path.splitext(background_img)
#                 phtobooth_outname = template_method + "_" + name + ".jpg"
#                 create_folder(photo_booth_dir)
#                 create_photobooth(
#                     background_photo=os.path.join(
#                         self.processed_template_dir,
#                         template_method,
#                         "background",
#                         background_img,
#                     ),
#                     config_path=config_file_path,
#                     photos=all_photos,
#                     save_as=os.path.join(photo_booth_dir, phtobooth_outname),
#                 )

#     def run(self):
#         self.create_template_demo_image()
#         self.process_photobooth_background_photos()
#         self.create_photo_booths("session123456789")


if __name__ == "__main__":
    pass
    # IP = ImageProcessor()
    # IP.run()