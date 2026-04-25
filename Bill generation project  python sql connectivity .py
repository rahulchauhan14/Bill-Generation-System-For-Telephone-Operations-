import mysql.connector

def add():       #working fine

    mydb = mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")

    mycur=mydb.cursor()

    ch='y'

    while ch=="y" or ch=="Y":
        print("=========Enter the following  values============= ")
        cno=int(input("Customer no: "))
        cname=input("Customer Name: ")
        mobile=int(input("Phone no.: "))
        address=input("address: ")
        email=input("Email id.: ")
        no_calls=int(input("No. of calls: "))
        str="INSERT INTO mtnl VALUES ('{}','{}','{}','{}','{}','{}')"
        query=(str.format(cno,cname,mobile,address,email,no_calls))
        mycur.execute(query)
        mydb.commit()
        print("record inserted")
        print("==================================================")
        ch=input("want to add more record (y/n): ")
        print("==================================================")

def search():     #working fine
    
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()

    cno=int(input("Enter The Customer no. : "))
    str="select*from mtnl where cno={}"
    query=str.format(cno)
    print("==================================================")
    mycur.execute(query)
    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," ",cname," ",mobile," ",address," ",email," ",no_calls)

def display():       #working fine
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()

    mycur.execute("select*from mtnl")
    print("="*99)
    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)

def edit():         #working fine
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()
    mycur.execute("select*from mtnl")
    print("="*99)
    print("Before Updation\n")
    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)
        

    print("="*99)
    
    print("1:Update cname")
    print("2:Update mobile")
    print("3:Update address")
    print("4:Update email")
    print("5:Update no_call")
    print("="*99)
    chs=int(input("Enter your choice:"))
    if chs==1:
        edit_name()
    elif chs==2:
        edit_mobile()
    elif chs==3:
        edit_address()
    elif chs==4:
        edit_email()
    elif chs==5:
        edit_no_calls()
    elif chs==6:
         return
    else:
        print("INVATID CHOISE TRY AGAIN")
def edit_name():
    mydb= mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()
    cno=int(input("Customer no: "))
    cname=input("Customer Name: ")
    st="update mtnl set cname='%s'where cno='%s'"%(cname,cno)
    mycur.execute(st)
    mydb.commit()
    print(" Succesfully updated")
    print("="*99)

    print("after Updation\n")
    mycur.execute("select * from mtnl")

    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)


def edit_mobile():
    mydb= mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()
    cno=int(input("Customer no: "))
    mobile=input("Enter phone no. : ")
    st="update mtnl set mobile='%s'where cno='%s'"%(mobile,cno)
    mycur.execute(st)
    mydb.commit()
    print("Succesfully updated")
    print("="*99)

    
    print("after Updation\n")
    mycur.execute("select * from mtnl")

    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)


def edit_address():
    mydb= mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()
    cno=int(input("Customer no: "))
    address=input("Enter Address")
    st="update mtnl set address='%s'where cno='%s'"%(address,cno)
    mycur.execute(st)
    mydb.commit()
    print("Succesfully updated")
    print("="*99)

    print("after Updation\n")
    mycur.execute("select * from mtnl")

    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)


def edit_email():
    mydb= mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()
    cno=int(input("Customer no: "))
    email=input("Enter new Email")
    st="update mtnl set email='%s'where cno='%s'"%(email,cno)
    mycur.execute(st)
    mydb.commit()
    print(" Succesfully updated")
    print("="*99)

    print("after Updation\n")
    mycur.execute("select * from mtnl")

    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)


def edit_no_calls():
    mydb= mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()
    cno=int(input("Customer no: "))
    no_calls=int(input("Enter no of calls:"))
    st="update mtnl set no_calls='%s'where cno='%s'"%(no_calls,cno)
    mycur.execute(st)
    mydb.commit()
    print(" Succesfully updated")       

    
        
    print("="*99)

    
    print("after Updation\n")
    mycur.execute("select * from mtnl")

    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)


def delete():      # working fine
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
    mycur=mydb.cursor()
    mycur.execute("select*from mtnl")
    print("="*99)
    print("Before Deletion")
    print("="*99)

    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)
    
    
    cno=int(input("Enter The Customer no.: "))
    str="delete from mtnl where cno={}"
    query=str.format(cno)
    mycur.execute(query)
    mydb.commit()

    print("Record deleted")
    mycur.execute("select* from mtnl")
    print("="*99)
    print("After Deletion: ")
    print("="*99)

    myrec=mycur.fetchall()
    for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)


def generate():      # working fine
     mydb = mysql.connector.connect(host="localhost", user="root", passwd="84610", database="project")
     mycur=mydb.cursor()
     mycur.execute("select*from mtnl")

     myrec=mycur.fetchall()
     for x in myrec:
        cno=x[0]
        cname=x[1]
        mobile=x[2]
        address=x[3]
        email=x[4]
        no_calls=x[5]
        print(cno," | ",cname," | ",mobile," | ",address," | ",email," | ",no_calls)

     cno=int(input("Enter The Customer no.: "))
     str="select cno, cname, mobile, address, email, no_calls from mtnl where cno={}"
     query =str.format(cno)
     mycur.execute(query)

     myrec=mycur.fetchall()
     for x in myrec :
         cno=x[0]
         cname=x[1]
         mobile=x[2]
         address=x[3]
         email=x[4]
         no_calls=x[5]

         a=x[5]

         if a<=100:
             amt=200
         elif a<=150:
             amt=200+0.60*(a-100)
         elif a<=200:
             amt=200+0.60*50+50*(a-150)
         elif a>200:
             amt=200+0.60*50+0.50*50+0.40*(a-200)

         tax= round(amt*0.10,2)
         net=round(amt+tax,2)
         print("==================================================")
         print("<====           S.R.M Telecoms               ====>")
         print("==================================================")
         print("M:- 011563287                  Branch:-Gtb Nagar")
         print("==================================================")
         print("Customer no. :- ",cno)
         print("Customer name: ",cname)
         print("==================================================")
         print("Phone no.: ",mobile)
         print("Address: ",address)
         print("==================================================")
         print("Email id: ",email)
         print("No. of Calls: ",no_calls)
         print("==================================================")
         print("Your bill is Rs. ",amt)
         print("Gst: Rs. ",tax)
         print("==================================================")
         print("net amount: Rs. ",net)




ch='y'
while ch=="y" or ch=="Y":
    print("==================================================")
    print("<====             Bill Generation Telecom              ====>")
    print("==================================================")
    print("CHOICES")
    print("1. To Add New Record")
    print("2. To Search a Record")
    print("3. To Update the Record")
    print("4. To Delete a Record")
    print("5. To View all Records")
    print("6. To Generate The Bill \n")
    print("==================================================")


    ch=int(input("Enter The Choice: "))
    
    if ch==1:
        add()
    elif ch==2:
        search()
    elif ch==3:
        edit()
    elif ch==4:
        delete()
    elif ch==5:
        display()
    elif ch==6:
        generate()
    print("\n\n-------------------------------")
    ch=input("Want to See Main Menu? (y/n):  ")
