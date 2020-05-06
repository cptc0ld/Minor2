from tkinter import *
from tkinter import messagebox
import EmailFetcher as ef


def interfaceFetchEmails():

    root = Tk()
    frame = Frame(root)
    frame.pack()
    bottomframe = Frame(root)
    bottomframe.pack(side=BOTTOM)

    L1 = Label(frame, text="E-mail: ")
    L1.pack()
    E1 = Entry(frame, bd=5, width=50)
    E1.pack()
    L2 = Label(frame, text="Password: ")
    L2.pack()
    E2 = Entry(frame, show="*", width=50)
    E2.pack(side=RIGHT)

    def submitCallBack():
        email = E1.get()
        password = E2.get()
        ef.login(email, password)
        messagebox.showinfo("OK")

    B1 = Button(bottomframe, text="Login", command=submitCallBack)
    B1.pack()
    root.mainloop()
