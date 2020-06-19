#----------
#comment included
class Customer:
    def __init__(self,cursor,cnx):
        self.cursor=cursor
        self.cnx=cnx
    def signup(self):
        print("------------------------------")
        print("          SIGN UP             ")
        print("------------------------------")
        cus_id=input("Enter your id:")
        name=input("Enter your name:")
        phone_no=input("Enter your phone number:")
        password=input("Enter the password")
        address=input("Enter your address:")
        query="INSERT INTO customer(cus_id,name,phone_no,password,address) VALUES( %s, %s, %s,%s,%s)"
        self.cursor.execute(query,(cus_id,name,phone_no,password,address))
        self.cnx.commit()
        self.customer_home( )
    def signin(self):
        print("------------------------------")
        print("           SIGNIN             ")
        print("------------------------------")
        name=input("Enter your name:")
        password=input("Enter your password:")
        query="SELECT name,password FROM customer WHERE name=%s and password=%s"
        self.cursor.execute(query,(name,password))
        val=self.cursor.fetchone()

        query="SELECT cus_id FROM customer WHERE name=%s and password=%s"
        self.cursor.execute(query,(name,password))
        cus=self.cursor.fetchone()
        cus_id=cus[0]

        query="SELECT address FROM customer WHERE name=%s and password=%s"
        self.cursor.execute(query,(name,password))
        addd=self.cursor.fetchone()
        address=addd[0]

        if(val==None):
            print("Wrong password")
        else:
            self.customer_home(cus_id,address)

    def customer_home(self,cus_id,address):

    
        print("------------------------------")
        print("          Home page           ")
        print("------------------------------")
        print('''
            1.Search item
            2.display item
            3.Cart
            4.Buyed product
            5.Logout
        ''')
        choice=int(input("Enter your choice:"))
        if(choice==1):
            item=input("Enter the item:")
            query="SELECT item_id,item_name,price,specification,quantity FROM product WHERE item_name=%s and item_name=%s"
            self.cursor.execute(query,(item,item))
            i=self.cursor.fetchone()
            item_id,item_name,price,specification,quantity=i
            print('{} - {}- Rs.{} - {} '.format(item_id,item_name,price,specification))
            
            print('''
            1.Buy
            2.Add to cart
            3.back
            ''')
            ch=int(input("Enter your choice:"))
            if(ch==1):
                print("Available quantity::",quantity)
                self.buy(item_id,cus_id,address)
            elif(ch==2):
                self.add_to_cart(item_id,cus_id,address)
            elif(ch==3):
                self.customer_home(cus_id,address)
            else:
                print("Invalid entry")
                self.customer_home(cus_id,address)


        elif(choice==2):
            query="SELECT item_id,item_name,price FROM product"
            self.cursor.execute(query)
            lst1=self.cursor.fetchall()   
            print("item ID - item name   -   price ")
            for item in lst1:
                a,b,c=item
                print('>{} - {} - Rs.{}'.format(a,b,c)) 
            i_id=input("Enter the itemID going to buy:")
            query="SELECT item_name,specification,quantity FROM product WHERE item_id=%s and item_id=%s"
            self.cursor.execute(query,(i_id,i_id))
            lst2=self.cursor.fetchone()
            a,b,quantity=lst2
            print("------------------------------------")
            print("Product name:",a)
            print("Specification:",b)
            
            print("------------------------------------")
            print('''
            1.Buy
            2.Add to cart
            3.back
            ''')
            
            ch=int(input("Enter your choice:"))
            if(ch==1):
                print("Available quantity::",quantity)
                self.buy(i_id,cus_id,address)
                self.customer_home(cus_id,address)
            elif(ch==2):
                self.add_to_cart(i_id,cus_id,address)
                self.customer_home(cus_id,address)
            elif(ch==3):
                self.customer_home(cus_id,address)
            else:
                print("Invalid entry")
        elif(choice==3):
            print("------------------------------")
            print("         CART ITEM            ")
            print("------------------------------")
            query1="SELECT item_id FROM cart WHERE cus_id=%s and cus_id=%s"
            self.cursor.execute(query1,(cus_id,cus_id))
            lst=self.cursor.fetchall()
            query2="SELECT item_id,item_name,price FROM product WHERE item_id=%s and item_id=%s"
            for i in lst:
                self.cursor.execute(query2,(i[0],i[0]))
                l=self.cursor.fetchone()
                a,name,price=l
                print('>{} - {} - Rs.{}'.format(a,name,price))
            
            
            print('''
            1.Buy
            2.Remove from the cart
            3.Back
            ''')
            n=int(input("Enter the choice:"))
            if(n==1):
                i_id=input("Enter the itemID going to buy:")
                self.buy(i_id,cus_id,address)
                self.customer_home(cus_id,address)
            elif(n==2):
                i_id=input("Enter the itemID going to remove:")
                self.remove_from_cart(i_id,cus_id,address)
                self.customer_home(cus_id,address)
            elif(n==3):
                self.customer_home(cus_id,address)
            else:
                print("Invalid entry")
                self.customer_home(cus_id,address)


            
        elif(choice==4):
            
            query1="SELECT item_id,quantity,status FROM buyed_product WHERE cus_id=%s and cus_id=%s"
            self.cursor.execute(query1,(cus_id,cus_id))
            lst1=self.cursor.fetchall()

            for i in lst1:
                item_id,quantity,status=i
                self.status(cus_id,item_id)
                query2="SELECT item_name,price,specification FROM product WHERE item_id=%s and item_id=%s"
                self.cursor.execute(query2,(item_id,item_id))
                lst2=self.cursor.fetchone()
                item_name,price,specification=lst2
                print(">{} - Rs.{} - {} - ({})".format(item_name,price*quantity,specification,status))
            self.customer_home(cus_id,address)

        elif(choice==5):
            pass
        else:
            print("Invalid entry")

    def remove_from_cart(self,item_id,cus_id,address):
        query="DELETE FROM cart WHERE item_id=%s and cus_id=%s"
        self.cursor.execute(query,(item_id,cus_id))
        self.cnx.commit()
        print("Item removed from the cart")
        self.customer_home(cus_id,address)



    def status(self,cus_id,item_id):
        query1="SELECT ordered_date,delivery_date FROM buyed_product WHERE cus_id=%s and item_id=%s"
        self.cursor.execute(query1,(cus_id,item_id))
        lst1=self.cursor.fetchone()
        ordered_date,delivery_date=lst1
        today=date.today()+timedelta(7)
        if(today==ordered_date):
            query1="UPDATE buyed_product SET status='Not delivered' WHERE cus_id=%s and item_id=%s"
            self.cursor.execute(query1,(cus_id,item_id))
            self.cnx.commit()
        elif(today==delivery_date):
            query2="UPDATE buyed_product SET status='Delivered' WHERE cus_id=%s and item_id=%s"
            self.cursor.execute(query2,(cus_id,item_id))
            self.cnx.commit()
        elif(today>delivery_date):
            query3="UPDATE buyed_product SET status='Delivered' WHERE cus_id=%s and item_id=%s"
            self.cursor.execute(query3,(cus_id,item_id))
            self.cnx.commit()
        




    def buy(self,item_id,cus_id,address):
        quantity=int(input("Enter the quantity you want::"))
        delivery_date=date.today()+timedelta(7)
        ordered_date=date.today()
        
        query1="INSERT INTO buyed_product(cus_id,item_id,quantity,address,ordered_date,delivery_date) VALUES(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(query1,(cus_id,item_id,quantity,address,ordered_date,delivery_date))
        self.cnx.commit()

        query2="UPDATE product SET quantity=quantity-%s WHERE item_id=%s"
        self.cursor.execute(query2,(quantity,item_id))
        self.cnx.commit()

        query4="UPDATE buyed_product SET status='Not delivered' WHERE item_id=%s and cus_id=%s"
        self.cursor.execute(query4,(item_id,cus_id))
        self.cnx.commit()

        query3="SELECT item_name,price FROM product WHERE item_id=%s and item_id=%s"
        self.cursor.execute(query3,(item_id,item_id))
        lst=self.cursor.fetchone()
        item_name,price=lst
        print("item name:",item_name)
        print("total price:",quantity*price)
        print("Delivery date:",delivery_date)

        

    def add_to_cart(self,item_id,cus_id,address):
        query="INSERT INTO cart(cus_id,item_id) VALUES(%s,%s)"
        self.cursor.execute(query,(cus_id,item_id))
        self.cnx.commit()

        print("item added to the cart....")
        self.customer_home(cus_id,address)

