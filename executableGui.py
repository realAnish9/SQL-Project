from sqlite3.dbapi2 import Cursor
import tkinter
from datetime import datetime
from tkinter import ttk
import math
import tkinter.messagebox
from tkinter import *
import sqlite3


root=Tk()
root.title('CAR RENTAL')
root.geometry("500x500")
root.configure(bg='pale turquoise')
root.option_add('*Font','Times 15')

#==========================================(1)=======================================# 
def openCustWindow():
    custWindow=Toplevel(root)
    custWindow.title("ADD CUSTOMER")
    custWindow.geometry("500x150")
    custWindow.configure(bg='pale turquoise')
    def submitCust():
        #Connect to database
        conn=sqlite3.connect('project.db')
        cursor=conn.cursor()

        cursor.execute("INSERT INTO CUSTOMER(Name,Phone) VALUES(:name,:phone)",
            {
                'name':name.get(),
                'phone':phone.get()
            })
        #Commit Changes
        conn.commit()
        #close connections
        conn.close()
        name.delete(0,END)
        phone.delete(0,END)
        tkinter.messagebox.showinfo('INFO', 'Customer Added')

    #create input boxes
    name=Entry(custWindow,width=30)
    name.grid(row=0,column=1,padx=20)
    phone=Entry(custWindow,width=30)
    phone.grid(row=1,column=1,padx=20)

    #create labels for boxes
    nameLabel=Label(custWindow,text="Name",background='pale turquoise')
    nameLabel.grid(row=0,column=0)
    phoneLabel=Label(custWindow,text="Phone",background='pale turquoise')
    phoneLabel.grid(row=1,column=0)

    #create ADD button
    addBtn=Button(custWindow,text="ADD",command=submitCust,bg="SpringGreen2")
    addBtn.grid(row=4,column=1,padx=10)
#==========================================(2)=======================================# 
def openVehcWindow():
    vehcWindow=Toplevel(root)
    vehcWindow.title("ADD VEHICLE")
    vehcWindow.geometry("600x300")
    vehcWindow.configure(bg='pale turquoise')
    def submitVehc():
        #Connect to database
        conn=sqlite3.connect('project.db')
        cursor=conn.cursor()

        cursor.execute("INSERT INTO VEHICLE VALUES(:VIN,:Description,:Year,:Type,:Category)",
            {
                'VIN':VIN.get(),
                'Description':Description.get(),
                'Year':Year.get(),
                'Type':Type.get(),
                'Category':Category.get()
            })
        #Commit Changes
        conn.commit()
        #close connections
        conn.close()
        VIN.delete(0,END)
        Description.delete(0,END)
        Year.delete(0,END)
        Type.delete(0,END)
        Category.delete(0,END)
        tkinter.messagebox.showinfo('INFO', 'Vehicle Added')
    #create input boxes
    VIN=Entry(vehcWindow,width=30)
    VIN.grid(row=0,column=1,padx=20)
    Description=Entry(vehcWindow,width=30)
    Description.grid(row=1,column=1,padx=20)
    Year=Entry(vehcWindow,width=30)
    Year.grid(row=2,column=1,padx=20)
    Type=Entry(vehcWindow,width=30)
    Type.grid(row=3,column=1,padx=20)
    Category=Entry(vehcWindow,width=30)
    Category.grid(row=4,column=1,padx=20)

    #create labels for boxes
    VINlabel=Label(vehcWindow,text="VIN",background='pale turquoise')
    VINlabel.grid(row=0,column=0)
    descpLabel=Label(vehcWindow,text="Description",background='pale turquoise')
    descpLabel.grid(row=1,column=0)
    yearLabel=Label(vehcWindow,text="Year",background='pale turquoise')
    yearLabel.grid(row=2,column=0)
    typeLabel=Label(vehcWindow,text="Type",background='pale turquoise')
    typeLabel.grid(row=3,column=0)
    categLabel=Label(vehcWindow,text="Category",background='pale turquoise')
    categLabel.grid(row=4,column=0)

    #create ADD button
    addBtn=Button(vehcWindow,text="ADD",command=submitVehc,bg="SpringGreen2")
    addBtn.grid(row=6,column=1,padx=10)
    
