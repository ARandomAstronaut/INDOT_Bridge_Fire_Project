from PIL                import Image
from pathlib            import Path
import cv2

def crop_image(input_path, output_path, crop_top=0, crop_bottom=0, crop_left=0, crop_right=0):
    """
    Crop a .png image by a specified number of pixels from each side.
    
    Parameters:
    - input_path: str, path to input .png image
    - output_path: str, path to save the cropped image
    - crop_top, crop_bottom, crop_left, crop_right: int, number of pixels to crop
    """
    with Image.open(input_path) as img:
        width, height = img.size #image dimension decleratopm
        left = crop_left; top = crop_top; right = width - crop_right; bottom = height - crop_bottom

        # Ensure valid crop box
        if left >= right or top >= bottom: raise ValueError("Cropping dimensions are too large for the image size.")

        cropped_img = img.crop((left, top, right, bottom))
        #cropped_img.show() #uncomment this line to debug
        cropped_img.save(output_path)

#main function
input_dir  = Path(r"C:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Fire Test\Video2_ImageCrop\uncropped_photo")
output_dir  = Path(r"C:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Fire Test\Video2_ImageCrop\cropped_photo")

files  = sorted(input_dir.glob("*.png"))
labels = [f.stem for f in files]

for i, fpath in enumerate(files):
    img = cv2.imread(str(fpath))
    if img is None: raise FileNotFoundError(f"Could not load '{fpath}'")
    output_path = output_dir / f"cropped_image_time{i*15}.png"
    crop_image(input_path=fpath,output_path=output_path,crop_top=300,crop_bottom=1200,crop_left=400, crop_right=1800)
    
