from tkinter import *
from tkinter.ttk import Progressbar
import sys
import os
import time

root = Tk()

height = 450
width = 600

x = (root.winfo_screenwidth()//2)-(width//2)
y = (root.winfo_screenheight()//2)-(height//2)

root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root.overrideredirect(1)

root.wm_attributes('-topmost', True)
root.config(background='#ffffff')

bg_label = Label(root, bg='black')
bg_label.place(x=0, y=0)

welcome_label = Label(text='Nome da Empresa - Controle de Estoque', bg='black', font=("arial", 15, "bold"), fg='white')
welcome_label.place(x=100, y=20)

created_by_label = Label(text='Created By Majors Solutions', bg='black', font=("arial", 15, "bold"), fg='white')
created_by_label.place(x=170, y=50)

progress_label = Label(root, text="Aguarde...", font=('arial', 13, 'bold'), fg='white',bg='black')
progress_label.place(x=225, y=350)
progress = Progressbar(root, orient=HORIZONTAL, length=550, mode='determinate')
progress.place(x=25, y=390)

exit_btn = Button(text='x', bg='red', command=lambda: exit_window(), bd=0, font=("arial", 16, "bold"),
                  activebackground='#fd6a36', fg='white')
exit_btn.place(x=570, y=0)
def exit_window():
    sys.exit(root.destroy())

def top():
    root.withdraw()
    os.system("python productManager.py")
    root.destroy()
i = 0

def loadsystem():
    global i
    if i <= 100:
        if i == 90:
            time.sleep(2)
        txt = 'Please Wait...  ' + (str(i)+'%')
        progress_label.config(text=txt)
        progress_label.after(10, loadsystem)
        progress['value'] = i
        i += 1
    else:
        top()

loadsystem()
root.mainloop()