#==========================================(3)=======================================# 
#define rental window. 
def openRentalWindow():
    rentalWindow = Toplevel(root)
    rentalWindow.title("Add rental info")
    rentalWindow.geometry("600x300")
    rentalWindow.configure(bg='pale turquoise')

    def submitRental():
        # first connect to database. 
        connection = sqlite3.connect("project.db")
        # need cursor to make changes / view changes. 
        cursor = connection.cursor()

        # create string to key values. 
        if(vehicleType.get()=="COMPACT"):
            value_for_vehicle=str(1)
        elif(vehicleType.get()=="MEDIUM"):
            value_for_vehicle=str(2)
        elif(vehicleType.get()=="LARGE"):
            value_for_vehicle=str(3)
        elif(vehicleType.get()=="SUV"):
            value_for_vehicle=str(4)
        elif(vehicleType.get()=="TRUCK"):
            value_for_vehicle=str(5)
        else:#(vehicleType.get()=="VAN")--> assume 
            value_for_vehicle=str(6)

        if(rentalCategory.get()=="BASIC"):
            value_for_category=str(0)
        else:
            value_for_category=str(1)

        cursor.execute("""
        
        SELECT VEHICLE.VehicleID, VEHICLE.Description,VEHICLE.Year
        FROM VEHICLE, RENTAL
        WHERE VEHICLE.VehicleID NOT IN(
            SELECT Rental.vehicleID
            FROM RENTAL, VEHICLE
            WHERE RENTAL.VehicleID=Vehicle.VehicleID AND
            (VEHICLE.Type)=? AND VEHICLE.Category=?
            AND RENTAL.ReturnDate > CAST(? AS DATE)
            AND RENTAL.StartDate < CAST(? AS DATE))
        AND VEHICLE.Type=? AND VEHICLE.Category=?
        AND RENTAL.VehicleID=Vehicle.VehicleID
        GROUP BY VEHICLE.VehicleID
        ;
        """,
        
        (value_for_vehicle,value_for_category,rentalStart.get(),rentalEnd.get(),value_for_vehicle,value_for_category,)
        
        )
        records=cursor.fetchall()
        # now commit changes. 
        connection.commit()
        connection.close() # close connection. 
        # after closing connection, reset all text boxes.     
