from datetime import datetime
import json
import mysql.connector
from datetime import date
import logging
logging.basicConfig(filename="log.txt", filemode='a+',
                        format='%(asctime)s %(levelname)s-%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
class UserDataInput:
    '''userdata getting initialized in the constructor'''
    def __init__(self,first_name,last_name,DOB,gender,nationality,current_city,state,pin_code,qualification,salary,pan_number):
        self.first_name = first_name
        self.last_name=last_name
        self.DOB=DOB
        self.gender=gender
        self.nationality=nationality
        self.current_city=current_city
        self.state=state
        self.pin_code=pin_code
        self.qualification=qualification
        self.salary=salary
        self.pan_number=pan_number
        self.reqid=None

    def Connection(self):
        """ creating connection """
        try:
            mydb = mysql.connector.connect(host='localhost',
                  username ='root',
                  password= 'Yeshwanth@28',
                   database='adf')
            return mydb
        except Exception as error:
            print(error)
    def createTable(self):
        """request_info and response_info tables creation"""
        try:
            con=self.Connection()
            cursor=con.cursor()
            cursor.execute("create table if not exists Request_info( ID int AUTO_INCREMENT primary key, First_Name varchar(50),\
                Last_Name varchar(50), DOB date, Gender char(30), Nationality char(30), Current_City char(30),\
                State char(30), Pincode int(10), Qualification varchar(50), Salary int(10),\
                PAN_Number varchar(20) unique, request_receive_time datetime)")
            cursor.execute("create table if not exists Response_info( EID int AUTO_INCREMENT primary key,\
                response varchar(100), id int, reason varchar(200), foreign key(id) references request_info(id))")
            con.commit()
            logging.info("tables created successfully")
        except:
            logging.error("creation table error")
        finally:
            con.close()

    def insertDataInRequestTable(self):
        """Inserting data into Request_info table"""
        try:
            con = self.Connection()
            cursor = con.cursor(prepared=True)
            cursor.execute("insert into Request_info values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                           (None, self.first_name, self.last_name, self.DOB, self.gender,\
                self.nationality, self.current_city, self.state, self.pin_code, self.qualification, self.salary, self.pan_number, datetime.now()))
            con.commit()
        except:
            con.rollback()
    def calculateAge(self):
        """ funtion to return age in number of years """
        p, q, r = map(int, self.DOB.split('-'))
        n = date(p, q, r)
        days_in_year = 365.2425
        age = int((date.today() - n).days / days_in_year)
        return age

    def validatingaAgeAndGender(self):
        """checking eligibility of age in years based on gender"""
        age=self.calculateAge()
        print(age)
        if self.gender == 'Male':
            if age > 21:
                return True
        if self.gender == 'Female':
            if age > 18:
                return True
        return False

    def validatingNation(self):
        """checking eligibility of nationality """
        if self.nationality in ['Indian', 'American']:
            return True
        return False

    def validatingState(self):
        """checking eligibility of state based on given data"""
        if self.state in ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam, Bihar', \
            'Chhattisgarh', 'Karnataka', 'Madhya Pradesh', 'Odisha', 'Tamil Nadu', 'Telangana', 'West Bengal']:
            return True
        return False

    def validatingSalary(self):
        """Checking eligibilty of salary for given range"""
        if self.salary>10000 and self.salary < 90000:
            return True
        return False
    def validatingRequest(self):
      """ checking the eligibilty of same pan number request within 5 days"""
        con = self.Connection()
        cursor = con.cursor()
        cursor.execute("select request_receive_time from request_info where PAN_Number = %s", (self.pan_number,))
        data = cursor.fetchall()
        self.request_receive_time = data[0][0]
        today=datetime.date.today()
        flag=10
        if len(data)>1:
            for date in data:
                x= today.year - date[0].year -((today.month, date[0].day) < (date[0].month,date[0].day))
                if x <flag:
                    flag=x
            return flag>5
        return True
                    
    def insertDataInResponseTable(self):
        try:
            con = self.Connection()
            cursor = con.cursor()
            cursor.execute("select id from request_info where PAN_Number = %s",(self.pan_number,))
            data=cursor.fetchall()
            self.reqid = data[0][0]
            response,reason='',''
            if not self.validatingaAgeAndGender():
                reason+='Age less than expected '
            if not self.validatingNation():
                reason+="Invalid nation "
            if not self.validatingState():
                reason+="Inavalid state "
            if not self.validatingSalary():
                reason+="salary not in given range "
            if not self.ValidatingRequest():
                reason+="request received on same pan should not be less than 5 days"
            if reason == '':
                response+="success"
            else:
                response+="failure"
            cursor.execute("insert into response_info values(%s,%s,%s,%s)",\
                (None, response, self.reqid, reason))
            con.commit()
            js = {"Request_id": self.reqid, "response":response, "reason": reason}
            logging.info(json.dumps(js))
        except Exception as error:
            logging.error(error)
            con.rollback()
        finally:
            con.close()

if __name__ == "__main__":
    '''inputs given by users'''
    first_name = input("Firstname:")
    last_name = input("Lastname:")
    DOB = input("dob(yyyy-mm-dd):")
    gender = input("gender:")
    nationality = input("nationality:")
    current_city = input("city:")
    state = input("state:")
    pin_code = int(input("pincode:"))
    qualification = input("qualification:")
    salary = int(input("salary:"))
    pan_number = input("PAN:")
    obj=UserDataInput(first_name,last_name,DOB,gender,nationality,current_city,state,pin_code,qualification,salary,pan_number)
    obj.createTable()
    obj.insertDataInRequestTable()
    obj.insertDataInResponseTable()










