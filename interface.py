import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

img_cv = None 
thresh_img_cv = None  
adjusted_img_cv = None 

def upload_image():
    global img_cv, thresh_img_cv, adjusted_img_cv
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    
    if file_path:
        img_cv = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        thresh_img_cv = None
        adjusted_img_cv = None  
        update_display(img_cv, panel1)  

def apply_threshold():
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
    global thresh_img_cv, adjusted_img_cv

    if thresh_img_cv is None:
        return 

    contrast = contrast_var.get() / 50
    brightness = brightness_var.get()

    # Always apply to the original thresholded image
    adjusted_img_cv = cv2.convertScaleAbs(thresh_img_cv, alpha=contrast, beta=brightness)

    update_display(adjusted_img_cv, panel2)




def update_display(image, panel):
    img_pil = Image.fromarray(image)
    img_pil = img_pil.resize((300, 300)) 
    img_tk = ImageTk.PhotoImage(img_pil)
    panel.config(image=img_tk)
    panel.image = img_tk

def save_image():
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
root.geometry("800x500")
root.config(bg="#e0f7fa")

frame = tk.Frame(root, bg="#e0f7fa")
frame.pack(pady=20)

panel1 = tk.Label(frame, text="Original Image", bg="#e0f7fa", fg="#00796b", font=("Helvetica", 12, "bold"))
panel1.grid(row=0, column=0, padx=20)

panel2 = tk.Label(frame, text="Output Image", bg="#e0f7fa", fg="#00796b", font=("Helvetica", 12, "bold"))
panel2.grid(row=0, column=1, padx=20)

btn_upload = tk.Button(root, text="Upload Image", command=upload_image, bg="#4caf50", fg="white", padx=10, pady=5, font=("Helvetica", 10, "bold"))
btn_upload.pack(pady=5)

btn_threshold = tk.Button(root, text="Apply Threshold", command=apply_threshold, bg="#4caf50", fg="white", padx=10, pady=5, font=("Helvetica", 10, "bold"))
btn_threshold.pack(pady=5)

contrast_var = tk.IntVar(value=50) 
brightness_var = tk.IntVar(value=50) 

contrast_slider = tk.Scale(root, from_=10, to=200, orient="horizontal", label="Contrast", length=300, variable=contrast_var, bg="#e0f7fa", fg="#00796b")
contrast_slider.pack(pady=5)

brightness_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Brightness", length=300, variable=brightness_var, bg="#e0f7fa", fg="#00796b")
brightness_slider.pack(pady=5)

btn_save = tk.Button(root, text="Save Image", command=save_image, bg="#2196f3", fg="white", padx=10, pady=5, font=("Helvetica", 10, "bold"))
btn_save.pack(pady=5)

contrast_var.trace_add("write", adjust_contrast_brightness)
brightness_var.trace_add("write", adjust_contrast_brightness)

root.mainloop()
