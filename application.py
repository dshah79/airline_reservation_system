#
import psycopg2
import re 
from datetime import datetime
import random
import string 
#

conn = psycopg2.connect(database = "*", user = "postgres", password = "*", host = "*", port = "5432")
cur = conn.cursor()
#
#

def home():
	userinput = ""
	print ("Please make selection From Following ")
	print ("Press 1: Login ")
	print ("Press 2: Register ")
	print ("Press 3: Flight Serach: ")
	userinput = raw_input ("Please make selection From Following: ")
	
	if (userinput == "2"):
		reg = registration()
		reg.collectInfo()
		reg.validation()
		reg.post()

	elif (userinput == "1"):
		
		email    	 	= raw_input ("Email: ")
		password		= raw_input ("Password: ")
		lo = Login(email,password)
		lo.valildate()
		lo.login()

		if (lo.ready):

			while True:
			
				print ("what you like to do ?")
				print ("Press 1: Modified")
				print ("Press 2: Flight Search")
				print ("Press 3: Book Flight")
				print ("Press 4: Review Booking")
				print ("Press 5: Cancel Booking")
				print ("Press 6: Log out")


				whattodo = raw_input ("Press Key to choice the option: ")
				whattodo.strip()
				book = Booking(email)

				if (whattodo == '1'):
					profile = Profile(email)
					print ("what you like to do ?")
					print ("Press 1: Delete CreditCard")
					print ("Press 2: Update address")
					updatePro = raw_input ("Press Key to choice the option: ")
					if (updatePro == '1'):
						profile.deleteCediteCard()

					elif (updatePro == '2'):
						profile.updateBillingAddress()



				elif (whattodo == '2'):
					book.filghtSearch()
			
				elif (whattodo == '3'):
					book.bookingID()

				elif (whattodo == '4'):
					book.reviewBooking()
				
				elif (whattodo == '5'):
					book.cancelBooking()

				else:
					print ("You are successfully Log out")
					break

			



	elif (userinput == "3"):
		pass

	conn.close()








