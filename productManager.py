import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import LabelFrame, Label, Button, Entry, Frame, Scrollbar, Style, Combobox
import ttkthemes
from ttkthemes import themed_tk
from database import Database
from convertToExcel import convert
from PIL import Image, ImageTk
import os

if __name__ == '__main__':
    db = Database("products.db")

    def fetch_all_from_db(field):
        rows = db.fetch_all_rows()
        return [row[field] for row in rows]

    def populate_name():
        categories = fetch_all_from_db(1)
        return categories

    def populate_list():
        product_list_listbox.delete(0, tk.END)
        for num, row in enumerate(db.fetch_all_rows()):
            string = ""
            for i in row:
                string = string + "  |  " + str(i)
            string = str(num + 1) + string
            product_list_listbox.insert(tk.END, string)

    def select_item(event):
        try:
            global selected_item
            index = product_list_listbox.curselection()[0]
            selected_item = product_list_listbox.get(index)
            selected_item = selected_item.split("  |  ")
            selected_item = db.fetch_by_product_id(selected_item[1])
            clear_input()

            product_id_entry.insert(0, selected_item[0][1])
            product_name_entry.insert(0, selected_item[0][2])
            product_stock_entry.insert(0,selected_item[0][3])
        except IndexError:
            pass


    root = themed_tk.ThemedTk()
    root.set_theme("scidpurple")

    root.title("Sistema de Controle de Estoque")
    width = 1080
    height = 700
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)

    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.columnconfigure(0, weight=1)

    entry_frame = LabelFrame(root, text="Entrar com Detalhes do Produto")
    
    # Product ID
    product_id_var = tk.StringVar()
    product_id_label = Label(entry_frame, text="CR do produto: ")
    product_id_label.grid(row=0, column=0, sticky="w", padx=10)
    product_id_entry = Entry(entry_frame, textvariable=product_id_var)
    product_id_entry.grid(row=0, column=1)

    # Product Name
    product_name_var = tk.StringVar()
    product_name_label = Label(entry_frame, text="Nome do Produto: ")
    product_name_label.grid(row=1, column=0, sticky="w", padx=10)
    product_name_combobox = Combobox(entry_frame, textvariable=product_name_var, state="readonly")
    product_name_combobox.grid(row=1, column=1)

    #Product Stock
    product_stock_var = tk.StringVar()
    product_stock_label = Label(entry_frame, text="Estoque do produto: ")
    product_stock_label.grid(row=0, column=2, sticky="w", padx=10)
    product_stock_entry = Entry(entry_frame, textvariable=product_stock_var)
    product_stock_entry.grid(row=0, column=3)

    # Product List
    # frame containing product listing and scrollbar
    listing_frame = Frame(root, borderwidth=1, relief="raised")
    product_list_listbox = tk.Listbox(listing_frame)
    product_list_listbox.grid(row=0, column=0, padx=10, pady=5, sticky="we")
    # binding list box to show selected items in the entry fields.
    product_list_listbox.bind("<<ListboxSelect>>", select_item)

    # Create ScrollBar
    scroll_bar = Scrollbar(listing_frame)
    scroll_bar.config(command=product_list_listbox.yview)
    scroll_bar.grid(row=0, column=1, sticky="ns")

    # Attach Scrollbar to Listbox
    product_list_listbox.config(yscrollcommand=scroll_bar.set)

    # =========================#

    # Create Statusbar using Label widget onto root
    statusbar_label = tk.Label(
        root, text="Status: ", bg="#ffb5c5", anchor="w", font=("arial", 10)
    )
    statusbar_label.grid(row=3, column=0, sticky="we", padx=10)
    # ========================#

    # Button Functions
    def add_item():
        if (
                product_id_var.get() == ""
                or product_name_var.get() == ""
                or product_stock_var.get() == ""
        ):
            messagebox.showerror(title="Campos obrigatórios", message="Por favor, preencha todos os campos")
            return

        db.insert(
            product_id_var.get(),
            product_name_var.get(),
            product_stock_var.get(),
        )
        clear_input()
        populate_list()
        statusbar_label["text"] = "Status: Produto adicionado com sucesso"
        populate_name()
        statusbar_label.config(bg='green',fg='white')


    def update_item():
        if(
                product_id_var.get() != ""
                and product_name_var.get() != ""
                and product_stock_var.get() != ""
                ):
                
            db.update(
                selected_item[0][0],
                product_id_var.get(),
                product_name_var.get(),
                product_stock_var.get(),
            )
            populate_list()
            statusbar_label["text"] = "Status: Produto atualizado com sucesso"
            statusbar_label.config(bg='green',fg='white')
            return
        messagebox.showerror(title="Campos obrigatórios", message="Por favor, preencha todos os campos")
        statusbar_label["text"] = "Por favor, preencha todos os campos"
        statusbar_label.config(bg='red', fg='white')

    def remove_item():
        db.remove(selected_item[0][1])
        clear_input()
        populate_list()
        statusbar_label["text"] = "Status: Produto removido com sucesso"
        populate_name()
        statusbar_label.config(bg='green', fg='white')

    def clear_input():
        product_id_entry.delete(0, tk.END)
        product_name_entry.delete(0, tk.END)
        product_stock_entry.delete(0,tk.END)


    def export_to_excel():
        convert()
        statusbar_label["text"] = f"Status: Arquivo Excel criado em {os.getcwd()}"
        statusbar_label.config(bg='green', fg='white')

    # Buttons
    button_frame = Frame(root, borderwidth=2, relief="groove")

    add_item_btn = Button(button_frame, text="Adicionar item", command=add_item)
    add_item_btn.grid(row=0, column=0, sticky="we", padx=10, pady=5)

    remove_item_btn = Button(button_frame, text="Remover item", command=remove_item)
    remove_item_btn.grid(row=0, column=1, sticky="we", padx=10, pady=5)

    update_item_btn = Button(button_frame, text="Atualizar item", command=update_item)
    update_item_btn.grid(row=0, column=2, sticky="we", padx=10, pady=5)

    clear_item_btn = Button(button_frame, text="Limpar input", command=clear_input)
    clear_item_btn.grid(row=0, column=3, sticky="we", padx=10, pady=5)

    export_to_excel_btn = Button(
        button_frame, text="Exportar para o Excel", command=export_to_excel
    )
    export_to_excel_btn.grid(row=0, column=4, sticky="we", padx=10, pady=5)

    entry_frame.grid(row=0, column=0, sticky="we", padx=10, pady=5)
    button_frame.grid(row=1, column=0, sticky="we", padx=10, pady=5)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid_columnconfigure(3, weight=1)
    button_frame.grid_columnconfigure(4, weight=1)
    listing_frame.grid(row=2, column=0, sticky="we", padx=10)
    listing_frame.grid_columnconfigure(0, weight=2)

    populate_list()
    populate_name()
    root.mainloop()
