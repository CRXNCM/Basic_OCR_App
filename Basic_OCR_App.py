import cv2
import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import messagebox
from PIL import ImageTk
import os

class BasicOCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic OCR Application")
        self.root.geometry("800x600")
        
        # Variables
        self.image_path = None
        self.image = None
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        # Top frame for buttons
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Open image button
        open_btn = tk.Button(top_frame, text="Open Image", command=self.open_image)
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # Process button
        process_btn = tk.Button(top_frame, text="Extract Text", command=self.process_image)
        process_btn.pack(side=tk.LEFT, padx=5)
        
        # Save text button
        save_btn = tk.Button(top_frame, text="Save Text", command=self.save_text)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Image display area (left side)
        image_frame = tk.LabelFrame(content_frame, text="Image")
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_label = tk.Label(image_frame, text="No image loaded")
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text display area (right side)
        text_frame = tk.LabelFrame(content_frame, text="Extracted Text")
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_image(self):
        file_types = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"),
            ("All files", "*.*")
        ]
        
        self.image_path = filedialog.askopenfilename(title="Select Image", filetypes=file_types)
        
        if self.image_path:
            try:
                # Load the image using OpenCV
                self.image = cv2.imread(self.image_path)
                
                # Display the image
                self.display_image()
                
                self.status_var.set(f"Loaded image: {os.path.basename(self.image_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {str(e)}")
    
    def display_image(self):
        if self.image is not None:
            # Convert from BGR to RGB for display
            img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            
            # Resize for display if needed
            h, w = img_rgb.shape[:2]
            max_size = 300
            
            if h > max_size or w > max_size:
                scale = min(max_size/h, max_size/w)
                new_h, new_w = int(h*scale), int(w*scale)
                img_rgb = cv2.resize(img_rgb, (new_w, new_h))
            
            # Convert to PhotoImage
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            
            # Update the image label
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # Keep a reference
    
    def process_image(self):
        if self.image is None:
            messagebox.showinfo("Info", "Please open an image first.")
            return
        
        try:
            self.status_var.set("Processing image...")
            self.root.update()
            
            # Convert image to grayscale (improves OCR accuracy)
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            
            # Apply OCR
            extracted_text = pytesseract.image_to_string(gray)
            
            # Display the extracted text
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, extracted_text)
            
            self.status_var.set("Text extraction completed")
        except Exception as e:
            messagebox.showerror("Error", f"OCR processing failed: {str(e)}")
            self.status_var.set("Text extraction failed")
    
    def save_text(self):
        if not self.text_area.get(1.0, tk.END).strip():
            messagebox.showinfo("Info", "No text to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.status_var.set(f"Text saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")

if __name__ == "__main__":
    # For Windows, you might need to set the path to Tesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    root = tk.Tk()
    app = BasicOCRApp(root)
    root.mainloop()
