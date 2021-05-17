from sqlconnection import create_connection #importing the function to create a connection 
conn =  create_connection() #creating a connection 
cursor = conn.cursor() #creating a cursor of that connection 

def check_if_user_exists(username): #function to check if a user exists
    query_check = f"SELECT * FROM login_table WHERE username = '{username}'" #query to retrieve the details of users with that username
    cursor.execute(query_check) #execute the query 
    result = cursor.fetchall() #fetch the results 
    if len(result) != 0: #if the result does not return 0 rows
        return True #return True
    else: #if the result returns 0 rows
        return False #return False

def valid_password(password):
    #defining a list of special characters
    special_char = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';',
     '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    l, u, p, d = 0, 0, 0, 0
    if (len(password) >= 8):
        for i in password:
            # counting lowercase alphabets
            if (i.islower()):
                l+=1			
            # counting uppercase alphabets
            if (i.isupper()):
                u+=1			
            # counting digits
            if (i.isdigit()):
                d+=1			
            # counting the mentioned special characters
            if i in special_char:
                p+=1		
    if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password)):
        #checking if l,u,p,d are all greater than or equal to 1 and there are no spaces 
        #as spaces would increase the length of the password and spaces wont be counted 
        #and l+p+u+d not equal to len(password)
        return True
    else:
        return False

def valid_phno(phno):
    if len(phno.split())>1: #if the phone number contains spaces
        if not phno.split()[1].strip().isdigit(): #if the second part contains some non digit characters
            return False #return False
        elif '+' in phno and (len(phno.split()[1].strip()) == 10 and phno.split()[1].strip().isdigit()): #if the phone number has + in it and the second part is 10 digits long and it contains all digits
            return True #return True 
        elif '+' not in phno and (len(phno.split()[1].strip()) == 8 and phno.split()[1].strip().isdigit()): #if the phno does not have + in it and the second part is 8 digits long and it contains all digits
            return True #return True
        else: #if none of the above conditions are satisfied 
            return False #return False
    else: #if the phone number does not contain spaces
        if not phno.strip().isdigit(): # if the phone number contains non digit characters
            return False #return False
        elif phno.startswith('0') and len(phno)==11: #if the phone number starts with 0 and the phone number is 11 digits long (including 0)
            return True #return True
        elif len(phno) == 10: #if the phone number doesnt start with 0 and is 10 digits long
            return True #return True 
        else: #if none of the above conditions are satisdied
            return False #return False