#<-------------------------------create listbox-------------------------------->
        displayWindow = Toplevel(root)
        displayWindow.title("Available Vehicles")
        displayWindow.geometry("1000x300")
        displayWindow.configure(bg='pale turquoise')

        listbox = Listbox(displayWindow,width=100,height=100)
       

        def reserve_selection(): # reserve the car user selects. 
            value = listbox.get(listbox.curselection())# this will have the vehicle info that the user wanna rent. 
            # here value is a tuple, where value[0] is the vin of the vehicle, value[1] is the make of the car, and value[2] is the year of the car. 
            # now we need to make reservation based on the vin number of the car, since the vin is the primary key for rental table. 
            
            def confirm_reservation():

                #define functions.
                def days_between(d1, d2, r):
                    d1 = datetime.strptime(d1, "%Y-%m-%d")
                    d2 = datetime.strptime(d2, "%Y-%m-%d")
                    v = abs((d2 - d1).days)
                    if(r=="7"):
                        v=v/7
                        if(v%7!=0):
                            v=math.ceil(v)
                    return int(v)

                def calculate_total():
                    if(rentalType.get()=="DAILY"):
                        value_for_type = str(1)
                    else: # assume weekly
                        value_for_type = str(7)
                    # first connect to database. 
                    connection = sqlite3.connect("project.db")
                    # need cursor to make changes / view changes. 
                    cursor = connection.cursor()
                    cursor.execute("""
                    
                    SELECT RATE.Weekly, RATE.Daily
                    FROM RATE
                    WHERE RATE.Type=? AND RATE.Category=?
                    ;
                    """,
                    (value_for_vehicle,value_for_category,)
                    
                    )
                    rec=cursor.fetchall()

                    # now commit changes. 
                    connection.commit()
                    connection.close() # close connection. 
                    # rec [0][0] has the value of total unit charge weekly
                    # rec[0][1] has the value of total unit charge daily.
                    # now check if the rental is weekly or daily. 
                    
                    if(value_for_type=="7"): # meaning weekly. 
                        return str(days_between(rentalStart.get(),rentalEnd.get(),value_for_type)*int(rec[0][0]))
                    else:
                        return str(days_between(rentalStart.get(),rentalEnd.get(),value_for_type)*int(rec[0][1]))
            
                #Connect to database
                conn=sqlite3.connect('project.db')
                cursor=conn.cursor()
                if(rentalType.get()=="DAILY"):
                    value_for_type = str(1)
                else: # assume weekly
                    value_for_type = str(7)
                if(paymentDate.get()==""):
                    value_for_pay="NULL"
                else:
                    value_for_pay=paymentDate.get()
                cursor.execute("""INSERT INTO RENTAL(CustID,VehicleID,StartDate,OrderDate,RentalType,Qty,ReturnDate,TotalAmount,PaymentDate,Returned)
                                VALUES(:CID,:VID,:sDate,:oDate,:rType,:time,:rDate,:tAmount,:pDate,:status)
                                """,
                    {
                        'CID':custId.get(),
                        'VID':value[0],
                        'sDate':rentalStart.get(),
                        'oDate':orderDate.get(),
                        'rType':value_for_type,
                        'time':days_between(rentalStart.get(),rentalEnd.get(),value_for_type),
                        'rDate':rentalEnd.get(),
                        'tAmount':calculate_total(),
                        'pDate':value_for_pay,
                        'status':0
                    })
                #Commit Changes
                conn.commit()
                #close connections
                conn.close()
                
                tkinter.messagebox.showinfo('INFO', 'Reservation Made')

            #STEP1- RESERVATION DETAILS POPUP WINDOW. 

            detailsWindow = Toplevel(root)
            detailsWindow.title("Enter information")
            detailsWindow.geometry("1000x300")
            detailsWindow.configure(bg='pale turquoise')


            #create input boxes for detailsWindow:
            custId=Entry(detailsWindow,width=30)
            custId.grid(row=0,column=1,padx=20)
            orderDate = Entry(detailsWindow,width=30)
            orderDate.grid(row=1, column=1,padx=20)
            rentalType = Entry(detailsWindow,width=30)
            rentalType.grid(row=2, column=1,padx=20)
            paymentDate = Entry(detailsWindow,width=30)
            paymentDate.grid(row=3, column=1,padx=20)

            #create labels for boxes
            custIdlabel=Label(detailsWindow,text="Customer ID",background='pale turquoise')
            custIdlabel.grid(row=0,column=0)
            orderlabel=Label(detailsWindow,text="Order Date",background='pale turquoise')
            orderlabel.grid(row=1,column=0)
            rentallabel=Label(detailsWindow,text="Rental Type",background='pale turquoise')
            rentallabel.grid(row=2,column=0)
            paymentlabel=Label(detailsWindow,text="Payment Date",background='pale turquoise')
            paymentlabel.grid(row=3,column=0)

            #create ADD button
            submitButton=Button(detailsWindow,text="CONFIRM RESERVATION",command=confirm_reservation,bg="SpringGreen2")
            submitButton.grid(row=4,column=1,padx=10)

        counter=1
        b1 = Button(displayWindow, text='Select the vehicle and then click here to reserve.', width=100, height=2, command=reserve_selection,bg="SpringGreen2")
        b1.pack()
        for x in records:
            listbox.insert(counter,x)
            counter=counter+1

        listbox.pack()
    
    # create input boxes to take the rental information. --> this is the first question window popup. 
    vehicleType = Entry(rentalWindow,width=30)
    vehicleType.grid(row=0, column=1)
    rentalCategory = Entry(rentalWindow,width=30)
    rentalCategory.grid(row=1, column=1)
    rentalStart = Entry(rentalWindow,width=30)
    rentalStart.grid(row=2, column=1)
    rentalEnd = Entry(rentalWindow,width=30)
    rentalEnd.grid(row=3, column=1)

    # create input label for the above boxes. 
    rentalTypeLabel = Label(rentalWindow, text="Vehicle Type",background='pale turquoise')
    rentalTypeLabel.grid(row=0, column=0)
    rentalCategoryLabel = Label(rentalWindow, text="Vehicle Category",background='pale turquoise')
    rentalCategoryLabel.grid(row=1, column=0)
    rentalStartLabel = Label(rentalWindow, text="Start Date",background='pale turquoise')
    rentalStartLabel.grid(row=2, column=0)
    rentalEndLabel = Label(rentalWindow, text="Return Date",background='pale turquoise')
    rentalEndLabel.grid(row=3, column=0)

    # create add button. 
    addButton = Button(rentalWindow,text="SEARCH",command=submitRental,bg='SpringGreen2')
    addButton.grid(row=5,column=1,padx=10)

