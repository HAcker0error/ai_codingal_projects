import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance


class PhotoEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Photo Editor")
        self.root.geometry("900x650")

        self.image = None
        self.display_image = None

        title = tk.Label(root, text="Photo Editor", font=("Arial", 22, "bold"))
        title.pack(pady=10)

        self.image_label = tk.Label(root, text="Open an image to start", font=("Arial", 14))
        self.image_label.pack(pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Open Image", command=self.open_image, width=15).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Rotate Left", command=self.rotate_left, width=15).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Rotate Right", command=self.rotate_right, width=15).grid(row=0, column=2, padx=5)

        brightness_frame = tk.Frame(root)
        brightness_frame.pack(pady=10)

        tk.Label(brightness_frame, text="Brightness:").pack(side=tk.LEFT)

        self.brightness = tk.Scale(
            brightness_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=250,     
            command=self.change_brightness
            )
        self.brightness.set(1.0)
        self.brightness.pack(side=tk.LEFT)

        crop_frame = tk.Frame(root)
        crop_frame.pack(pady=10)

        tk.Label(crop_frame, text="X:").grid(row=0, column=0)
        self.x_entry = tk.Entry(crop_frame, width=8)
        self.x_entry.grid(row=0, column=1)

        tk.Label(crop_frame, text="Y:").grid(row=0, column=2)
        self.y_entry = tk.Entry(crop_frame, width=8)
        self.y_entry.grid(row=0, column=3)

        tk.Label(crop_frame, text="Width:").grid(row=0, column=4)
        self.width_entry = tk.Entry(crop_frame, width=8)
        self.width_entry.grid(row=0, column=5)

        tk.Label(crop_frame, text="Height:").grid(row=0, column=6)
        self.height_entry = tk.Entry(crop_frame, width=8)
        self.height_entry.grid(row=0, column=7)

        tk.Button(root, text="Crop Image", command=self.crop_image, width=20).pack(pady=5)
        tk.Button(root, text="Save Image", command=self.save_image, width=20).pack(pady=10)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])

        if file_path:
            self.image = Image.open(file_path)
            self.show_image()

    def show_image(self):
        if self.image:
            preview = self.image.copy()
            preview.thumbnail((700, 400))

            self.display_image = ImageTk.PhotoImage(preview)
            self.image_label.config(image=self.display_image, text="")

    def rotate_left(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            self.show_image()

    def rotate_right(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)
            self.show_image()

    def change_brightness(self, value):
        if self.image:
            factor = float(value)

            enhancer = ImageEnhance.Brightness(self.image)
            bright_image = enhancer.enhance(factor)

            preview = bright_image.copy()
            preview.thumbnail((700, 400))

            self.display_image = ImageTk.PhotoImage(preview)
            self.image_label.config(image=self.display_image, text="")

    def crop_image(self):
        if self.image:
            try:
                x = int(self.x_entry.get())
                y = int(self.y_entry.get())
                width = int(self.width_entry.get())
                height = int(self.height_entry.get())

                self.image = self.image.crop((x, y, x + width, y + height))
                self.show_image()

            except ValueError:
                self.image_label.config(text="Please enter valid numbers.")

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")]
            )

            if file_path:
                self.image.save(file_path)
                self.image_label.config(text="Image saved successfully!")


root = tk.Tk()
app = PhotoEditor(root)
root.mainloop()