import tkinter
import pandas as pd
import sqlite3
import math
from tkinter import ttk
import numpy as np

# Gives insurance quote when data is entered in tkinter app
def get_quote():
    # Open connection to sqlite3 database
    connection = sqlite3.connect('insurance.db')
    
    # Get inputs of user from app
    age = age_spinbox.get()
    sex = sex_combobox.get()
    bmi = bmi_entry.get()
    smoke = smoke_combobox.get()
    children = children_spinbox.get()
    region = region_combobox.get()
    
    # Process inputs and make into a list
    new_user = []
    new_user.append(int(age))
    if sex == 'Female':
        new_user.append(1)
    else:
        new_user.append(0)
    new_user.append(float(bmi))
    if smoke == 'Yes':
        new_user.append(1)
    else:
        new_user.append(0)
    new_user.append(int(children))   
    if region == 'northeast':
        new_user.append(1)
    elif region == 'northwest':
        new_user.append(2)
    elif region == 'southeast':
        new_user.append(3)
    else:
        new_user.append(4)
    
    # Read and process raw data
    # Turns string data into numbers and then a categorical variable
    data = pd.read_csv('insurance.csv')
    X = data.copy()
    X['sex'] = [1 if 'female' in i else 0 for i in X['sex']]
    X['smoker'] = [1 if 'yes' in i else 0 for i in X['smoker']]
    region = []
    for i in X['region']:
        if i == 'northeast':
            region.append(1)
        if i == 'northwest':
            region.append(2)
        if i == 'southeast':
            region.append(3)
        if i == 'southwest':
            region.append(4)
    X['region'] = region

    X['sex'].astype('category');
    X['children'].astype('category');
    X['smoker'].astype('category');
    X['region'].astype('category');
    
    # Calculate Euclidean distance to all data and find ID of top 10 neighbors
    distances = []
    for i in X['id']:
        comparison = X[X['id'] == i].drop(['id', 'charges'], axis=1).to_numpy()[0]
        distance = math.dist(comparison, new_user)
        distances.append([i, distance])
    neighbors = pd.DataFrame(distances).sort_values(by=[1])[0:10][0]
    
    # Find prices based on user ID with SQL query
    cursor = connection.cursor()
    premiums = []
    for i in neighbors:
        target_id = i
        rows = cursor.execute(
            'SELECT id, charges FROM mytable WHERE id = ?',
            (target_id,),).fetchall()
        premiums.append(rows[0][1])
        
    # Get mean of 10 premiums of the neighbors and output
    final_premium = round(np.mean(premiums),2)
    insurance_output = tkinter.Label(window, text= f"Your insurance quote is {final_premium}")
    insurance_output.pack() 
        

window = tkinter.Tk()
window.title('Insurance Premium Calculator')

frame = tkinter.Frame(window)
frame.pack()

# Instruction frame for app
intro_frame = tkinter.LabelFrame(frame, text = 'Welcome!')
intro_frame.grid(row=0,column=0, padx=20,pady=20)
instruction_label = tkinter.Label(intro_frame, text='Please input all information to get a quote.')
instruction_label.grid(row=0,column=0, sticky = 'news')

# Data inputting form
info_frame = tkinter.LabelFrame(frame, text = 'User Information')
info_frame.grid(row=1,column=0, padx=20, pady=20)

age_label = tkinter.Label(info_frame, text = 'Age')
age_label.grid(row=0, column=0)
age_spinbox = tkinter.Spinbox(info_frame, from_=18, to=110)
age_spinbox.grid(row=1, column=0)

sex_label = tkinter.Label(info_frame, text = 'Sex')
sex_combobox = ttk.Combobox(info_frame, values = ['Male', 'Female'])
sex_label.grid(row=0, column = 1)
sex_combobox.grid(row=1, column = 1)

bmi_label = tkinter.Label(info_frame, text = 'BMI')
bmi_entry = ttk.Entry(info_frame)
bmi_label.grid(row=0, column = 2)
bmi_entry.grid(row=1, column = 2)

smoke_label = tkinter.Label(info_frame, text = 'Are you a Smoker?')
smoke_combobox = ttk.Combobox(info_frame, values = ['Yes', 'No'])
smoke_label.grid(row=2, column = 0)
smoke_combobox.grid(row=3, column = 0)

children_label = tkinter.Label(info_frame, text = '# of Children')
children_spinbox = tkinter.Spinbox(info_frame, from_=0, to=100)
children_label.grid(row=2, column = 1)
children_spinbox.grid(row=3, column = 1)

region_label = tkinter.Label(info_frame, text = 'Region')
region_combobox = ttk.Combobox(info_frame, values = ['Northwest', 'Northeast', 'Southeast', 'Southwest'])
region_label.grid(row=2, column = 2)
region_combobox.grid(row=3, column = 2)
#age, sex, bmi, children, smoker, region

for widget in info_frame.winfo_children():
    widget.grid_configure(padx= 10, pady =5)

#Button allowing for calculation of quote
button = tkinter.Button(frame, text = "Submit information", command = get_quote)
button.grid(row=3, column =0, sticky = "news", padx = 20, pady =5)

    
window.mainloop()