#==========================================(5)=======================================# 
def openListCustWindow():
    listCustWindow=Toplevel(root)
    listCustWindow.title("List Customer")
    listCustWindow.geometry("500x300")
    listCustWindow.configure(bg='pale turquoise')
    listCustWindow.option_add('*Font','Times 12')

    def search():
        #Connect to database
        conn=sqlite3.connect('project.db')
        cursor=conn.cursor()
        if len(custName.get())==0 and len(custId.get())==0:
            cursor.execute("""SELECT Name,
            CASE
                WHEN R.PaymentDate="NULL" THEN SUM(TotalAmount)
                ELSE "0.00"
            END AS Balance
            FROM CUSTOMER AS C, RENTAL AS R
            WHERE R.CustID=C.CustID
            GROUP BY NAME
            ORDER BY Balance""")
            result=cursor.fetchall()
        else:
            cursor.execute("""SELECT Name,
            CASE
                WHEN R.PaymentDate="NULL" THEN SUM(TotalAmount)
                ELSE "0.00"
            END AS Balance
            FROM CUSTOMER AS C, RENTAL AS R
            WHERE C.Name=:custName AND C.Name LIKE :custName AND C.CustID=R.CustID
            GROUP BY NAME""",
            {
                'custID':custId.get(),
                'custName':custName.get()
            }
            )
            result=cursor.fetchall()
            print(custName.get())
            #(C.CustID=:custID OR C.Name=:custName OR C.Name LIKE :custName)
        i=5
        custTitle=Entry(listCustWindow, width=20, fg='red')
        custTitle.grid(row=4,column=0)
        custTitle.insert(END,"Customer Name")
        custTitle=Entry(listCustWindow, width=20, fg='red')
        custTitle.grid(row=4,column=1)
        custTitle.insert(END,"Balance")
        for line in result: 
            for j in range(len(line)):
                e = Entry(listCustWindow, width=20, fg='green') 
                e.grid(row=i, column=j) 
                if j==1:
                    if len(str(line[j]))==0:
                        e.insert(END, "$"+str(line[j])+".00")
                    else:
                       e.insert(END, "$"+str(line[j])) 
                else:
                    e.insert(END, str(line[j]))
            i=i+1
        #Commit Changes
        conn.commit()
        #close connections
        conn.close()

    custName=Entry(listCustWindow,width=30)
    custName.grid(row=0,column=1,padx=20)
    custId=Entry(listCustWindow,width=30)
    custId.grid(row=1,column=1,padx=20)

    custNameLabel=Label(listCustWindow,text="Customer Name",background='pale turquoise')
    custNameLabel.grid(row=0,column=0)
    custIdLabel=Label(listCustWindow,text="Customer ID",background='pale turquoise')
    custIdLabel.grid(row=1,column=0)

    #create search button
    addBtn=Button(listCustWindow,text="Search",command=search,bg="SpringGreen2")
    addBtn.grid(row=3,column=1,padx=10)


