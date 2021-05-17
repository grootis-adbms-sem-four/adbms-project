import streamlit as st #to create the web app and gui
import hashlib #to hash the passwords
from sqlconnection import create_connection #custom function to create connection
import mysql.connector #to connect python with mysql
from custom_functions import check_if_user_exists, valid_password, valid_phno
conn = create_connection() #create a connection using the custom python script we created 
cursor = conn.cursor() #creating a cursor of that connection to execute queries 
st.header("Welcome to the web app") #print welcome message 
option = st.selectbox("Chose an action", ["Register", "Login", "Change Password","Forgot Password","Deactivate account"]) #print a list of options we offer

if option == "Register": #if register is clicked 
    #inputting the details
    name = st.text_input("Enter your name")
    email = st.text_input('Enter your email address')
    age = st.number_input("Enter your age")
    gender = st.selectbox('Gender', options=['M','F', 'Other'])
    address = st.text_area("Enter your address", max_chars=200)
    phno = st.text_input("Enter your phone number along with the country code")
    username = st.text_input("Enter a username")
    password = st.text_input("Create a password", type="password")
    confirm_password = st.text_input("Re enter the password",type="password")
    submit_button = st.button("Submit")
    if submit_button:#if submit button is clicked 
        if ' ' in username:
            st.error('Spaces should not be present in username')
        else:
            if password == confirm_password: #if the password matches with the confirm password 
                if not valid_password(password): #if the password is invalid 
                    st.error('Invalid password as passwords should contain at least one upper case, one lower case, one digit and one special character and passwords cannot be blank') #show error message 
                elif not valid_phno(phno): #if the phone number is invalid 
                    st.error('Invalid phone number. Please check the phone number you have entered') #show error message 
                elif password == username:
                    st.error('Password cannot be same as the username')
                elif not '@' in email or not '.' in email: #if the email does not contain @ or . in it then show error
                    st.error('Enter valid email id')
                elif age<= 0.00 or age>120: #if the age is less than or equal to 0  or it is greater than 120 then show error
                    st.error('Enter a valid age')
                else: #if everything is valid 
                    encoded_password = hashlib.md5(password.encode()).hexdigest() #hash the password using md5 algo
                    query = f"INSERT INTO details_table VALUES ('{name}','{email}','{username}', {age},'{gender}', '{address}', '{phno}',curdate())" #insert in details_table
                    query_register = f"INSERT INTO login_table VALUES ('{username}', '{encoded_password}')" #insert in login_table
                    try: #trying to execute the below code 
                        cursor.execute(query) #execute query for inserting in details_table
                        conn.commit() #commit for the changes to reflect in the database
                        cursor.execute(query_register) #execute query for inserting in login_table
                        conn.commit() #commit for the changes to reflect in the database
                        st.success("You have registered now") #give a success message
                    except mysql.connector.IntegrityError as e: #checking if there is an integrity error (as username is primary key, its unique and not null)
                        st.error('This username is taken,try a different username') #give error msg that the username is taken
            else: #if the passwords entered do not match 
                st.error('The passwords you have entered do not match') #show error that passwords entered do not match
if option == 'Login': #if the user selects login
    username_login = st.text_input('Enter the username') #ask for usernamme
    password_login = st.text_input('Enter the password', type='password') #ask for password
    login_button = st.button('Login') #create login button 
    if login_button: #if login button is clicked
        if ' ' in username_login:
            st.error('Spaces should not be present in the username')
        elif not check_if_user_exists(username_login): #if the user does not exist
            st.error('This user does not exist') #show error that the user does not exist
        elif not valid_password(password_login): #if the password is not a valid password
            st.error('Invalid Password as passwords should contain at least one upper case, one lower case, one special character and one digit and passwords cannot be blank') #show error that the password is invalied
        else: #if the user exists and password is valid 
            query_check_pass = f"SELECT pass FROM login_table WHERE username='{username_login}'" #query to retrieve password from the database
            cursor.execute(query_check_pass) #execute the above query
            retrieved_pass = cursor.fetchall()[0][0] #fetch retrieved password
            if retrieved_pass == hashlib.md5(password_login.encode()).hexdigest(): #if the password entered matches with the password stored in db
                st.markdown('You have sucessfully logged in. Please check out out website [Group Website] (https://grootis-adbms-sem-four.github.io/group-website/)') #show success message
            else: #if the password does not match 
                st.error('The username or password does not match') #show error message
if option == 'Change Password': #if the user selects change password
    username_change = st.text_input('Enter the username') #ask for username 
    old_pass_change = st.text_input('Enter the old password', type='password') #ask for old password
    new_pass_change = st.text_input('Enter a new password', type='password') #ask for new password
    confirm_new_pass_change = st.text_input('Confirm the new password', type='password') #confirm new password
    change_button = st.button('Change Password') #create change password button
    if change_button: #if change button is clicked
        if ' ' in username_change:
            st.error('Sapces should not be present in username')
        elif not check_if_user_exists(username_change): #if the user does not exist
            st.error('The user does not exist') #display error message
        else: #if password is valid
            query_check_update = f"SELECT pass FROM login_table WHERE username='{username_change}'" #query to retrieve password from database
            cursor.execute(query_check_update) #executing the above query
            old_pass_retrieve = cursor.fetchall()[0][0] #retreiving the old password
            if hashlib.md5(old_pass_change.encode()).hexdigest() == old_pass_retrieve: #if the hash of the old password matches the retrieved hash
                if new_pass_change == confirm_new_pass_change: #if the new password matches the confirm new password
                    if not valid_password(new_pass_change): #if it is an invalid password
                        st.error('Invalid password as passwords should contain at least one upper case, one lower case, one digit and one special characters and passwords should not be blank') #display error message
                    elif hashlib.md5(new_pass_change.encode()).hexdigest() == old_pass_retrieve:
                        st.error('Old passsword can not be same as new password')
                    else: #if it is valid password
                        query_update_password = f"UPDATE login_table SET pass = '{hashlib.md5(new_pass_change.encode()).hexdigest()}' WHERE username = '{username_change}'" #query to update the password
                        cursor.execute(query_update_password) #execute the above query
                        conn.commit() #commit to database
                        st.success('Password Changed Successfully') #show success message
                else: #if the passwords entered do not match
                    st.error('The passwords you have entered do not match') #show error message
            else: #if the database password does not match with retreived password
                st.error('The username or password is incorrect') #show error message 
