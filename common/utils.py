from PIL import Image
 
 
def crop_center(img: Image, width: int, height: int) -> Image:
    "Cuts out the center of the image."
    img_width, img_height = img.size
    box = (
        (img_width - width) // 2,
        (img_height - height) // 2,
        (img_width + width) // 2,
        (img_height + height) // 2,
    )
    return img.crop(box)
 
 
def crop_max_square(img: Image) -> Image:
    'Cuts out the max square in the center of the image.'
    side = min(img.size)
    return crop_center(img, side, side)


def crop_rectange(img: Image, width: int, height: int) -> Image:
    "Cuts out the rectangle in the center of the image."
    return crop_center(img, width, height)


def set_picture(path_to_picture: str, size: tuple, type: str) -> None:
    """
    Sets the image fromat to a square or rectangle to be saved on model further.
    The size parameter is needed to create a thumbnail. f.e. (771, 482)
    The type parameter defines the type of the thumbnail.
    It can be of two kinds: square (for profile pictures) and rectangle (for article titles).
    """
    with Image.open(path_to_picture) as image:
        if type == 'square':
            image = crop_max_square(image)
            image.thumbnail(size, Image.ANTIALIAS)
        elif type == 'rectangle':
            image.thumbnail(size, Image.ANTIALIAS)
            image = crop_rectange(image, *size)
        image.save(path_to_picture)