#==========================================(5)=======================================# 
def openListVehcWindow():

    listVehcWindow=Toplevel(root)
    listVehcWindow.title("List Vehicle")
    listVehcWindow.geometry("500x100")
    listVehcWindow.configure(bg='pale turquoise')
    listVehcWindow.option_add('*Font','Times 15')


    def searchVehc():
        notroot=Tk()
        notroot.geometry("450x700")
         #create A Main frame

        listVechFrame=Frame(notroot)
        listVechFrame.pack(fill=BOTH,expand=1)

        #create a Canvas
        myCanvas=Canvas(listVechFrame)
        myCanvas.pack(side=LEFT,fill=BOTH,expand=1)

        #create a scroll bar
        myscrollbar=ttk.Scrollbar(listVechFrame,orient=VERTICAL,command=myCanvas.yview)
        myscrollbar.pack(side=RIGHT,fill=Y)

        #config canvas
        myCanvas.configure(bg='pale turquoise',yscrollcommand=myscrollbar.set)
        #myCanvas.bind('<Configure>', Lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))

        #create another frame
        secondFrame=Frame(myCanvas)

        #Add window
        myCanvas.create_window((0,0),window=secondFrame,anchor="nw")
        #Connect to database
        conn=sqlite3.connect('project.db')
        cursor=conn.cursor()
        if len(VIN.get())==0 or len(description.get())==0:
            cursor.execute("""SELECT V.VehicleID,Description,
            CASE
                WHEN V.VehicleID NOT IN (SELECT RENTAL.VehicleID FROM RENTAL) THEN "NON APPLICABLE"
                ELSE CAST(Daily AS NUMERIC(10,2))*100/100 
            END AS DailyPrice
            FROM VEHICLE AS V,RATE AS R, RENTAL
            WHERE V.Type=R.Type AND V.Category=R.Category
            GROUP BY V.VehicleID
            ORDER BY DailyPrice 
            """)
            result=cursor.fetchall()
        else:
            cursor.execute("""SELECT V.VehicleID,Description,
            CASE
                WHEN V.VehicleID NOT IN (SELECT RENTAL.VehicleID FROM RENTAL) THEN "NON APPLICABLE"
                ELSE Daily
            END AS DailyPrice
            FROM VEHICLE AS V,RATE AS R, RENTAL
            WHERE V.Type=R.Type AND V.Category=R.Category
            AND V.VehicleID=:VIN
            GROUP BY V.VehicleID
            ORDER BY DailyPrice 
            """,
            {
                'VIN':VIN.get(),
            })
            result=cursor.fetchall()
        
        #print results in new window
        i=2
        VINTitle=Entry(secondFrame, width=23, fg='red')
        VINTitle.grid(row=1,column=0)
        VINTitle.insert(END,"VIN")
        descTitle=Entry(secondFrame, width=23, fg='red')
        descTitle.grid(row=1,column=1)
        descTitle.insert(END,"Description")
        priceTitle=Entry(secondFrame, width=23, fg='red')
        priceTitle.grid(row=1,column=2)
        priceTitle.insert(END,"Daily Price")
        for line in result: 
            for j in range(len(line)):
                ev = Listbox(secondFrame, height=1,width=23, fg='black',bg="deep sky blue")
                ev.grid(row=i, column=j) 
                if(j==2):
                    if line[2]=="NON APPLICABLE":
                        ev.insert(END, str(line[j]))
                    else:
                        ev.insert(END, "$"+str(line[j])+".00")
                else:
                    ev.insert(END, line[j])
            i=i+1
        #Commit Changes
        conn.commit()
        #close connections
        conn.close()

    #create input boxes
    VIN=Entry(listVehcWindow,width=30)
    VIN.grid(row=0,column=1,padx=20)
    description=Entry(listVehcWindow,width=30)
    description.grid(row=1,column=1,padx=20)

    #create labels for input boxes
    VINLabel=Label(listVehcWindow,text="VIN",background='pale turquoise')
    VINLabel.grid(row=0,column=0)
    descripLabel=Label(listVehcWindow,text="Description",background='pale turquoise')
    descripLabel.grid(row=1,column=0)

    #create search button
    addBtn=Button(listVehcWindow,text="Search",command=searchVehc,bg="SpringGreen2")
    addBtn.grid(row=3,column=1,padx=10)