class Admin:
    def __init__(self,cursor,cnx):
        self.cursor=cursor
        self.cnx=cnx

    def signin(self):
        print("------------------------------")
        print("         SIGNIN PAGE          ")
        print("------------------------------")
        name=input("Enter your name:")
        password=input("Enter your password:")
        query="SELECT name,password FROM admin WHERE name=%s and password=%s"
        self.cursor.execute(query,(name,password))
        val=self.cursor.fetchone()

    
        if(val==None):
            print("Wrong password")
        else:
            self.admin_home()

    
    def product(self):
        query="SELECT item_id,item_name,quantity,price FROM product"
        self.cursor.execute(query)
        lst=self.cursor.fetchall()   
        for item in lst:
            a,b,c,d=item
            print('+{} - {} - {} - Rs{}'.format(a,b,c,d))
        c=int(input('''
            1.add product
            2.remove product
            3.back
            '''))
        if(c==1):
           item_id=input("Enter the item ID:") 
           item_name=input("Enter the item name:")
           price=int(input("Enter price of the item:"))
           specification=input("Enter item specificaiton:")
           quantity=int(input("Enter the quantity:"))
           query="INSERT INTO product(item_id,item_name,price,specification,quantity) VALUES(%s,%s,%s,%s,%s)"
           self.cursor.execute(query,(item_id,item_name,price,specification,quantity))
           self.cnx.commit()
           print("added succesfully")
           self.admin_home()
        elif(c==2):
            item_id=input("Enter the item ID")
            query="DELETE FROM product WHERE item_id=%s and item_id=%s"
            self.cursor.execute(query,(item_id,item_id))
            self.cnx.commit()
            print("Removed successfully")
            self.admin_home()
        elif(c==3):
            self.admin_home()
        else:
            print("Invalid entry")

    def quantity(self):
        print('''
            1.add quantity
            2.remove quantity
            3.back
            ''')
        ch=int(input("Enter your choice:"))
        if(ch==1):
            query="SELECT item_id,item_name,quantity FROM product"
            self.cursor.execute(query)
            lst=self.cursor.fetchall()   
            for item in lst:
                a,b,c=item
                print('>{} - {} - {}'.format(a,b,c))

            item_id=input("Enter the item ID:")
            q="SELECT item_name FROM product WHERE item_id=%s and item_id=%s"
            self.cursor.execute(q,(item_id,item_id))
            i=self.cursor.fetchone()
            prod_name=i[0]
            choice=input('sure this ({}) product [yes/no]? '.format(prod_name))
            if(choice=='yes' or choice=='y'):
                aq=input("Enter the number of quantity:")
                query="UPDATE product SET quantity=quantity+%s WHERE item_id=%s"
                self.cursor.execute(query,(aq,item_id))
                self.cnx.commit()
                print(aq+" item added successfully")
                self.admin_home()
            elif(choice=='no' or choice=='n'):
                self.quantity()

        elif(ch==2):
            query="SELECT item_id,item_name,quantity FROM product"
            self.cursor.execute(query)
            lst=self.cursor.fetchall()   
            for item in lst:
                a,b,c=item
                print('+{} - {} - {}'.format(a,b,c))
            item_id=input("Enter the item ID:")
            q="SELECT item_name FROM product WHERE item_id=%s and item_id=%s"
            self.cursor.execute(q,(item_id,item_id))
            i=self.cursor.fetchone()
            prod_name=i[0]
            choice=input('sure this ({}) product [yes/no]? '.format(prod_name))
            if(choice=='yes' or choice=='y'):
                rq=input("Enter the number of quantity:")
                query="UPDATE product SET quantity=quantity-%s WHERE item_id=%s"
                self.cursor.execute(query,(rq,item_id))
                self.cnx.commit()
                print(rq+" item removed successfully")
                self.admin_home()
            elif(choice=='no' or choice=='n'):
                self.quantity()
        elif(ch==3):
            self.admin_home()
        else:
            print("Invalid entry")
            self.admin_home()


    def view_product(self):
        query="SELECT item_id,item_name,quantity FROM product"
        self.cursor.execute(query)
        lst=self.cursor.fetchall()   
        for item in lst:
            a,b,c=item
            print('>{} - {} - {}'.format(a,b,c))
        self.admin_home()

    def view_customer(self):
        query1="SELECT cus_id,name FROM customer"
        self.cursor.execute(query1)
        lst1=self.cursor.fetchall()
        for i in lst1:
            id,name=i
            print(">{} - {}".format(id,name))
        cus_id=input("Enter the customerID:")
        query2="SELECT name,phone_no,address FROM customer WHERE cus_id=%s and cus_id=%s"
        self.cursor.execute(query2,(cus_id,cus_id))
        lst2=self.cursor.fetchone()
        name,phone_no,address=lst2
        print("Name:",name)
        print("Phone Number:",phone_no)
        print("Address:",address)
        query3="SELECT item_id,quantity,delivery_date FROM buyed_product WHERE cus_id=%s and cus_id=%s"
        self.cursor.execute(query3,(cus_id,cus_id))
        lst3=self.cursor.fetchall()
        for i in lst3:
            item_id,quantity,delivery_date=i
            query4='SELECT item_name,price FROM product WHERE item_id=%s and item_id=%s'
            self.cursor.execute(query4,(item_id,item_id))
            lst4=self.cursor.fetchone()
            item_name,price=lst4
            print('Item Name:',item_name)
            print("quantity:",quantity)
            print("Total price:",quantity*price)
        



        self.admin_home()
        
        
    def admin_home(self):
        
        print("------------------------------")
        print("            ADMIN             ")
        print("------------------------------")
        print('''
         1.make changes in product
         2.make changes in quantity
         3.view the product
         4.view the customer
         5.logout

        ''' )
        choice=int(input("Enter your choice:"))
        if(choice==1):
            self.product()
            self.admin_home()
        elif(choice==2):
            self.quantity()
            self.admin_home()
        elif(choice==3):
            self.view_product()
            self.admin_home()
        elif(choice==4):
            self.view_customer()
            self.admin_home()
        elif(choice==5):
            pass
        else:
            print("Invalid entry")

    
    




import mysql.connector
from datetime import date,timedelta
cnx=mysql.connector.connect(user="root",database="online_shopping")
cursor=cnx.cursor(buffered=True)
while True:
    print("================================")
    who=input("  Admin or Customer:")
    print("================================")

    if(who=="admin" or who=="a"):
        ad=Admin(cursor,cnx)
        ad.signin()
         
    elif(who=="customer" or who=="c"):
        cus=Customer(cursor,cnx)
        sign=input("'signin' or 'sigup':")
        if(sign=="signin"):
            cus.signin()
        elif(sign=='signup'):
            cus.signup()
        else:
            print("Invalid data")
    else:
        print("Invalid data")
        