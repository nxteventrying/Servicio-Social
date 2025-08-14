import tkinter as tk

window = tk.Tk()

#Title of the window
window.title("Login form")
#the initial size of the window
window.geometry("300x440")
#setting the background colour
#window.configure(bg='#333333')


label = tk.Label(window, text = "Login")
#label.pack()
label.grid(row=0,column=0)
#it's like an infinite loop, nothing after this gets executed
#only after killing it
window.mainloop()




