import tkinter
from tkinter import *
from tkinter import filedialog
import temp
import pandas as pd
top = tkinter.Tk()
top.title("Stock Price Prediction")
top.geometry("1000x500")
top.config(bg='#659DBD')

def file_diag(): #open file dialog
    global folder_path
    global total_data
    filename = filedialog.askopenfilename()
    folder_path.set(filename)
    
    filename=filename.replace("/","\\\\")
    df=pd.read_csv(filename)
    total_data.set(df.shape[0])
    

def predict_stock():
    global train_dat
    if folder_path.get()=="":
        messagebox.showerror("Retry", "Choose Data Set to continue")
        return
    try:
        int(train_data.get())
        if int(train_data.get())>=int(total_data.get()):
            messagebox.showerror("Retry", "Train Data should be Strictly less than Total Data")
        else:
            temp.predict(folder_path,int(train_data.get()))
    except:
        if train_data.get()=="":
            messagebox.showerror("Retry", "Train data cannot be empty")
        else:
            messagebox.showerror("Retry", "Train data should contain only numbers")
folder_path = StringVar()
total_data = StringVar()
train_data = StringVar()
#LABLE FOLDER PATH
Label(top, text = "Dataset : ",
      font=("Arial", 15),
      bg='#659DBD').place(x = 40,y = 100)
Label(master=top,textvariable=folder_path,
             borderwidth=1, 
             relief="solid",
             width=70).place(x = 180,y = 107)
#BROWSE BUTTON
Button(text="Browse", 
       command=file_diag,
       relief=SUNKEN).place(x = 770,y = 100)

#LABLE TOTAL DATA
Label(top, text = "Total Data : ",font=("Arial", 15),bg='#659DBD').place(x = 350,y = 150) 
Label(master=top,textvariable=total_data, 
             borderwidth=1, 
             relief="solid",
             width=10).place(x = 520,y = 155)

#LABLE TEST DATA
Label(top, text = "Test Data : ",font=("Arial", 15),bg='#659DBD').place(x = 350,y =200) 
Entry(master=top, textvariable = train_data,
             borderwidth=1, 
             relief="solid",
             width=10).place(x = 520,y = 205)

PredictBTN = Button(text="Predict", 
                    command=predict_stock,
                    relief=GROOVE,
                    ).place(relx=0.5, rely=0.58,anchor=CENTER)
top.mainloop()