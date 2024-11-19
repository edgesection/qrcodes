import qrcode, PIL
from PIL import Image,ImageTk
import tkinter as tk
from tkinter import ttk,messagebox,filedialog,PhotoImage
import re
import sqlite3
import time
import calendar
from datetime import datetime
from urllib.parse import urlparse
from tkinter import font

utc = time.gmtime()

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('index.db')
c = connection.cursor()

c.execute('CREATE TABLE IF NOT EXISTS links (id integer primary key, link text NOT NULL, time integer);')
c.execute('CREATE TABLE IF NOT EXISTS views (id integer primary key, id_link integer NOT NULL, time integer, FOREIGN KEY (id_link) REFERENCES links (id));')
connection.commit()

def createQR(*args):
    data = text_entry.get().lower()
    data = urlparse(data)
    data = data.netloc+data.path+""+data.query
    
    result=re.match("^((ftp|http|https):\/\/)?(www\.)?([A-Za-zА-Яа-я0-9]{1}[A-Za-zА-Яа-я0-9\-]*\.?)*\.{1}[A-Za-zА-Яа-я0-9-]{2,8}(\/([\w#!:.?+=&%@!\-\/])*)?", data) is not None
    if not result:
        messagebox.showerror("Предупреждение","Введите ссылку на сайт")
    else:
        if data:
        
            c.execute('SELECT * FROM links WHERE link = "'+data+'"')
            links = c.fetchall()
            
            existindb = 0
            id_activity = 0
            
            # Выводим результаты
            for link in links:
                existindb = 1
                id_activity = link[0]
                break
            
            
            if existindb == 0:
                c.execute('INSERT INTO links (link, time) VALUES (?,?)', (data, int(time.time())))
                connection.commit()
                id_activity = c.lastrowid
            else:
                messagebox.showwarning("Предупреждение", ''+data+' уже есть в системе')
                
            c.execute('INSERT INTO views (id_link, time) VALUES (?,?)', (id_activity, int(time.time())))
            connection.commit()
                
            img = qrcode.make(data) #generate QRcode  
            res_img = img.resize((300,300)) # reszie QR Code Size
            #Convert To photoimage
            tkimage= ImageTk.PhotoImage(res_img)
            qr_canvas.create_image(0,0,anchor=tk.NW, image=tkimage)
            qr_canvas.image = tkimage
                
        else:
            messagebox.showwarning("Предупреждение",'Введите сайт')

def saveQR():
    data = text_entry.get()
    if data:
        img = qrcode.make(data) #generate QRcode  
        res_img = img.resize((300,300)) # reszie QR Code Size
        
        path = filedialog.asksaveasfilename(defaultextension=".png",)
        if path:
            res_img.save(path)
            messagebox.showinfo("Отлично","QR Code был сохранён ")
    else:
        messagebox.showwarning("Предупреждение",'Для начала введите ссылку')
    
def top():

    c.execute('SELECT L.link as link,  COUNT(*) as views, MAX(V.time) as last_time, L.time as time FROM views V LEFT OUTER JOIN links L ON L.id = V.id_link GROUP BY V.id_link ORDER BY views DESC LIMIT 10')
    links = c.fetchall()
    
    if len(links) <= 0:
        messagebox.showwarning("Предупреждение",'Сайтов пока нет(')
        return 0

    window = tk.Tk()
    window.title("Новое окно")
    window.geometry("500x260")
    
    font1 = font.Font(family= "Arial", size=11, weight="bold", slant="roman", underline=False, overstrike=False)
    label=ttk.Label(window, text="Топ-10 сайтов:", font=font1)
    label.pack(anchor=tk.NW, expand=1, padx=[0, 20])
    
    # определяем данные для отображения
    sites = []
    
    
    # Выводим результаты
    for link in links:
        
        last_correct_time = str(datetime.fromtimestamp(link[2])).split(" ")[0].split("-")
        last_correct_time = list(reversed(last_correct_time))
        last_correct_time = '.'.join(last_correct_time)
        
        correct_time = str(datetime.fromtimestamp(link[3])).split(" ")[0].split("-")
        correct_time = list(reversed(correct_time))
        correct_time = '.'.join(correct_time)
        
        #correct_time = '.'.join(correct_time)
        sites.append(tuple([link[0], link[1], last_correct_time, correct_time]))
     
    # определяем столбцы
    columns = ("site", "views", "lsat_date", "date")
     
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.pack(fill=tk.BOTH, expand=1)
     
    # определяем заголовки
    tree.heading("site", text="Сайт")
    tree.heading("views", text="Просмотров")
    tree.heading("lsat_date", text="Последняя активность")
    tree.heading("date", text="Дата создания")
    
    tree.column("#1", stretch=tk.NO, width=150)
    tree.column("#2", stretch=tk.NO, width=80)
    tree.column("#3", stretch=tk.NO, width=140)
    tree.column("#4", stretch=tk.NO, width=90)
    
    ysb = ttk.Scrollbar(orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=ysb.set)
     
    # добавляем данные
    for site in sites:
        tree.insert("", tk.END, values=site)
    
    
def exit():
    connection.close()
    root.quit()


root = tk.Tk()
root.title("QR Code генератор")
root.geometry("350x430")
root.config(bg='white')
root.resizable(0,0)
icon = PhotoImage(file = "icon.png")
root.iconphoto(False, icon)
root.rowconfigure(index=0, weight=1)
root.columnconfigure(index=0, weight=1)

frame1 = tk.Frame(root,bd=0,relief=tk.RAISED)
frame1.place(x=25,y=0,width=300,height=300)

frame2 = tk.Frame(root,bd=5,relief=tk.RIDGE)
frame2.place(x=10,y=280,width=330,height=100)

qr_canvas = tk.Canvas(frame1)
qr_canvas.pack(fill=tk.BOTH)

image = Image.open("welcome.png")
tkimage= ImageTk.PhotoImage(image)
qr_canvas.create_image(0,0,anchor=tk.NW, image=tkimage)
qr_canvas.image = tkimage

text_entry = ttk.Entry(frame2,width=30,font=("Sitka Small",11),justify=tk.CENTER)
text_entry.bind("<Return>",createQR)
text_entry.place(x=7,y=5)

btn_1 = ttk.Button(frame2,text="Генерация",width=15,command=createQR)
btn_1.place(x=5,y=50)

btn_2 = ttk.Button(frame2,text="Сохранить",width=15,command=saveQR)
btn_2.place(x=110,y=50)

btn_3 = ttk.Button(frame2,text="Выход",width=15,command=exit)
btn_3.place(x=215,y=50)

btn_4 = ttk.Button(root,text="Топ сайтов",width=53,command=top)
btn_4.place(x=10,y=390)


root.mainloop()
