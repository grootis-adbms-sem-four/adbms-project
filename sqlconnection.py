import mysql.connector #to create connection to mysql database 
def create_connection(filepath="sqlcredentials.txt"): #create a function and pass the filepath to it as argument
    credential = [] #create empty credential list
    value = [] #create empty value list
    with open(filepath, 'r') as f: #open file at filepath in read mode 
        lines = f.readlines() #read all the lines in the file and store them in lines 
        for line in lines: #iterate through lines 
            credential.append(line.split('=')[0].strip()) #append credentaial name in credential
            value.append(line.split('=')[1].strip()) #append credential value in value
    credentials_dict = dict(zip(credential,value)) #create a dictionary of credential name and values
    conn = mysql.connector.connect(host=credentials_dict['host'], #establish the connnection with appropriate credentials
                                   port=credentials_dict['port'],
                                   user=credentials_dict['user'],
                                   password=credentials_dict['password'],
                                   auth_plugin=credentials_dict['auth_plugin'],
                                   database=credentials_dict['database'])
    return conn #return the connection 
