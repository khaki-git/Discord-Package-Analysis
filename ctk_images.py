import customtkinter as ctk
from PIL import Image, ImageTk

class Imagebox(ctk.CTkCanvas):
    def __init__(self, master, image_path="./icon.png", width=500, height=500, transparent=True):
        try:
            fg_clr = master.cget("fg_color")
            appearance_mode = ctk.get_appearance_mode()

            if appearance_mode == "Dark":
                bg_clr = fg_clr[1]  # Dark mode color
            else:
                bg_clr = fg_clr[0]  # Light mode color
        except Exception as e:
            print(e)
            bg_clr = "#262626"
        if transparent:
            super().__init__(master=master, width=width, height=height, background=bg_clr, highlightthickness=0)
        else:
            super().__init__(master=master, width=width, height=height)
        self.img = image_path
        self.img_width = width
        self.img_height = height
        self.photo_img = None  # Add this line to hold the image reference

        self.refresh_img()

    def refresh_img(self):
        img = Image.open(self.img)
        img = img.resize((self.img_width, self.img_height))
        self.photo_img = ImageTk.PhotoImage(img)  # Store it in an instance variable

        self.img_height = img.height
        self.img_width = img.width

        self.create_image(0, 0, image=self.photo_img, anchor='nw')  # Make sure the anchor is set

    def apply_img(self, image_path):
        self.img = image_path
        self.refresh_img()