if option == 'Forgot Password': #if user clicks forgot password
    username_forgot = st.text_input('Enter the username') #ask for username
    phno_forgot = st.text_input('Enter the phone number') #ask for phone number for verification of user
    password_forgot = st.text_input('Enter the password',type='password') #ask for new password
    password_forgot_confirm = st.text_input('Confirm the new password', type='password') #confirm new password
    change_pass_forgot_button = st.button('Update password') #create change password button 
    if change_pass_forgot_button: #if change password button is clicked 
        if password_forgot == password_forgot_confirm: #if both the passwords entered match
            if ' ' in username_forgot:
                st.error('Spaces should not be present in the username')
            elif not check_if_user_exists(username_forgot): #if the user does not exist 
                st.error('The user does not exist') #show error message 
            elif not valid_phno(phno_forgot): #if the phone number is not valid 
                st.error('Invalid phone number, please check the phone number you have entered') #show error message 
            elif not valid_password(password_forgot): #if the password entered is invalid 
                st.error('Invalid password as passwords should contain at least one upper case, one lower case, one special character and one digit and passwords should not be blank') #show error message 
            else: #if everything is fine 
                query_forgot_old_pass_retrieve = f"SELECT pass FROM login_table WHERE username = '{username_forgot}'"
                cursor.execute(query_forgot_old_pass_retrieve)
                old_pass_forgot = cursor.fetchall()[0][0]
                if hashlib.md5(password_forgot.encode()).hexdigest() == old_pass_forgot:
                    st.error('Old password cannot be same as new password')
                else:
                    query_retrieve_phno = f"SELECT phno FROM details_table WHERE username = '{username_forgot}'" #query to retrieve phone number
                    cursor.execute(query_retrieve_phno) #execute the above query 
                    phno_forgot_retrieve = cursor.fetchall()[0][0] #fetch the phone number 
                    if phno_forgot == phno_forgot_retrieve: #if the phone numbers match
                        query_update_forgot = f"UPDATE login_table SET pass = '{hashlib.md5(password_forgot.encode()).hexdigest()}' WHERE username = '{username_forgot}'"  #query to update the password
                        cursor.execute(query_update_forgot) #execute the above query
                        conn.commit() #commit to the database
                        st.success('Password changed successfully') #show success message 
                    else: #if the phone numbers do not match 
                        st.error('The phone number does not match') #show error message 
        else: #if the passwords do not match 
            st.error('The passwords entered do not match') #show error message 
if option == 'Deactivate account': #if deactivate account is clicked 
    username_delete = st.text_input('Enter your username') #ask for username 
    pass_delete = st.text_input('Enter password', type='password') #ask for password
    confirm_pass_delete = st.text_input('Enter password to confirm action', type='password') #confirm password to delete
    delete_button = st.button('Deactivate account')  #create delete button 
    if delete_button: #if delete button is clicked
        if pass_delete == confirm_pass_delete: #if the passwords match 
            if ' ' in username_delete:
                st.error('Spaces should not be present in username')
            elif not check_if_user_exists(username_delete): #if the user does not exist  
                st.error('The user does not exist') ##show error message 
            elif not valid_password(pass_delete): #if the password is invalid 
                st.error('Invalid password as passwords should contain at least one upper case, one lower case, one special character and one digit and passwords should not contain spaces') #show error message 
            else: #if everything is fine 
                query_retrive_pass_delete = f"SELECT pass FROM login_table WHERE username = '{username_delete}'" #query to retrieve password 
                cursor.execute(query_retrive_pass_delete) #execute the above query 
                retrieved_pass_delete = cursor.fetchall()[0][0] #fetch retrieved password 
                if hashlib.md5(pass_delete.encode()).hexdigest() == retrieved_pass_delete: #if the hash of the entered password matches with the retrieved hash
                    query_delete_login_table = f"DELETE FROM login_table WHERE username = '{username_delete}'" #delete query for login_table 
                    query_delete_details_table = f"DELETE FROM details_table WHERE username = '{username_delete}'" #delete query for details_table
                    cursor.execute(query_delete_login_table) #execute delete query for login table 
                    conn.commit() #commit to the database 
                    cursor.execute(query_delete_details_table) #execute delete query for details_table 
                    conn.commit() #commit to the database 
                    st.success('Account deleted successfully') #show success message 
                else: #if the password does not match
                    st.error('The username or password does not match') #show error message 
        else: #if the passwords entered do not match
            st.error('The passwords entered do not match') #show error message 
