from tkinter import *
import backend_db
from tkinter import ttk
import random
import tkinter.messagebox
import datetime as dt
import pymysql
import time
import tempfile, os
import sqlite3
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import csv
from tkinter import filedialog

#frontend

conn = sqlite3.connect("translate update.db")
cursor = conn.cursor()

class Translate:

    def __init__(self, root):
        self.root = root
        blank_space = " "
        self.root.title(200*blank_space + "Translate Database Management System")
        self.root.geometry("1530x800+0+0")

        id = StringVar()
        kata = StringVar()
        arti = StringVar()
        flag = StringVar()
        sqltime = StringVar()
        sqltimeupdate = dt.datetime.now()

        #============================================functions========================================================
        def ireset():
            self.txtid.delete(0, END)
            self.txtKata.delete(0, END)
            self.txtArti.delete(0, END)
            self.txtFlag.delete(0, END)
            self.txtSqlTime.delete(0, END)
            self.txtSqlTimeUpd.delete(0, END)
            self.txtSearch.delete(0, END)
            iDisplay()


        def iDisplay():
            result = backend_db.ViewData()
            if len(result) != 0:
                self.translatelist.delete(*self.translatelist.get_children())
                for row in result:
                    self.translatelist.insert('', END, values=row)


        def add_item():
            if self.txtKata.get() == "" or self.txtArti.get() == "" :
                messagebox.showerror("Warning !", "PG English & PG Bahasa is Required")
                return
            else:
                backend_db.AddData(
                    kata.get(),
                    arti.get(),
                    flag.get(),
                    sqltime.get(),
                    sqltimeupdate
                    )
                messagebox.showinfo("Info !", "New Data have been added")
                ireset()
                iDisplay()


        def SelectItem(a):
            try:
                self.txtid.delete(0, END)
                self.txtKata.delete(0, END)
                self.txtArti.delete(0, END)
                self.txtFlag.delete(0, END)            
                self.txtSqlTime.delete(0, END)
                self.txtSqlTimeUpd.delete(0, END)

                selected_item = self.translatelist.selection()[0]
                self.txtid.insert(0, self.translatelist.item(selected_item)['values'][0])
                self.txtKata.insert(0, self.translatelist.item(selected_item)['values'][1])
                self.txtArti.insert(0, self.translatelist.item(selected_item)['values'][2])
                self.txtFlag.insert(0, self.translatelist.item(selected_item)['values'][3])
                self.txtSqlTime.insert(0, self.translatelist.item(selected_item)['values'][4])
                self.txtSqlTimeUpd.insert(0, self.translatelist.item(selected_item)['values'][5])

            except IndexError:
                pass


        def iDelete():
            respon = messagebox.askquestion("Be Noticed !", "This data will be permanently deleted")

            if respon == 'yes' :
                selected_item = self.translatelist.selection()[0]
                self.translatelist.delete(selected_item)
                cursor.execute("DELETE FROM datakamus WHERE id=" + self.txtid.get())
                conn.commit()
                ireset()
                iDisplay()
                messagebox.showinfo("Info !", "Data Successfully Deleted")
            else:
                iDisplay()
     
        def update_item():
            if self.txtKata.get() == "" or self.txtArti.get() == "" or self.txtFlag.get() == "" or self.txtSqlTime.get() == "" :
                messagebox.showerror("Warning!", "PG English, PG Bahasa, Flag, Created Time is Required")
                return
            else:   
                selected_item = self.translatelist.focus()
                self.translatelist.item(selected_item, text="", values=(
                    self.txtid.get(),
                    self.txtKata.get(),
                    self.txtArti.get(),
                    self.txtFlag.get(),
                    self.txtSqlTime.get(),
                    self.txtSqlTimeUpd
                ))
                    
                cursor.execute("""UPDATE datakamus SET 
                        kata = :kata,
                        arti = :arti,
                        flag = :flag,
                        sqltimeupdate = :sqltimeupdate

                        WHERE id = :id""",
                        {
                            'kata' : self.txtKata.get(),
                            'arti' : self.txtArti.get(),
                            'flag' : self.txtFlag.get(),
                            'sqltimeupdate': self.txtSqlTimeUpd.get(),
                            'id' : self.txtid.get()
                        })
                conn.commit()
                ireset
                iDisplay()
                messagebox.showinfo("Info !", "Data have been updated")
                #source : https://www.youtube.com/watch?v=q7KXEMkMBLk&t=18s

        def search_data():
            for item in self.translatelist.get_children():
                self.translatelist.delete(item)

            val = self.txtSearch.get()
            cursor.execute("SELECT * FROM datakamus WHERE kata LIKE ?",("%"+ val +"%",))
            users = cursor.fetchall()

            for row in users:
                self.translatelist.insert('', END, values=row)  


        def upload_file():
            try :
                file = filedialog.askopenfilename(filetypes=[("CSV File",".csv")])
                Rcsv = open(file)
                content = csv.reader(Rcsv)
                insert_records = "INSERT INTO datakamus VALUES (NULL, ?, ?, ?, ?, ?)"
                cursor.executemany(insert_records, content)
                conn.commit()
                iDisplay()
                messagebox.showinfo("Sekilas Info", "Data has been added !")
            except Exception :
                messagebox.showerror("Warning!", "Incorrect Data CSV")

        def update_bulky():
            try :
                file = filedialog.askopenfilename(filetypes=[("CSV File",".csv")])
                Rcsv = open(file)
                content = csv.reader(Rcsv)
                update_records = "UPDATE datakamus SET kata = ?, arti = ?, flag = ?, sqltime = ?, sqltimeupdate = ? WHERE id = ?"
                cursor.executemany(update_records, content)
                conn.commit()
                iDisplay()
                messagebox.showinfo("Sekilas Info", "Data has been updated !")
            except Exception :
                messagebox.showerror("Warning!", "Incorrect Data CSV")

        #============================================Frames=======================================================

        MainFrame = Frame(self.root, bd=10, width=1350, height=700, relief=RIDGE, bg="cadet blue")
        MainFrame.grid()

        TopFrame1 = Frame(MainFrame, bd=5, width=1340, height=50, relief=RIDGE)
        TopFrame1.grid(row=2, column=0, pady=8)
        TitleFrame = Frame(MainFrame, bd=7, width=1340, height=100,relief=RIDGE)
        TitleFrame.grid(row=0,column=0)
        TopFrame3 = Frame(MainFrame, bd=5, width=1340, height=500, relief=RIDGE)
        TopFrame3.grid(row=1, column=0)

        LeftFrame = Frame(TopFrame3, bd=5, width=1340, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        LeftFrame.pack(side=LEFT)
        LeftFrame1 = Frame(LeftFrame, bd=5, width=600, height=180, padx=2, pady=4, relief=RIDGE)
        LeftFrame1.pack(side=TOP, padx=0, pady=4)

        RightFrame1 = Frame(TopFrame3, bd=5, width=320, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        RightFrame1.pack(side=RIGHT)
        RightFrame1a = Frame(RightFrame1, bd=5, width=310, height=200, padx=2, pady=2, relief=RIDGE)
        RightFrame1a.pack(side=TOP)
        
        #======================================Title==========================================================
        self.lblTitle = Label(TitleFrame, font=("arial", 56,"bold"), text="Translate Manager", bd=7)
        self.lblTitle.grid(row=0, column=0, padx=132)
        
        #======================================Widget=========================================================
        self.lblid = Label(LeftFrame1, font=("arial", 12,"bold"), text="ID", bd=7, anchor='w', justify=LEFT)
        self.lblid.grid(row=0, column=0, sticky=W, padx=5)
        self.txtid = Entry(LeftFrame1, font=("arial", 12, "bold"), bd=5, width=40, justify='left', textvariable=id)
        self.txtid.grid(row=0, column=1)

        self.lblKata = Label(LeftFrame1, font=("arial", 12,"bold"), text="PG English", bd=7, anchor='w', justify=LEFT)
        self.lblKata.grid(row=1, column=0, sticky=W, padx=5)
        self.txtKata = Entry(LeftFrame1, font=("arial", 12, "bold"), bd=5, width=40, justify='left', textvariable=kata)
        self.txtKata.grid(row=1, column=1)

        self.lblArti = Label(LeftFrame1, font=("arial", 12,"bold"), text="PG Bahasa", bd=7, anchor='w', justify=LEFT)
        self.lblArti.grid(row=2, column=0, sticky=W, padx=5)
        self.txtArti = Entry(LeftFrame1, font=("arial", 12, "bold"), bd=5, width=40, justify='left', textvariable=arti)
        self.txtArti.grid(row=2, column=1)

        self.lblFlag = Label(LeftFrame1, font=("arial", 12,"bold"), text="Flag", bd=7, anchor='w', justify=LEFT)
        self.lblFlag.grid(row=3, column=0, sticky=W, padx=5)
        self.txtFlag = Entry(LeftFrame1, font=("arial", 12, "bold"), bd=5, width=40, justify='left', textvariable=flag)
        self.txtFlag.grid(row=3, column=1)

        self.lblSqlTIme = Label(LeftFrame1, font=("arial", 12,"bold"), text="Created Time", bd=7, anchor='w', justify=LEFT)
        self.lblSqlTIme.grid(row=4, column=0, sticky=W, padx=5)
        self.txtSqlTime = Entry(LeftFrame1, font=("arial", 12, "bold"), bd=5, width=40, justify='left', textvariable=sqltime)
        self.txtSqlTime.grid(row=4, column=1)

        self.lblSqlTImeUpd = Label(LeftFrame1, font=("arial", 12,"bold"), text="Updated Time", bd=7, anchor='w', justify=LEFT)
        self.lblSqlTImeUpd.grid(row=5, column=0, sticky=W, padx=5)
        self.txtSqlTimeUpd = Entry(LeftFrame1, font=("arial", 12, "bold"), bd=5, width=40, justify='left', textvariable=sqltimeupdate)
        self.txtSqlTimeUpd.grid(row=5, column=1)

        self.txtSearch = Entry(LeftFrame1, font=("arial", 12), bd=5, width=40, justify='left', textvariable=StringVar)
        self.txtSearch.grid(row=6, column=1, pady=20)

        #==============================================Tree View=========================================================
        scroll_x = Scrollbar(RightFrame1a, orient=HORIZONTAL)
        scroll_y = Scrollbar(RightFrame1a, orient=VERTICAL)

        self.translatelist = ttk.Treeview(RightFrame1a, height=14, columns=("id","kata","arti","flag","sqltime","sqltimeupdate"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.translatelist.heading("id", text="ID")
        self.translatelist.heading("kata", text="PG English")
        self.translatelist.heading("arti", text="PG Bahasa")
        self.translatelist.heading("flag", text="Flag")
        self.translatelist.heading("sqltime", text="Created Time")
        self.translatelist.heading("sqltimeupdate", text="Updated Time")

        self.translatelist['show'] = 'headings'

        self.translatelist.column("id", width=50)
        self.translatelist.column("kata", width=250)
        self.translatelist.column("arti", width=250)
        self.translatelist.column("flag", width=80)
        self.translatelist.column("sqltime", width=140)
        self.translatelist.column("sqltimeupdate", width=140)
        
        self.translatelist.pack(fill=BOTH, expand=1)
        self.translatelist.bind("<<TreeviewSelect>>", SelectItem)
        iDisplay()

        #==========================================Button=============================================================
        self.btnAddNew = Button(TopFrame1, pady=1, bd=4, font=('arial', 23, 'bold'), text="Create New", padx=10, command=add_item,
                                width=11, height=1).grid(row=0, column=0, padx=1)
        
        self.btnUpdate = Button(TopFrame1, pady=1, bd=4, font=('arial', 23, 'bold'), text="Update Data", padx=10, command=update_item,
                                width=11, height=1).grid(row=0, column=1, padx=1)
        
        self.btnDelete = Button(TopFrame1, pady=1, bd=4, font=('arial', 23, 'bold'), text="Delete Data", padx=10, command=iDelete,
                                width=11, height=1).grid(row=0, column=2, padx=1)
        
        self.btnBulky = Button(TopFrame1, pady=1, bd=4, font=('arial', 23, 'bold'), text="Bulky Add New", padx=10, command=upload_file,
                                bg="Light Green", width=11, height=1).grid(row=0, column=3, padx=1)
        
        self.btnClear = Button(TopFrame1, pady=1, bd=4, font=('arial', 23, 'bold'), text="Clear Field", padx=10, command=ireset,
                                width=11, height=1).grid(row=0, column=5, padx=1)
        
        self.btnUpdateB = Button(TopFrame1, pady=1, bd=4, font=('arial', 23, 'bold'), text="Bulky Update", padx=10, command=update_bulky,
                                bg="Light Green", width=11, height=1).grid(row=0, column=4, padx=1)
        
        self.btnSearch = Button(LeftFrame1, font=('arial', 12, 'bold'), text="Search", bd=5, bg="cadet blue", fg="white", command=search_data,
                                width=8, height=1).grid(row=6, column=0, sticky=W)






if __name__=='__main__' :
    root = Tk()
    application = Translate(root)
    root.mainloop()
