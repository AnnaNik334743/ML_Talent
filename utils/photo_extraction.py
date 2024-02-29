from PIL import Image
from config import YOLO_MODEL


def is_human(img: Image.Image) -> bool:
    """
    Detects whether there is a human in an image using an object detection model.

    Parameters:
        img (PIL.Image.Image): The image to be analyzed.

    Returns:
        bool: True if a human is detected in the image, False otherwise.
    """
    output = YOLO_MODEL(img, verbose=False)
    res = output[0]
    classes = res.boxes.cls
    probs = res.boxes.conf
    for p, c in zip(probs, classes):
        if c.item() == 0 and p.item() > 0.3:
            return True
    return False

