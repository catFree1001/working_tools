import sys,os
import pillow_heif
import numpy as np 
import cv2

def convert_heic_to_png(heic_path):
    try:
        # Open the HEIC file
        file_path = os.path.dirname(heic_path)
        file_name ,extention_name= os.path.splitext(os.path.basename(heic_path))
        if extention_name != ".heic":
            return
        
        image = pillow_heif.open_heif(heic_path, convert_hdr_to_8bit=False, bgr_mode=True)
        

        # Get the original file path and name
        file_path = os.path.dirname(heic_path)
        file_name = os.path.splitext(os.path.basename(heic_path))[0]

        # Save the image as PNG with the same name in the original location
        png_file = file_path + "\\" + file_name + '.png'
        
        np_array = np.asarray(image)
        # print(png_file)
        cv2.imwrite(png_file, np_array)
        # Image.save(png_file, 'PNG')
        print("Convered {}".format(png_file))

    except Exception as e:
        print("Error converting HEIC to PNG:", str(e))

# Check if a HEIC file is provided as a command-line argument

    
def iterdir(path:str, process):
    """iter all files at the root dir, 
    對folder內所有文件進行處理"""
    # print(folder)
    if os.path.isdir(path):
        subfolder = os.listdir(path)
        # print("sub:",subfolder)
        for file in subfolder:
            newpath = os.path.join(path,file)
            iterdir(newpath,process)
    else:
        # print("Process: ", path)
        process(path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            path = os.path.abspath(i)
            iterdir(path, process=convert_heic_to_png)
            # print(i)
    else:
        heic_path = input("Image path : ")
        convert_heic_to_png(heic_path)