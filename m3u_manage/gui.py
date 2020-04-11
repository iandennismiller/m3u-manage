import os
import inspect
from tkinter import Tk, Menu, Toplevel, Image, filedialog, END
import tkinter.ttk as ttk
from . import __meta__

root = Tk()

input_file = None
output_file = None

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = ttk.Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = ttk.Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.open_button = ttk.Button(master, text="Blopen", command=self.get_input_file)
        self.open_button.pack()

        self.close_button = ttk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.label = ttk.Label(text="Name")
        self.label.pack()

        self.input_file_entry = ttk.Entry(width=50)
        self.input_file_entry.pack()

    def get_input_file(self):
        input_file = filedialog.askopenfilename(
            initialdir = ".",
            title = "Select m3u file",
            filetypes = (
                ("m3u files","*.m3u"),
                ("all files","*.*")
            )
        )
        self.input_file_entry.delete(0, END)
        self.input_file_entry.insert(0, input_file)

    def greet(self):
        print("Greetings!")


def donothing():
    filewin = Toplevel(root)
    button = ttk.Button(filewin, text="Do nothing button")
    button.pack()


def init_menu():
    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Save as...", command=donothing)
    filemenu.add_command(label="Close", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)

def start_gui():
    init_menu()

    # img_path = os.path.dirname(inspect.getfile(__meta__))
    # img = Image("photo", file=os.path.join(img_path, "clipboard.gif"))
    # root.iconphoto(True, img) # you may also want to try this.
    # root.tk.call('wm','iconphoto', root._w, img)

    my_gui = MyFirstGUI(root)

    # s = ttk.Style()
    # s.theme_use('alt')

    root.configure(background='#E9E9E9')
    root.focus_force()

    root.mainloop()
