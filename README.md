# ADFPythonDay6

•	Create a python code that will get the user details as input, store them in the table and perform the eligibility and give response in JSON if the user is eligible or not eligible
1.	Following are the input in user details  :
	First Name 
	Middle Name - Optional
	Last Name
	DOB – YYYY-MM-DD
	Gender
	Nationality
	Current City
	State
	Pin-code
	Qualification 
	Salary
	PAN Number
2.	Create Two Mysql table :
	Request_Info :
•	Should contain above set of fields with appropriate data type
•	Should have id field as auto increment. 
•	Should have Request received datetime field.
	Response_Info
•	Should have id field as auto increment. 
•	Should have request_id as a foreign key reference to the Request_Info id column.
•	Should have response field to store the response generated for the request.
3.	Eligibility Criteria :
	Age should be greater than 21 Yrs for Male as of current day.
	Age should be greater than 18 Yrs for Female as of current day.
	No Request should have received in last 5 days from the same user (use PAN as the identifier).
	Nationality should be “Indian” or “American”.
	State should be only from Andhra Pradesh, Arunachal Pradesh, Assam, Bihar,  Chhattisgarh,  Karnataka,  Madhya Pradesh,  Odisha,  Tamil Nadu,  Telangana, West Bengal.
	Salary should not be less than 10,000.
	Salary Should not be greater than 90,000.
4.	Response should be formed as a JSON.
	Sample success response :
•	{‘Request_id’: 1, ‘Response’:’Success’}
	Sample Validation Failure response :
•	Here assuming the DOB input was not in expected format, below will be the response.
•	{‘Response’:’Validation Failure’, ‘Reason’:’Invalid Input for DOB’} 
	Sample Eligibility Failure  response :
•	Response example1: Here assuming the DOB input was ‘2015-06-01’, below will be the response.
•	                {‘Request_id’: 2, ‘Response’:Failed’, ’Reason’:’Age is less than expected.’}
•	Response example2: Here assuming other request received with same pan number within last 5 days, below will be the response.
•	                {‘Request_id’: 3, ‘Response’:Failed’, ’Reason’:’Recently request received in last 5 days.’
