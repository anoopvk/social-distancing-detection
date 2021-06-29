import tkinter as tk
# from tkinter.constants import INSERT
# from typing import Text


submited=False

def get_width_height():
    global submited
    def submit():
        global submited
        wi=width.get()
        hi=height.get()
        try:
            wi=float(wi)
            hi=float(hi)
            submited=True
            # print("changed submited",submited)
            root.quit()
            # w.set(wi)
            # h.set(hi)
        except ValueError:
            err.config(text="error")
        


    root = tk.Tk()
    root.title("Enter the width and height")
    error_message=""
    err=tk.Label(root,text=error_message)
    l1=tk.Label(root,text="enter width in centimeters")
    l2=tk.Label(root,text="enter height in centimeters")

    width=tk.StringVar()
    height=tk.StringVar()
    # w=""
    # h=""

    e1 = tk.Entry(root,textvariable=width)
    e2 = tk.Entry(root,textvariable=height)

    err.grid(row=0,column=1,padx=10,pady=3)
    l1.grid(row=1,column=0,padx=10,pady=3)
    l2.grid(row=2,column=0,padx=10,pady=3)
    e1.grid(row=1,column=1,padx=10,pady=3)
    e2.grid(row=2,column=1,padx=15,pady=3)

    # tk.Button(root,  text='Quit',command=root.quit).grid(row=3,column=0,sticky=tk.W,pady=4)
    tk.Button(root,text='submit', command=submit).grid(row=3,column=1,padx=15,pady=10)

    root.mainloop()
    # print(submited)
    w=width.get()
    h=height.get()
    # reg = root.register(callback)
    # e.config(validate ="key", validatecommand =(reg, '%P'))
    # print(w,h)
    if submited:
        return int(float(w)//1),int(float(h)//1)
    else:
        return False


if __name__=="__main__":
    print(get_width_height())