#===========================Creating View Rental Window(4)===================================#  
def openViewRentWindow():
    viewRentWindow=Toplevel(root)
    viewRentWindow.title("View Rental")
    viewRentWindow.geometry("800x500")
    viewRentWindow.configure(bg='pale turquoise')
    viewRentWindow.option_add('*Font','Times 15')

    def submitSearch():
        #Connect to database
        conn=sqlite3.connect('project.db')
        cursor=conn.cursor()
        cursor.execute("""SELECT RENTAL.TotalAmount, VEHICLE.Description, VEHICLE.VehicleID
        FROM VEHICLE, RENTAL,CUSTOMER
        WHERE  RENTAL.VehicleID = VEHICLE.VehicleID AND CUSTOMER.Name=:name AND CUSTOMER.CustID=RENTAL.CustID AND VEHICLE.VehicleID=:vec_id AND Rental.PaymentDate='NULL'""",
        {
            'return':returnDate.get(),
            'name':custName.get(),
            'vec_id':vid.get(),
        })
        result=cursor.fetchall()

        i=6
        

            
        amountTitle=Entry(viewRentWindow, width=15, fg='red')
        amountTitle.grid(row=5,column=0)
        amountTitle.insert(END,"Amount")
        descTitle=Entry(viewRentWindow, width=15, fg='red')
        descTitle.grid(row=5,column=1)
        descTitle.insert(END,"Description")
        vechIDTitle=Entry(viewRentWindow, width=15, fg='red')
        vechIDTitle.grid(row=5,column=2)
        vechIDTitle.insert(END,"VIN")
        for line in result: 
            for j in range(len(line)):
                ev = Listbox(viewRentWindow, height=1,width=23, fg='black',bg="deep sky blue")
                ev.grid(row=i, column=j) 
                ev.insert(END, line[j])
        i=i+1

        def payment():
            conn=sqlite3.connect('project.db')
            cursor=conn.cursor()
            cursor.execute("""UPDATE RENTAL SET Returned=1,
            PaymentDate='2020-12-17'
            WHERE Rental.VehicleID=:vec_id AND Rental.ReturnDate=:return
            """,
            {
                'return':returnDate.get(),
                'vec_id':vid.get(),
            })
            tkinter.messagebox.showinfo('INFO', 'Payment Succesfull')
            #Commit Changes
            conn.commit()
            #close connections
            conn.close()

        #Commit Changes
        conn.commit()
        #close connections
        conn.close()
        updateBtn=Button(viewRentWindow,text="Pay",command=payment,bg="SpringGreen2")
        updateBtn.grid(row=8,column=1,padx=10)

        

    #create input boxes
    returnDate=Entry(viewRentWindow,width=30)
    returnDate.grid(row=0,column=1,padx=20)
    custName=Entry(viewRentWindow,width=30)
    custName.grid(row=1,column=1,padx=20)
    vid=Entry(viewRentWindow,width=30)
    vid.grid(row=2,column=1,padx=20)

    #create labels for boxes
    returnLabel=Label(viewRentWindow,text="Return Date",background='pale turquoise')
    returnLabel.grid(row=0,column=0)
    nameLabel=Label(viewRentWindow,text="Your Name",background='pale turquoise')
    nameLabel.grid(row=1,column=0)
    vinLabel=Label(viewRentWindow,text="Vehicle VIN",background='pale turquoise')
    vinLabel.grid(row=2,column=0)

    #create Search button
    searchBtn=Button(viewRentWindow,text="Retrive",command=submitSearch,bg="SpringGreen2")
    searchBtn.grid(row=4,column=1,padx=10)

#===========================Creating Buttons for main window===================================#    
custBtn=Button(root,text="Add Customer",command=openCustWindow,bg="deep sky blue")
custBtn.pack(pady=10)
custBtn.configure(height=2,width=20)

vehcBtn=Button(root,text="Add Vehicle",command=openVehcWindow,bg="deep sky blue")
vehcBtn.pack(pady=10)
vehcBtn.configure(height=2,width=20)

rentBtn=Button(root,text="Search Rental",command=openRentalWindow,bg="deep sky blue")
rentBtn.pack(pady=10)
rentBtn.configure(height=2,width=20)

viewRentBtn=Button(root,text="Return Car",command=openViewRentWindow,bg="deep sky blue")
viewRentBtn.pack(pady=10)
viewRentBtn.configure(height=2,width=20)

listCustBtn=Button(root,text="List Customers",command=openListCustWindow,bg="deep sky blue")
listCustBtn.pack(pady=10)
listCustBtn.configure(height=2,width=20)

listVehcBtn=Button(root,text="List Vehicles",command=openListVehcWindow,bg="deep sky blue")
listVehcBtn.pack(pady=10)
listVehcBtn.configure(height=2,width=20)
#===============================================================================================#
root.mainloop()

'''conn=sqlite3.connect('project.db')
cursor=conn.cursor()
cursor.execute("SELECT *FROM CUSTOMER")
custData=cursor.fetchall()
for row in custData:
    print(row)'''
