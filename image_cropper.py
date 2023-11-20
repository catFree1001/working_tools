from PIL import Image
import os, sys

def image_cropper(image_path:str):
    # image_path = r"C:\Users\dicky.kf.lam\Desktop\_working_script\Screenshot 2023-11-06 172926.png"

    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    left = 0
    top = 0
    right = width
    bottom = height

    print(width, height)

    left, right, top, bottom = input("left, right, top, bottom : ").strip().split()
    left, right, top, bottom = map(int, (left, right, top, bottom))

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image
    directory = os.path.dirname(image_path)
    name ,file_extension = os.path.splitext(os.path.basename(image_path))
    # file_extension = os.path.splitext(image_path)[1]
    cropped_file = directory + "\\" + name + "_cropped" + file_extension
    cropped_image.save(cropped_file)

    print(f"Cropped image saved as {cropped_file}")


def iterdir(path:str, process:function):
    """iter all files at the root dir, 
    對folder內所有文件進行處理"""
    # print(folder)
    if os.path.isdir(path):
        subfolder = os.listdir(path)
        # print("sub:",subfolder)
        for i in subfolder:
            newpath = os.path.join(path,i)
            iterdir(newpath)
    else:
        print("Process: ", path)
        process(path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            path = os.path.abspath(i)
            iterdir(path, process=image_cropper)
    else:
        image_path = input("Image path: ")
        image_cropper(image_path)
