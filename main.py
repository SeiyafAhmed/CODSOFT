from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledFrame
import random

to_do_list = []
tasks = []

with open("./to-do.csv") as to_dos_csv:
    to_dos = to_dos_csv.readlines()
    for to_do in to_dos:
        to_do = to_do.replace("\n", "")
        to_do_list.append([to_do.split(", ")[0], int(to_do.split(", ")[1])])
    to_dos_csv.close()


class Task:
    def __init__(self, root, to_do, state):
        self.root = root
        self.lines = 1

        self.line_height = 15
        self.to_do = to_do

        self.main_frame = Frame(root, width=470, style="")
        self.status = StringVar(self.main_frame, state)

        themes = ["success", "warning", "primary", "info"]

        self.box = Checkbutton(self.main_frame, variable=self.status, text=self.to_do, command=self.change, style=random.choice(themes))
        self.box.place(x=10, y=15)

        self.edit_btn = Button(self.main_frame, text="✒", command=self.edit, style="info-outline")

        self.delete_btn = Button(self.main_frame, text="🗑", command=self.delete, style="danger-outline")

        self.bottom_line = Frame(self.main_frame, width=440, height=0, style="warning")

        self.edit_frame = Frame(self.main_frame, width=50, style="info")
        self.edited_text = Text(self.edit_frame, width=38, height=self.lines * self.line_height/25, font=("dubai", 12))
        self.save_btn = Button(self.main_frame, text="✔", command=self.save, style="success-outline")

        self.main_frame.pack()
        self.set_height()


    def change(self):
        to_do_list[tasks.index(self)][1] = self.status.get()
        update()

    def set_height(self):
        mx_len = 60
        ln = 0
        self.lines = 0

        while "\n" in self.to_do:
            self.to_do = self.to_do.replace("\n", "")

        if len(self.to_do) > mx_len:
            temp = self.to_do.split(" ")
            txt = ""
            for i in temp:
                if ln+len(i) > mx_len:
                    ln = 0
                    txt += "\n"
                    self.lines += 1
                ln += len(i) + 1
                txt += i + " "
            self.to_do = txt
        self.box.config(text=self.to_do)
        self.main_frame.config(height=45 + self.lines * self.line_height)
        self.edit_btn.place(x=390, y=5+self.lines * self.line_height / 2)
        self.delete_btn.place(x=430, y=5+self.lines * self.line_height / 2)
        self.bottom_line.place(x=10, y=40 + self.lines * self.line_height)

    def delete(self):
        self.main_frame.destroy()
        to_do_list.pop(tasks.index(self))
        tasks.remove(self)
        update()

    def edit(self):
        self.edited_text.pack()
        self.edited_text.insert("end", self.to_do,)
        self.edited_text.config(height=self.lines * self.line_height/25)
        self.edit_frame.place(x=25, y=-2)
        self.save_btn.place(x=390, y=5+self.lines*self.line_height/2)

    def save(self):
        self.to_do = self.edited_text.get(1.0, "end-1c")
        if self.to_do == "":
            self.delete()
            return 0
        to_do_list[tasks.index(self)][0] = self.to_do
        self.set_height()
        self.edit_frame.destroy()
        self.save_btn.destroy()
        update()


def update():
    csv = open("./to-do.csv", 'w')
    for _to_do, _state in to_do_list:
        csv.write(f"{_to_do}, {_state}\n")
    csv.close()
    scrollbar_manger()


def add_to_do(txt=None):
    if new_to_do.get():
        to_do_list.append([new_to_do.get(), 0])
        tasks.append(Task(to_do_area, new_to_do.get(), 0))
        update()
        new_to_do.set("")
        to_do_area.yview("moveto", scrollbar_manger())


def scrollbar_manger():
    ln = 0
    for task in tasks:
        ln += 40 + task.lines * task.line_height

    if ln < 500:
        scrollbar_hider.place(x=510, y=120)
    else:
        scrollbar_hider.place_forget()
    return ln


root = Window()

root.geometry("550x750")
root.resizable(False, False)
root.title("TO-DO")
root.iconbitmap("./logo.ico")

Label(root, text="TO DO", style="warning", font=("Arial black", 42)).pack(pady=5)

ad_frame = Frame(root)
ad_frame.pack(pady=5)

to_do_area = ScrolledFrame(root, width=500, height=580)
to_do_area.pack()

new_to_do = StringVar()

new_task = Entry(ad_frame, width=60, style="warning", textvariable=new_to_do)
new_task.pack(side=LEFT, padx=5)
new_task.bind("<Return>", add_to_do)
Button(ad_frame, text="+", style="warning", command=add_to_do).pack(side=RIGHT)

scrollbar_hider = Frame(root, width=20, height=600)

for to_do, state in to_do_list:
    tasks.append(Task(to_do_area, to_do, state))

footer = Frame(root, width=550, style="dark",)
footer.pack(side=BOTTOM)
Label(footer, text="©2024 Seiyaf Ahmed ", style="inverse-dark", justify="right",).pack(padx=216)

scrollbar_manger()

root.mainloop()
