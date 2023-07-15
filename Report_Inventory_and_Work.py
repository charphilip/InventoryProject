"""
Author: Felipe Patino
Python Program Project CIT 295
Purpose: The purpose of the program is to assist Quinta Los Santos in managing its product inventory by facilitating the 
insertion, updating, and deletion of items. It also aims to generate individual reports for employees based on 
their work hours and inventory usage 
Steps:
• Use a CSV file to manage the company's product inventory.
    o The user can add, delete, or modify products in the file.
    o The user can view the inventory using a menu option.
• Work Report (Date will be added in each step)
    o The worker can select items from the inventory, ensuring it remains updated.
    o Once the job starts, the worker will input the Work Order, name, and quantity of items.
Afterward, the program will display a message based on the inputs. The worker's name will be associated with the chosen item in the inventory until the job is completed.
    o When the job is finished, the worker can choose an option to input the work time and provide a report on the finished items.
"""

import pandas as pd
import datetime
from datetime import tzinfo, timedelta, datetime
import numpy as np

df = ""
# This function will call the entire program. Here, there is a simple menu to navigate in the program. 
def main():
    #Exception errors
    try:
        print("PROJECT INVENTORY & WORK HOURS\n")
        print("1) Get the inventory\n2) Add a new item\n3) Delete item\n4) Modify item\n5) Select items (Worker)\n6) Work Hours (Worker)\n7) Exit")
        optionuser = int(input("What option you want? "))
        option_inventory(optionuser)
    
    except FileNotFoundError as file_not_found_err:
        # This code will be executed if the user enters
        # the name of a file that doesn't exist.
        print()
        print(type(file_not_found_err).__name__, file_not_found_err, sep=": ")
        print("Run the program again and check the file.")
    
    except PermissionError as perm_err:
        # This code will be executed if the user enters the name
        # of a file and doesn't have permission to read that file.
        print()
        print(type(perm_err).__name__, perm_err, sep=": ")
        print("Run the program again and verify you do not have the file opens.")
    
    except ValueError as val_err:
        # This code will be executed if the user enters
        # an invalid integer for the line number.
        print()
        print(type(val_err).__name__, val_err, sep=": ")
        print("You entered an invalid integer for the line number.")
        print("Run the program again and enter an integer for the line number.")
    
    except Exception as excep:
        # This code will be executed if some other type of exception occurs.
        print()
        print(type(excep).__name__, excep, sep=": ")

# This funciont will open the file using PANDAS, then it will handle the menu according to the user input
def option_inventory(option):
        df = pd.read_csv('report_inventory.csv', index_col=0)
        if(option == 1):
            print(df.to_string(index=False))
            print()
            main()
        if(option == 2):
            product_name = input("New product name: ")
            quantity_stock = int(input("How many items are entering? "))
            date_expired = ObtainDate()
            add_items(product_name,quantity_stock,date_expired, df)
            print("Item added")
            main()
        elif(option == 3):
            print((df[['Item ID','Product Name']]).to_string(index=False))
            index_drop = int(input("What item you want to delete? "))
            remove_items(df, index_drop)
            print(f"The item was removed")
            main()
        elif(option == 4):
            print((df[['Item ID', 'Product Name']]).to_string(index=False))
            index_modify = int(input("What item you want to modify? "))
            modify_items(df, index_modify)
            print("The item was modified")
            main()
        elif(option == 5):
            print((df[['Item ID', 'Product Name']]).to_string(index=False))
            select_items(df)
            print(df)
            main()
        elif(option == 6):
            work_hours(df)
            # print(df)
            main()
        elif(option == 7):
            print("Bye....")
            exit()
        else:
            print("Invalid option")
            main()
# This funcition will add items in the file inventory. It will require three different information. Then, it will call a function to save a file 
# the new data in the actual file. 
def add_items(product_name, quantity_stock, date_expired, file):
    length_file = file.index.max()
    new_ID = length_file + 2
    new_row = {'Item ID': new_ID, 'Product Name': product_name , 
                    'Quantity in Stock':quantity_stock, 'Quantity Available': quantity_stock,
                    'Date Expired':date_expired}
    add = file.append(pd.DataFrame([new_row], ignore_index=True))
    # add = pd.DataFrame(new_row)
    save_file(add)
    
    #length_file_sum = length_file + 1

# This function will remove a selected item from the file. Then, it will call a function to save the file  
def remove_items(file, index_drop):
    correct_index = index_drop - 1
    remove_item = file.drop([file.index[correct_index]])
    save_file(remove_item)
# This function will modify a selected item from the file, first it will find the item and then it will change the values in the inventory.
# Then, it will call a function to save the file 
def modify_items(file, index_modify):
    name_product = input("Product: ")
    quantity_stock = int(input("Quantity in Stock: "))
    quantity_available = int(input("Quantity Available: "))
    file.loc[index_modify-1,['Product Name','Quantity in Stock','Quantity Available']] = [name_product,quantity_stock,quantity_available]
    save_file(file)

# This function will save the file 
def save_file(file):
    file.to_csv('report_inventory.csv')

#This function will be selected by the worker. It will require name and the  work order to add them in the inventory.
# Additional, it will require to select the items the worker needs, it will find the item and it will add the name and quantity entered by the user
# The original file will be updated. Into the function, the date will be evaluated by other function. 
def select_items(file):
    select = -1
    worker = input("\nWhat is your name? ")
    work_order = input("What is the number for the work order: ")
    while select != 0:
        print("Please, enter the ID for the item you want to use. Once you finish type number 0")
        select = int(input("-> "))
        if select != 0:
            current_date = datetime.today().strftime('%Y-%m-%d')
            quantity = int(input("How many do you need? -> "))
            new_quantity = file['Quantity in Stock'] - file['Quantity used']
            file.loc[select-1,['Used by','Quantity used', 'Work Order Day', 'Work Order Number']] = [worker,quantity, current_date,work_order]
            file['Quantity Available']=new_quantity
            save_file(file)

# This function will request to the user a report of work hours and the work order. Then, it will save a new file with the information provided. 
def work_hours(file):
    order = input("What is the order? ")
    name = input("Your name -> ")
    work_time = ObtainTime()
    convert_sec = int(work_time.total_seconds() / 60)
    convert_hour = int(convert_sec / 60)
    data_dict = {'ORDER': [order], 
                'WORKER': [name], 
                'TIME(HOURS)': [convert_hour]}
    data = pd.DataFrame(data_dict)
    data.to_csv("WorkHours.csv", index=False)

# This function will evaluate dates according to a specific format. 
def ObtainDate():
    isValid=False
    while not isValid:
        user_expiration_date = input("Date Expired: mm/dd/yy: ")
        try:
            date_item = datetime.strptime(user_expiration_date, "%m/%d/%y")
            isValid=True
        except:
            print ("Invalid Format!\n")
    return date_item

# This function will evaluate times according to a specific format. 
def ObtainTime():
    isValid=False
    while not isValid:
        user_time_1 = input("Enter the start hour Ex.(11:00) Format 24 H -> ")
        user_time_2 = input("Enter the final hour Ex.(18:00) Format 24 H -> ")
        try:
            hour_work_1 = datetime.strptime( user_time_1, "%H:%M")
            hour_work_2 = datetime.strptime(user_time_2, "%H:%M")
            # convert = hour_work_1.strftime("%I:%M %p")
            # convert2 = hour_work_2.strftime("%I:%M %p")
            
            isValid=True
            total_time = hour_work_2 - hour_work_1
            
        except:
            print ("Invalid Format!\n")
    return total_time

if __name__ == "__main__":
    main()


