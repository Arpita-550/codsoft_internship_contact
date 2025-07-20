import tkinter as tk
from tkinter import messagebox
import json
import os

CONTACT_FILE = "contact_records.json"

def load_data():
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as file:
             return json.load(file)
    return[]

def save_data():
    with open(CONTACT_FILE, "w") as file:
            json.dump(contact_list, file, indent=2)

def create_entry():
    name = name_input.get().strip()
    number = number_input.get().strip()
    email = email_input.get().strip()
    location = location_input.get().strip()

    if not name or not number:
        show_popup("Input Missing", "Name and phone number are required", "warning")
        return
    
    new_record = {
          "name": name,
          "number": number,
          "email": email,
          "location": location
    }

    contact_list.append(new_record)
    save_data()
    reset_inputs()
    refresh_display()
    show_popup("saved", "new contact has been saved","info")
    
def modify_entry():
    index = display_box.curselection()
    if not index:
        show_popup("select required","pick a contact number","info")
        return
    idx = index[0]
    contact_list[idx] = {
        "name" : name_input.get().strip(),
        "number" : number_input.get().strip(),
        "email" : email_input.get().strip(),
        "location" : location_input.get().strip()
    }
    save_data()
    refresh_display()
    show_popup("updated, 'contact information updated","info")

def remove_entry():
    index= display_box.curselection()
    if not index:
        show_popup("Nothing chosen", "no contact selected","info")
        return
    idx = index[0]
    confirmation = messagebox.askquestion("Delete entry", "Remove this contact permanently?")
    if confirmation =="yes":
        del contact_list[idx]
        save_data()
        reset_inputs()
        refresh_display()

def load_selected(event):
    index = display_box.curselection()
    if index:
        idx = index[0]
        data = contact_list[idx]
        name_input.delete(0,tk.END)
        number_input.delete(0,tk.END)
        email_input.delete(0,tk.END)
        location_input.delete(0,tk.END)

        name_input.insert(0,data["name"])
        number_input.insert(0,data["number"])
        email_input.insert(0,data["email"])
        location_input.insert(0,data["location"])

def reset_inputs():
    name_input.delete(0,tk.END)
    number_input.delete(0,tk.END)
    email_input.delete(0,tk.END)
    location_input.delete(0,tk.END)

def show_popup(title, message, popup_type):
    if popup_type =="info":
        messagebox.showinfo(title,message)
    elif popup_type =="warning":
        messagebox.showwarning(title,message)
    elif popup_type =="error":
        messagebox.showerror(title,message)

def refresh_display():
    display_box.delete(0,tk.END)
    for record in contact_list:
        display_box.insert(tk.END, f"{record['name']}-{record['number']}")

def look_up():
    keyword = search_input.get().lower()
    display_box.delete(0,tk.END)
    for person in contact_list:
        if keyword in person["name"].lower()  or keyword in person["number"]:
           display_box.insert(tk.end,f"{person['name']}-{person['number']}")



contact_list = load_data()
app = tk.Tk()
app.title ("Contact List")
app.geometry ("600x520")
app.resizable(False,False)

tk.Label(app, text= "Full Name: ").place(x=20, y=20)
tk.Label(app, text= "Phone No: ").place(x=20, y=60)
tk.Label(app, text= "Email: ").place(x=20, y=100)
tk.Label(app, text= "Location: ").place(x=20, y=140)


name_input = tk.Entry(app, width=30)
name_input.place(x=120, y=20)

number_input = tk.Entry(app, width=30)
number_input.place(x=120, y=60)

email_input = tk.Entry(app, width=30)
email_input.place(x=120, y=100)

location_input = tk.Entry(app, width=30)
location_input.place(x=120, y=140)


tk.Button(app, text="Add Number", width=15, command=create_entry).place(x=420, y=20)
tk.Button(app, text="Update Number", width=15, command=modify_entry).place(x=420, y=60)
tk.Button(app, text="Delete Number", width=15, command=remove_entry).place(x=420, y=100)

tk.Label(app,text="Search: ").place(x=20, y=190)
search_input= tk.Entry(app, width=30)
search_input.place(x=120, y=190)
tk.Button(app,text= "Find", command= look_up, width=15).place(x=420, y=190)

display_box = tk.Listbox(app, width=70, height=15)
display_box.place(x=20, y=240)
display_box.bind("<<ListboxSelect>>", load_selected)


refresh_display()
app.mainloop()
    
    


