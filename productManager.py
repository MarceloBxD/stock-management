import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import LabelFrame, Label, Button, Entry, Frame, Scrollbar, Style
import ttkthemes
from ttkthemes import themed_tk
from database import Database
from convertToExcel import convert, calc_profit
from PIL import Image, ImageTk
import os

if __name__ == '__main__':

    db = Database("products.db")
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
            product_category_entry.insert(0, selected_item[0][2])
            product_brand_entry.insert(0, selected_item[0][3])
            product_name_entry.insert(0, selected_item[0][4])
            product_stock_entry.insert(0,selected_item[0][5])
            cost_price_entry.insert(0, selected_item[0][6])
            selling_price_entry.insert(0, selected_item[0][7])
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

    root.wm_iconphoto(True, icon)

    entry_frame = LabelFrame(root, text="Entrar com Detalhes do Produto")
    # Product ID
    product_id_var = tk.StringVar()
    product_id_label = Label(entry_frame, text="ID do produto: ")
    product_id_label.grid(row=0, column=0, sticky="w", padx=10)
    product_id_entry = Entry(entry_frame, textvariable=product_id_var)
    product_id_entry.grid(row=0, column=1)

    # Product Category
    product_category_var = tk.StringVar()
    product_category_label = Label(entry_frame, text="Categoria do produto: ")
    product_category_label.grid(row=1, column=0, sticky="w", padx=10)
    product_category_entry = Entry(entry_frame, textvariable= product_category_var)
    product_category_entry.grid(row=1, column=1)

    # Product Brand
    product_brand_var = tk.StringVar()
    product_brand_label = Label(entry_frame, text="Marca do produto: ")
    product_brand_label.grid(row=0, column=2, sticky="w", padx=10)
    product_brand_entry = Entry(entry_frame, textvariable=product_brand_var)
    product_brand_entry.grid(row=0, column=3)

    # Product Name
    product_name_var = tk.StringVar()
    product_name_label = Label(entry_frame, text="Nome do Produto: ")
    product_name_label.grid(row=1, column=2, sticky="w", padx=10)
    product_name_entry = Entry(entry_frame, textvariable=product_name_var)
    product_name_entry.grid(row=1, column=3)

    #Product Stock
    product_stock_var = tk.StringVar()
    product_stock_label = Label(entry_frame, text="Estoque do produto: ")
    product_stock_label.grid(row=0, column=4, sticky="w", padx=10)
    product_stock_entry = Entry(entry_frame, textvariable=product_stock_var)
    product_stock_entry.grid(row=0, column=5)

    # Cost Price
    cost_price_var = tk.StringVar()
    cost_price_label = Label(entry_frame, text="Preço de custo: ")
    cost_price_label.grid(row=1, column=4, sticky="w", padx=10)
    cost_price_entry = Entry(entry_frame, textvariable=cost_price_var)
    cost_price_entry.grid(row=1, column=5)

    # Selling Price
    selling_price_var = tk.StringVar()
    selling_price_label = Label(entry_frame, text="Preço de venda: ")
    selling_price_label.grid(row=2, column=0, sticky="w", padx=10)
    selling_price_entry = Entry(entry_frame, textvariable=selling_price_var)
    selling_price_entry.grid(row=2, column=1)

    # ****************************************** #

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
                or product_category_var.get() == ""
                or product_brand_var.get() == ""
                or product_name_var.get() == ""
                or product_stock_var.get() == ""
                or cost_price_var.get() == ""
                or selling_price_var.get() == ""
        ):
            messagebox.showerror(title="Campos obrigatórios", message="Por favor, preencha todos os campos")
            return

        db.insert(
            product_id_var.get(),
            product_category_var.get(),
            product_brand_var.get(),
            product_name_var.get(),
            product_stock_var.get(),
            cost_price_var.get(),
            selling_price_var.get(),
        )
        clear_input()
        populate_list()
        statusbar_label["text"] = "Status: Produto adicionado com sucesso"
        statusbar_label.config(bg='green',fg='white')


    def update_item():
        if(
                product_id_var.get() != ""
                and product_category_var.get() != ""
                and product_brand_var.get() != ""
                and product_name_var.get() != ""
                and product_stock_var.get() != ""
                and cost_price_var.get() != ""
                and selling_price_var.get() != ""):
            db.update(
                selected_item[0][0],
                product_id_var.get(),
                product_category_var.get(),
                product_brand_var.get(),
                product_name_var.get(),
                product_stock_var.get(),
                cost_price_var.get(),
                selling_price_var.get(),
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
        statusbar_label.config(bg='green', fg='white')

    def clear_input():
        product_id_entry.delete(0, tk.END)
        product_category_entry.delete(0,tk.END)
        product_brand_entry.delete(0,tk.END)
        product_name_entry.delete(0, tk.END)
        product_stock_entry.delete(0,tk.END)
        cost_price_entry.delete(0, tk.END)
        selling_price_entry.delete(0, tk.END)


    def export_to_excel():
        convert()
        calc_profit()
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

    root.mainloop()
