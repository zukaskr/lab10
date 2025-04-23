import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os

csv_file_path = r"C:\Users\yesta\OneDrive\Desktop\lab10\my_contacts.csv"
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

def initialize_csv():
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'phone_number'])
            writer.writerow(['Aruzhan', '+77012345678'])
            writer.writerow(['Miras', '+77098765432'])
            writer.writerow(['Dana', '+77011223344'])

def load_contacts():
    contacts_listbox.delete(0, tk.END)
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contacts_listbox.insert(tk.END, f"{row['name']}: {row['phone_number']}")

def add_contact():
    name = simpledialog.askstring("Add Contact", "Enter name:")
    phone = simpledialog.askstring("Add Contact", "Enter phone number:")
    if name and phone:
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, phone])
        load_contacts()

def delete_contact():
    selected = contacts_listbox.curselection()
    if selected:
        name_line = contacts_listbox.get(selected[0])
        name = name_line.split(':')[0].strip()
        new_contacts = []
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] != name:
                    new_contacts.append(row)
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'phone_number'])
            writer.writeheader()
            writer.writerows(new_contacts)
        load_contacts()
    else:
        messagebox.showinfo("Delete Contact", "Please select a contact to delete.")

def edit_contact():
    selected = contacts_listbox.curselection()
    if selected:
        current_line = contacts_listbox.get(selected[0])
        current_name, current_phone = current_line.split(':')
        new_name = simpledialog.askstring("Edit Contact", "Enter new name:", initialvalue=current_name.strip())
        new_phone = simpledialog.askstring("Edit Contact", "Enter new phone:", initialvalue=current_phone.strip())
        if new_name and new_phone:
            updated_contacts = []
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['name'] == current_name.strip():
                        updated_contacts.append({'name': new_name, 'phone_number': new_phone})
                    else:
                        updated_contacts.append(row)
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'phone_number'])
                writer.writeheader()
                writer.writerows(updated_contacts)
            load_contacts()

# 初始化 CSV 数据
initialize_csv()

# 创建 GUI
root = tk.Tk()
root.title("Phonebook")

contacts_listbox = tk.Listbox(root, width=40, height=10)
contacts_listbox.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Add", width=10, command=add_contact).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit", width=10, command=edit_contact).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", width=10, command=delete_contact).grid(row=0, column=2, padx=5)

load_contacts()

root.mainloop()
