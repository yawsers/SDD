from flaskapp import app
import unittest

'''
Testing module for the flask methods
'''

class TestIntegrations(unittest.TestCase):
	def set_up(self):
		'''
		sets up the flask app for testing
		'''
		self.app = app.test_client()
		#empty the database before starting the tests
		#self.app.get('/reset_database')
	def test_adding_user(self):
		'''
		tests the functionality of the add_user flask method
		add student method takes as arguments name, email, password and isstudent(boolean) all as a Json. Returns status of the result (True or False if the user was 
		added)
		'''
		self.set_up()

		#Sucessfully adding students 
		status = self.app.post('/add_user', json = {"name": "Obama", "email": "obama@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': True})

		status = self.app.post('/add_user', json = {"name": "Bob", "email": "bob@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': True})

		status = self.app.post('/add_user', json = {"name": "Bill", "email": "bill@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': True})

		status = self.app.post('/add_user', json = {"name": "Mario", "email": "mario@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': True})

		#Unsucessfully adding a student(Email exists in the database already for another student)
		status = self.app.post('/add_user', json = {"name": "Obamas Brother", "email": "obama@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': False})

		status = self.app.post('/add_user', json = {"name": "Bobs cousin", "email": "bob@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': False})

		status = self.app.post('/add_user', json = {"name": "Bills Mom", "email": "bill@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': False})

		status = self.app.post('/add_user', json = {"name": "Marios Dad", "email": "mario@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': False})

		#Sucessfully adding Instructors
		status = self.app.post('/add_user', json = {"name": "Goldschmidt", "email": "Goldschmidt@gmail.com", "password": "password" , "isstudent": "false"})
		self.assertEqual(status.get_json(), {'status': True})

		status = self.app.post('/add_user', json = {"name": "Kuzmin", "email": "Kuzmin@gmail.com", "password": "password2" , "isstudent": "false"})
		self.assertEqual(status.get_json(), {'status': True})

		status = self.app.post('/add_user', json = {"name": "Turner", "email": "Turner@gmail.com", "password": "password3" , "isstudent": "false"})
		self.assertEqual(status.get_json(), {'status': True})

		#Unsuccessfully adding an instructor (Email exists in the database already for another instructor)
		status = self.app.post('/add_user', json = {"name": "NotGoldschmidt", "email": "Goldschmidt@gmail.com", "password": "password" , "isstudent": "false"})
		self.assertEqual(status.get_json(), {'status': False})

		#Unsuccessfully adding a Student using instructor email that already exists in the database
		status = self.app.post('/add_user', json = {"name": "Student Goldschmidt", "email": "Goldschmidt@gmail.com", "password": "password" , "isstudent": "true"})
		self.assertEqual(status.get_json(), {'status': False})

		#Unsuccessfully adding a Instructor using student email that already exists in the database
		status = self.app.post('/add_user', json = {"name": "Instructor Obama", "email": "obama@gmail.com", "password": "password" , "isstudent": "false"})
		self.assertEqual(status.get_json(), {'status': False})

		#self.assertTrue(True)

	def test_verifying_user(self):
		'''
		tests the functionality of the verify_user flask method
		verify_user method takes as arguments email, and password all as a Json. Returns status of the result (True or False if the user was verified)
		'''
		self.set_up()

		#sucessful student logins
		status = self.app.post('/verify_user_login', json = {"email":"obama@gmail.com", "password":"password"} )
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/verify_user_login', json = {"email":"bob@gmail.com", "password":"password"} )
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/verify_user_login', json = {"email":"bill@gmail.com", "password":"password"} )
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/verify_user_login', json = {"email":"mario@gmail.com", "password":"password"} )
		self.assertTrue(status.get_json(), {"status":True})

		#sucessful instructor login
		status = self.app.post('/verify_user_login', json = {"email":"Goldschmidt@gmail.com", "password":"password"} )
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/verify_user_login', json = {"email":"Kuzmin@gmail.com", "password":"password2"} )
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/verify_user_login', json = {"email":"Turner@gmail.com", "password":"password3"} )
		self.assertTrue(status.get_json(), {"status":True})

		#unsucessful student login(wrong password)
		status = self.app.post('/verify_user_login', json = {"email":"obama@gmail.com", "password":"wrongpassword"} )
		self.assertTrue(status.get_json(), {"status":False})

		#unsucessful student login (email not in database)
		status = self.app.post('/verify_user_login', json = {"email":"fakeEmail@gmail.com", "password":"password"} )
		self.assertTrue(status.get_json(), {"status":False})

		#unsucessful instructor login(wrong password)
		status = self.app.post('/verify_user_login', json = {"email":"Goldschmidt@gmail.com", "password":"wrongpassword"} )
		self.assertTrue(status.get_json(), {"status":False})





	def test_creating_class(self):
		'''
		tests the functionality of the save_class flask method
		save_class method takes as arguments classname and instructorid all as a Json. Returns status of the result (True or False if the class was created)
		'''
		self.set_up()
		# 1, 2, 3, 4 are student user ids
		# 5, 6, 7 are instructor ids


		#instructor sucessfully creates class
		status = self.app.post('/save_class', json = {"classname": "SDD", "instructorid" : "5"})
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/save_class', json = {"classname": "PSoft", "instructorid" : "6"})
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/save_class', json = {"classname": "RCOS", "instructorid" : "7"})
		self.assertTrue(status.get_json(), {"status":True})

		#instructor creates two classes with the same name
		status = self.app.post('/save_class', json = {"classname": "SDD", "instructorid" : "5"})
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/save_class', json = {"classname": "PSoft", "instructorid" : "6"})
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/save_class', json = {"classname": "RCOS", "instructorid" : "7"})
		self.assertTrue(status.get_json(), {"status":True})

		#different instructor creates a class with the same name as another instructor
		status = self.app.post('/save_class', json = {"classname": "SDD", "instructorid" : "6"})
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/save_class', json = {"classname": "PSoft", "instructorid" : "7"})
		self.assertTrue(status.get_json(), {"status":True})
		status = self.app.post('/save_class', json = {"classname": "RCOS", "instructorid" : "5"})
		self.assertTrue(status.get_json(), {"status":True})

		#student is unsuccessfully able to create the class(Students can't create classes)
		status = self.app.post('/save_class', json = {"classname": "newClass", "instructorid" : "1"})
		self.assertTrue(status.get_json(), {"status":False})
		status = self.app.post('/save_class', json = {"classname": "newClass", "instructorid" : "2"})
		self.assertTrue(status.get_json(), {"status":False})
		status = self.app.post('/save_class', json = {"classname": "newClass", "instructorid" : "3"})
		self.assertTrue(status.get_json(), {"status":False})
		status = self.app.post('/save_class', json = {"classname": "newClass", "instructorid" : "4"})
		self.assertTrue(status.get_json(), {"status":False})



if __name__ == "__main__":
	#run the tests
	unittest.main()
