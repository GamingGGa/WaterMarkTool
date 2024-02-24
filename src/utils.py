import math
import shutil
import os


def remove_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Debug    - Folder '{folder_path}' and its contents have been removed.")
    else:
        print(f"Debug    - Folder '{folder_path}' does not exist.")


def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    print(f"Debug    - Folder '{folder_path}' and its parent directories have been created.")


def list_files(directory, fp: bool = False):
    out = []
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
        if files:
            # print(f"Files in directory '{directory}':")
            for file in files:
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    out_data = file_path if fp else file
                    out.append(out_data)
        else:
            # print(f"No files found in directory '{directory}'.")
            pass
    else:
        # print(f"Directory '{directory}' does not exist.")
        pass

    return out


def list_dirs(directory, fp: bool = False):
    out = []
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
        if files:
            for file in files:
                file_path = os.path.join(directory, file)
                if os.path.isdir(file_path):
                    out_data = file_path if fp else file
                    out.append(out_data)
        else:
            # print(f"No directory found in directory '{directory}'.")
            pass
    else:
        # print(f"Directory '{directory}' does not exist.")
        pass

    return out


def get_size_to_fit_in_frame_w_ratio(
    original_frame_size: tuple,
    target_w_h_ratio: tuple,
    return_position: bool,
):
    # get the maximum image size to fit into a frame with a target ratio
    # return_position: True => return the relative position of the maximum frame
    #    (left, top, right, bottom)
    # return_position: False => return the size as (width, height)

    # read ratios
    target_w_h_ratio = target_w_h_ratio[0] / target_w_h_ratio[1]  ## 0.33
    current_w_h_ratio = original_frame_size[0] / original_frame_size[1]  # 2

    if current_w_h_ratio > target_w_h_ratio:
        # crop vertically
        # use all height
        new_image_width = math.floor(original_frame_size[1] * target_w_h_ratio)

        pixels_to_rm = original_frame_size[0] - new_image_width
        left_to_rm = math.ceil(pixels_to_rm / 2)
        right_to_rm = math.floor(pixels_to_rm / 2)
        left = left_to_rm
        right = original_frame_size[0] - right_to_rm
        bottom = 0
        top = original_frame_size[1]

    elif current_w_h_ratio < target_w_h_ratio:
        # crop vertically
        # use all width

        new_image_height = math.floor(original_frame_size[0] / target_w_h_ratio)
        pixels_to_rm = original_frame_size[1] - new_image_height
        top_to_rm = math.ceil(pixels_to_rm / 2)
        bottom_to_rm = math.floor(pixels_to_rm / 2)
        top = original_frame_size[1] - top_to_rm
        bottom = bottom_to_rm
        left = 0
        right = original_frame_size[0]

    else:
        top = original_frame_size[1]
        bottom = 0
        left = 0
        right = original_frame_size[0]

    if return_position:
        return (left, bottom, right, top)
    else:
        return (right, top)


def get_size_to_cover_frame_w_ratio (
    original_w_h_ratio: tuple,
    target_frame_size: tuple,
):
    # get the maximum image size to fit into a frame with a target ratio
    # read ratios
    target_frame_ratio = target_frame_size[0] / target_frame_size[1]  ## 0.33
    original_w_h_ratio_num = original_w_h_ratio[0] / original_w_h_ratio[1]  # 2

    if target_frame_ratio > original_w_h_ratio_num:
        # expand vertically
        # use all width
        new_image_width = target_frame_size[0]
        new_image_height = math.ceil(original_w_h_ratio[1] * target_frame_size[0] / original_w_h_ratio[0])

    elif target_frame_ratio < original_w_h_ratio_num:
        # expand vertically
        # use all height
        
        new_image_height = target_frame_size[1]
        new_image_width = math.ceil(original_w_h_ratio[0] * target_frame_size[1] / original_w_h_ratio[1])

    else:
        new_image_height = target_frame_size[1]
        new_image_width = target_frame_size[0]

    return (new_image_width, new_image_height)