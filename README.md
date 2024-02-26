# WaterMarkTool
A little tool to add water mark on various pictures


```python
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
```
