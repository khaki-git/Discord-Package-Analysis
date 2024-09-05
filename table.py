import customtkinter as ctk

class Table(ctk.CTkFrame):
    def __init__(self, master, rows, columns, table_data, **kwargs):
        super().__init__(master=master, **kwargs)

        self.rows = rows
        self.columns = columns

        # Define border options
        border_width = 2
        border_color = "black"  # Customize the border color

        # Create table headers
        for col in range(self.columns):
            header = ctk.CTkLabel(self, text=table_data[f"h{col+1}"], width=20, height=2)
            header.grid(row=0, column=col, sticky="nsew")

        # Create table cells
        for row in range(1, self.rows):
            for col in range(self.columns):
                cell = ctk.CTkLabel(self, text=table_data[f"t{col+1}%{row+1}"], width=20, height=2,
                                   anchor='center')
                cell.grid(row=row, column=col, sticky="nsew")

        # Configure rows and columns to expand
        for col in range(self.columns):
            self.grid_columnconfigure(col, weight=1)

        for row in range(self.rows):
            self.grid_rowconfigure(row, weight=1)

if __name__ == "__main__":
    table_data = {
        "h1": "Header 1", "h2": "Header 2", "h3": "Header 3",
        "t1%1": "Cell 1", "t2%1": "Cell 2", "t3%1": "Cell 3",
        "t1%2": "Cell 4", "t2%2": "Cell 5", "t3%2": "Cell 6",
        "t1%3": "Cell 7", "t2%3": "Cell 8", "t3%3": "Cell 9",
        "t1%4": "Cell 10", "t2%4": "Cell 11", "t3%4": "Cell 12",
        "t1%5": "Cell 13", "t2%14": "Cell 15", "t3%5": "Cell 16",
    }

    app = ctk.CTk()
    app.title("Table Example")
    app.geometry("400x300")

    table = Table(master=app, rows=3, columns=3, table_data=table_data)
    table.pack(fill="both", expand=True, padx=20, pady=20)

    app.mainloop()
