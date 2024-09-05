import customtkinter as ctk
import ctk_images
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import analysis as analyze
import table
import os

# Set appearance mode and theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("./coffee.json")

class Results(ctk.CTkToplevel):
    def __init__(self, master, package_results: analyze.PackageAnalysis):
        super().__init__(master=master)

        self.title("Results")
        self.iconbitmap("./icon.ico")
        self.geometry("500x500")
        self.package_results = package_results
        self.attributes("-topmost", True)

        # Configure the grid
        self.grid_rowconfigure(0, weight=1)  # The first row for the table
        self.grid_rowconfigure(1, weight=1)  # The second row for the textboxes and their labels
        self.grid_rowconfigure(2, weight=1)  # The third row for the textboxes and their labels
        self.grid_columnconfigure(0, weight=1)  # The first column (left side) expands horizontally
        self.grid_columnconfigure(1, weight=0)  # The second column (right side) does not expand

        top_gc = analyze.get_top(package_results.involved_gc)
        top_server = analyze.get_top(package_results.favourite_channels)

        # Create and configure data table
        self.data_table = table.Table(master=self, columns=2, rows=6, table_data={
            "h1": "Statistic",
            "h2": "Count",
            "t1%1": "Words", "t2%1": f"{self.package_results.word_count}",
            "t1%2": "Links", "t2%2": f"{self.package_results.links_sent}",
            "t1%3": "Pings", "t2%3": f"{self.package_results.pings_sent}",
            "t1%4": "Attachments", "t2%4": f"{self.package_results.attachments}",
            "t1%5": "Top Server", "t2%5": f"{top_server}",
            "t1%6": "Top GC", "t2%6": f"{top_gc}",
        })
        self.data_table.grid(column=0, row=0, rowspan=3, sticky="nsew")  # Span vertically

        # Create labels for textboxes
        self.label_links = ctk.CTkLabel(master=self, text="Links in order of usage", anchor='w')
        self.label_links.grid(column=1, row=0, sticky="w", padx=10, pady=(10, 0))  # Adjust padding

        # Create textboxes
        self.textbox_links = ctk.CTkTextbox(master=self, corner_radius=0, width=250)
        self.textbox_links.grid(column=1, row=2, sticky="nsew", padx=10, pady=(0, 10))  # Place below label_links

        self.label_words = ctk.CTkLabel(master=self, text="Words in order of usage", anchor='w')
        self.label_words.grid(column=1, row=3, sticky="w", padx=10, pady=(10, 0))  # Adjust padding

        self.textbox_words = ctk.CTkTextbox(master=self, corner_radius=0, width=250)
        self.textbox_words.grid(column=1, row=4, sticky="nsew", padx=10, pady=(0, 10))  # Place below label_words

        self.explore_button = ctk.CTkButton(master=self, text='Open in Explorer', command=self.open_explorer)
        self.explore_button.grid(column=0, padx=10, pady=(0, 10))

        self.docs_textboxes()

    def docs_textboxes(self):
        self.textbox_links.insert(1.0, analyze.sort_get(self.package_results.links))
        self.textbox_words.insert(1.0, analyze.sort_get(self.package_results.words))

    def open_explorer(self):
        os.startfile(os.path.abspath("./results/package.txt"))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Discord Package Analysis')
        self.iconbitmap("./icon.ico")
        self.geometry("700x500")
        self.minsize(600, 300)

        self.navbar = ctk.CTkFrame(master=self, height=72)
        self.navbar.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=3)
        self.grid_columnconfigure(0, weight=1)

        self.icon_box = ctk_images.Imagebox(master=self.navbar, image_path="./icon.png", width=64, height=64)
        self.icon_box.grid(column=0, row=0, padx=10, pady=4)

        self.icon_label = ctk.CTkLabel(master=self.navbar, text="Discord Package Analysis", width=500, height=64, font=('Roboto', 40), anchor='w')
        self.icon_label.grid(column=1, row=0, padx=10, pady=4)

        # Folder icon and Select Folder button
        self.folder_icon = ctk_images.Imagebox(master=self, image_path="./assets/folder.png", width=64, height=64)
        self.select_folder = ctk.CTkButton(master=self, text="Select Folder", width=200, font=('Roboto', 20), command=self.analysis)

        # Place folder icon and button in the same column and adjust padding
        self.folder_icon.grid(column=0, row=1, padx=10, pady=10, sticky="s")
        self.select_folder.grid(column=0, row=2, padx=10, pady=10, sticky="n")



    def __repr__(self):
        return 'App'

    def analysis(self):
        package = filedialog.askdirectory(title="Select Data Package")

        if package:
            CTkMessagebox(master=self, title="Began Analysis",
                          message="Your data is currently being analysed. Please wait, your results will get written to a file if the program crashes.")

            package, errors = analyze.analyze(package)
            analyze.analyze(package)

            if package is not None:
                with open("./results/package.txt", "wb") as package_file:
                   package_file.write(package.encode().encode("utf-8"))
                result_window = Results(master=self, package_results=package)
                result_window.mainloop()
            else:
                CTkMessagebox(master=self, title="Errors", message=errors)


if __name__ == "__main__":
    app = App()
    app.mainloop()