class registration:
		def __init__(self):
			self.firstName  	= None
			self.lastName  		= None
			self.email      	= None
			self.streetNumber   = None
			self.street  		= None
			self.zipcode 		= None
			self.creditcard 	= None
			self.password		= None 
			self.CVV 			= None
			self.type			= None
			self.expirationDate = None
			self.ready 			= 0

		def validation(self):
			
			cur.execute("SELECT * FROM CUSTOMER WHERE email = '%s'" % (self.email))
			if (cur.fetchall()):
				print ("This email is already register please use other email \n")
				self.ready = 0


			if ((re.match("^[A-Za-z]*$", self.firstName)) == None):
				print ("You enter invaid name please enter vaild name. Please Only use alphabetical character")
				self.firstName = input ("FirstName")

			if ((re.match("^[A-Za-z]*$", self.lastName)) == None):
				print ("You enter invaid Last name please enter vaild name. Please Only use alphabetical character")
				self.lastName = input ("LastName")

			if ((re.match(r'\b[\w.-]+?@\w+?\.\w+?\b', self.email)) == None ):
				print ("You enter invaid Email !! please enter vaild email example of Vaild email first@company.com")
				self.email = input ("Email ")

			if ((re.match("^[0-9]*$", self.streetNumber)) == None):
				print ("You enter invaid streetNumber. Please use only number")
				self.streetNumber = input ("streetNumber")


				
		def collectInfo(self):

			self.firstName 		= raw_input ("FirstName: ")
			self.lastName 	 	= raw_input ("LastName: ")
			self.password		= raw_input ("Password: ")
			self.email    	 	= raw_input ("Email: ")
			self.streetNumber   = raw_input ("streetNumber: ")
			self.street  		= raw_input ("steet: ")
			self.zipcode 		= raw_input ("zipcode: ")
			self.creditcard 	= int(raw_input ("creditcard: "))
			self.CVV 			= int(raw_input ("CVV: "))
			self.type			= raw_input("Type: ")
			self.expirationDate = raw_input("Expiration Date: ")
			self.ready 			= 1


		def post(self):
			if (self.ready):
				cur = conn.cursor()
				self.expirationDate = datetime.strptime(str(self.expirationDate),'%m/%y')
				cur.execute("INSERT INTO CUSTOMER   VALUES (%s,%s,%s,%s,%s,%s)", (self.firstName,'H',self.lastName,self.email,'ORD',self.password))
				cur.execute("INSERT INTO ADDRESS    VALUES (%s,%s,%s)",(int(self.streetNumber), int(self.zipcode), self.street))
				cur.execute("INSERT INTO CREDITCARD VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(self.creditcard,self.CVV,self.type,self.expirationDate,self.streetNumber, self.zipcode, self.street,self.email))
				cur.execute("INSERT INTO LIVEAT 	VALUES (%s,%s,%s,%s)",(self.email, int(self.streetNumber), int(self.zipcode), self.street))
				print ("Registration Done")
				conn.commit()



class Login:
	def __init__ (self,email, password):
		self.email 	  = email 
		self.password =  password
		self.ready = 1

	def valildate (self):
		if ((re.match(r'\b[\w.-]+?@\w+?\.\w+?\b', self.email)) == None ):
				print ("You enter invaid Email !! please enter vaild email example of Vaild email first@company.com")
				self.email = raw_input ("Email ")

		cur.execute("SELECT * FROM CUSTOMER WHERE email = '%s'" % (self.email))
		if (cur.fetchall() == []):
			print ("This email is not register !!! Please register ")
			register = raw_input ("Would you like to register ? ")
			if (register == 'yes'):
				reg = registration()
				reg.collectInfo()
				reg.validation()
				reg.post()
			self.ready = 0


	def login(self):
		cur.execute("SELECT * FROM CUSTOMER WHERE email = '%s'" % (self.email))
		rows = cur.fetchall()
		if (self.ready):
			if (self.password == rows[0][5]):
				print ("Login successfully")
			else:
				print ("Sorry Username or Password is wrong ")
				self.ready = 0



	def resetPassword(self):
		newPassword = raw_input ("Please enter the valid password? ")

class Profile():
	def __init__ (self, email):
		self.email = email

	def deleteCediteCard (self):
		cur.execute("SELECT CreditCard FROM CREDITCARD WHERE email = '%s'" % (self.email))
		
		for i in cur.fetchall():
			print (i[0])

		delete_credit = raw_input ("Which creditcard would like to delete ")
		cur.execute("DELETE FROM CREDITCARD WHERE CreditCard = '%s'" % (delete_credit))

	def updateBillingAddress(self):
		cur.execute("SELECT CreditCard FROM CREDITCARD WHERE email = '%s'" % (self.email))
		
		for i in cur.fetchall():
			print (i[0])

		update_credit 	= raw_input ("Which creditcard would like to update shipping address?  ")
		streetNumber   	= raw_input ("streetNumber: ")
		street  		= raw_input ("steet: ")
		zipcode 		= raw_input ("zipcode: ")


		cur.execute("SELECT streetNumber, street, zipcode FROM ADDRESS WHERE streetNumber = '%s' and street = '%s' and zipcode = '%s'" %(streetNumber,street,zipcode))
		a = cur.fetchall()
		print (a)
		if (a == []):
			cur.execute("INSERT INTO ADDRESS VALUES (%s,%s,%s)",(int(streetNumber), int(zipcode), street))
			conn.commit()
			cur.execute("INSERT INTO LIVEAT  VALUES (%s,%s,%s,%s)",(self.email, int(streetNumber), int(zipcode), street))
			conn.commit()
			

		cur.execute("SELECT streetNumber, street, zipcode FROM LIVEAT WHERE email = '%s'" % (self.email))
		needToupdate = 0 
		for i in cur.fetchall():
			print (int(streetNumber),street.strip(),int(zipcode), int(i[0]),str(i[1]).strip(),int(i[2]))
			if (int(streetNumber),street.strip(),int(zipcode)) == (int(i[0]),str(i[1]).strip(),int(i[2])):
				print ("Hello")
				needToupdate = 1


		if (needToupdate == 0):
			cur.execute("INSERT INTO LIVEAT  VALUES (%s,%s,%s,%s)",(self.email, int(streetNumber), int(zipcode), street))
			conn.commit()
			

		cur.execute("UPDATE  creditCard SET streetNumber = %s , zipcode = %s , street = '%s' WHERE creditcard = %s" % (int(streetNumber), int(zipcode), street, update_credit) ) 
		conn.commit()



			
class Booking:
	def __init__(self,email):
		self.bookingId = None 
		self.email = email

	def filghtSearch(self):
		returnFilght = raw_input ("Do you like to find return flight too ")

		departure = raw_input("depature From: ")
		arrive    = raw_input("arrive From: ")
		classAir  = raw_input ("Class: ")
		cur = conn.cursor()

		print ("Flight from ",departure, "to", arrive)
		cur.execute("SELECT dateoffilght,airlinecode,flight_number,iata,arrives_fromiata,departuretime,arrivaltime,amount FROM FLIGHT NATURAL JOIN price WHERE iata = '%s' and arrives_fromiata = '%s' and class = '%s'" % (departure,arrive,classAir))
		for i in cur.fetchall():
			print (str(i[0]),i[1].strip(),i[2],i[3],i[4],str(i[5]),str(i[6]),i[7])

		if (returnFilght == 'yes'):
			print ("Flight from ",arrive, "to", departure)
			cur.execute("SELECT dateoffilght,airlinecode,flight_number,iata,arrives_fromiata,departuretime,arrivaltime,amount FROM FLIGHT NATURAL JOIN price WHERE iata = '%s' and arrives_fromiata = '%s' and class = '%s'" % (arrive,departure,classAir))
			for i in cur.fetchall():
				print (str(i[0]),i[1].strip(),i[2],i[3],i[4],str(i[5]),str(i[6]),i[7])



	def bookingID(self):
		email 		 = self.email.split("@") 
		bookingID_a  = email[0] + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

		numWayBooking = raw_input ("Do you like to book one way or two way flight ?")
		numWayBooking = 1 if (numWayBooking == 'one way') else 2

		for b in range(numWayBooking):
			print (b)
			flight 			= raw_input ("Please Enter Flight number ")
			classFlight 	= raw_input ("Please Enter Class you would like to book flight ")
			dateoffilght 	= raw_input ("Please enter the date ")
		
			flight 		 = flight.split(" ")
			dateoffilght = datetime.strptime(str(dateoffilght),'%m/%d/%Y')

			cur.execute("SELECT CreditCard FROM CREDITCARD WHERE email = '%s'" % (self.email))
			for i in cur.fetchall():
				print (i[0])


			if (b == 0):
				creditcardUSE = raw_input ("Which creditcard would like to use ? ")
				cur.execute("INSERT INTO BOOKING VALUES (%s,%s,%s)", (bookingID_a,self.email,creditcardUSE))
				conn.commit()
				
			cur.execute("INSERT INTO INCLUDES VALUES (%s,%s,%s,%s,%s)", (bookingID_a,classFlight,flight[1],flight[0],dateoffilght.date()))
			conn.commit()

	def cancelBooking (self):
		cur.execute("SELECT bookingid FROM BOOKING WHERE email = '%s'" % (self.email))
		for i in cur.fetchall():
			print (i[0])

		cancelID = raw_input ("Which Booking would like to cancel ")
		cur.execute("DELETE FROM INCLUDES WHERE bookingid = '%s'" % (cancelID))
		cur.execute("DELETE FROM BOOKING  WHERE bookingid = '%s'" % (cancelID))
		
		conn.commit()

	def reviewBooking (self):
		cur.execute("SELECT bookingid,airlinecode,flight_number,dateoffilght FROM BOOKING NATURAL JOIN INCLUDES WHERE email = '%s'" % (self.email))

		for i in cur.fetchall():
			print (i)

#
#	
#
home();
#
#
#


