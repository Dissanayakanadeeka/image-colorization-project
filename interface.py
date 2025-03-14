import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

img_cv = None 
thresh_img_cv = None  
adjusted_img_cv = None 

def upload_image():
    """Upload an image, convert it to grayscale, and display it."""
    global img_cv, thresh_img_cv, adjusted_img_cv
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    
    if file_path:
        img_cv = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        thresh_img_cv = None
        adjusted_img_cv = None  
        update_display(img_cv, panel1)  

def apply_threshold():
    """Apply thresholding and update the output panel."""
    global img_cv, thresh_img_cv, adjusted_img_cv
    if img_cv is None:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    _, thresh_img = cv2.threshold(img_cv, 128, 255, cv2.THRESH_BINARY)
    thresh_img_cv = thresh_img 
    adjusted_img_cv = thresh_img.copy() 

    update_display(thresh_img, panel2)  
    adjust_contrast_brightness() 

def adjust_contrast_brightness(*args):
    """Adjust contrast and brightness of the thresholded image in real-time."""
    global thresh_img_cv, adjusted_img_cv
    if thresh_img_cv is None:
        return 

    contrast = contrast_var.get()/50   
    brightness = brightness_var.get()  

    adjusted_img_cv = cv2.convertScaleAbs(thresh_img_cv, alpha=contrast, beta=brightness)

    update_display(adjusted_img_cv, panel2)  

def update_display(image, panel):
    """Update a Tkinter display panel with the given image."""
    img_pil = Image.fromarray(image)
    img_pil = img_pil.resize((300, 300)) 
    img_tk = ImageTk.PhotoImage(img_pil)
    panel.config(image=img_tk)
    panel.image = img_tk

def save_image():
    """Save the contrast and brightness adjusted image."""
    global adjusted_img_cv
    if adjusted_img_cv is None:
        messagebox.showerror("Error", "No processed image to save!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("Bitmap files", "*.bmp")])
    if file_path:
        cv2.imwrite(file_path, adjusted_img_cv)
        messagebox.showinfo("Success", "Image saved successfully!")

root = tk.Tk()
root.title("Thresholding & Adjustment App")
root.geometry("400x600")  # Adjust window size

btn_upload = tk.Button(root, text="Upload Image", command=upload_image)
btn_upload.pack()

btn_threshold = tk.Button(root, text="Apply Threshold", command=apply_threshold)
btn_threshold.pack()

panel1 = tk.Label(root, text="Original Image")
panel1.pack()

panel2 = tk.Label(root, text="Output Image")  
panel2.pack()

contrast_var = tk.IntVar(value=50) 
brightness_var = tk.IntVar(value=50) 

contrast_slider = tk.Scale(root, from_=10, to=200, orient="horizontal", label="Contrast", length=300, variable=contrast_var)
contrast_slider.pack()

brightness_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Brightness", length=300, variable=brightness_var)
brightness_slider.pack()

contrast_var.trace_add("write", adjust_contrast_brightness)
brightness_var.trace_add("write", adjust_contrast_brightness)

# Save Button
btn_save = tk.Button(root, text="Save Image", command=save_image)
btn_save.pack()

root.mainloop()
