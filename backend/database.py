import psycopg2 as dbapi2

class DatabaseManager():
	'''
	A class used to manage the database
	'''
	def __init__(self):
		#Change user and database name to local database
		self.db = dbapi2.connect (database = "professit", user= "yawsers")
		self.cur = self.db.cursor()
	def add_user(self, usid, name, email, passwordhash, isstudent):
		'''
		creates a new user for the database
		'''
		try:
			self.cur.execute("INSERT INTO users VALUES({}, '{}', '{}', '{}', {})".format(usid, name, email, passwordhash, isstudent))
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			self.db.rollback()
			return False
	def add_student(self, usid, classid):
		'''
		Adds a student to a class in the database
		'''
		#verify user is a student
		try:
			assert self.isStudent(usid)
			self.cur.execute("INSERT INTO member VALUES({}, {})".format(usid, classid))
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			self.db.rollback()
			return False
		#add student in the database
	def save_class(self, classid, classname, instructorid):
		'''
		creates a class
		'''
		
		#attempt to create the class
		try:
			#verify if user is an instructor
			assert not self.isStudent(instructorid)
			self.cur.execute("INSERT INTO class VALUES({}, '{}')".format(classid, classname))
			self.cur.execute("INSERT INTO teaches VALUES({}, {})".format(classid, instructorid))
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			self.db.rollback()
			return False
	def verify_user_login(self,usid, passwordhash):
		'''
		returns true if the user and passwordhash are in the database
		'''
		rows = self.cur.execute("SELECT 1 FROM users WHERE userid = {} and passwordhash = '{}'".format(usid, passwordhash))
		return len(self.cur.fetchall()) == 1
	def isStudent(self,usid):
		rows = self.cur.execute("SELECT 1 FROM users WHERE userid = {} and isstudent = {}".format(usid, True))
		return len(self.cur.fetchall()) == 1    	
	def add_lecture(self,instructorid, lectureid, classid, starttime, endtime, lectureurl,day):
		try:
			#Check is the instructor is an instructor of the current class
			self.cur.execute("SELECT 1 FROM teaches WHERE instructorid = {} and classid = {}".format(instructorid, classid))
			assert len(self.cur.fetchall()) == 1
			self.cur.execute("INSERT INTO lecture VALUES({}, {}, '{}', '{}', '{}', '{}')".format(lectureid, classid, starttime, endtime, lectureurl,day))
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			self.db.rollback()
			return False

	def get_all_lectures(self,usid, classid):
		'''
		returns all the lectures of a given class
		'''
		try:
			#make sure student or instructor is a part of the class
			self.cur.execute("SELECT 1 FROM member m , teaches t WHERE (m.studentid = {} and m.classid = {}) or  (t.classid = {} and t.instructorid ={})".format(usid, classid, classid, usid))
			assert len(self.cur.fetchall()) >= 1
			self.cur.execute("SELECT * FROM lecture WHERE classid = {}".format(classid))
			rows = self.cur.fetchall()
			return rows
		except Exception as e:
			return False
	def get_all_classes(self, studentid):
		'''
		returns all the classes of a student
		'''
		self.cur.execute("SELECT c.classid, c.name FROM class c, member m WHERE m.studentid = {} and c.classid = m.classid".format(studentid))
		return self.cur.fetchall()
	def get_all_teaching(self, instructorid):
		'''
		returns all the classes an instructor teaches
		'''
		self.cur.execute("SELECT c.classid, c.name FROM class c, teaches t WHERE t.instructorid = {} and t.classid = c.classid".format(instructorid))
		return self.cur.fetchall()
	
	def generate_new_classid(self):
		'''
		returns a classid that is not already in the database TODO: could make random id instead of incremental
		'''
		self.cur.execute("SELECT max(classid) FROM class;")
		rows = self.cur.fetchall()
		if rows[0][0] != None:
			return rows[0][0] + 1
		else:
			return 1

	def generate_new_usid(self):
		self.cur.execute("SELECT max(userid) FROM users")
		rows = self.cur.fetchall()
		if rows[0][0] != None :
			return rows[0][0] + 1
		else:
			return 1
	def generate_new_lectureid(self, classid):
		self.cur.execute("SELECT max(lectureid) FROM lecture WHERE classid = {}".format(classid))
		rows = self.cur.fetchall()
		if rows[0][0] != None:
			return rows[0][0] + 1
		else:
			return 1

	def get_instructorid(self, email):
		'''
		returns the instructor id coresponding to the email, returns false if it can't be found
		'''
		try:
			self.cur.execute("SELECT userid FROM users WHERE isStudent = false and email = '{}'".format(email))
			rows = self.cur.fetchall()
			print(rows)
			return rows[0][0]
		except Exception as e:
			print(e)
			return False

if __name__ == "__main__":
	db = DatabaseManager()
	#add students as users
	usid = db.generate_new_usid()
	db.add_user(usid, 'SISMAN', 'SISMAN@rpi.edu', 'password', True)
	usid = db.generate_new_usid()
	db.add_user(usid, 'yawsers', 'yawsers@rpi.edu', 'password', True)
	usid = db.generate_new_usid()
	db.add_user(usid, 'shirley', 'shirley@rpi.edu', 'password', True)
	
	#add instructors as users
	usid = db.generate_new_usid()
	db.add_user(usid, 'Goldschmidt', 'Goldschmidt@rpi.edu', 'password', False)
	usid = db.generate_new_usid()
	db.add_user(usid, 'Kuzmin', 'Kuzmin@rpi.edu', 'password', False)
	usid = db.generate_new_usid()
	db.add_user(usid, 'Hubel', 'Hubel@rpi.edu', 'password', False)	
	

	#login
	print('Login')
	print(db.verify_user_login(1, 'password'))
	print(db.verify_user_login(2,'password'))
	print(db.verify_user_login(3, 'notpassword'))


	#create a class
	classid = db.generate_new_classid()
	instructorid = db.get_instructorid('Goldschmidt@rpi.edu')
	db.save_class(classid, 'SD and D',instructorid)
	
	classid = db.generate_new_classid()
	instructorid = db.get_instructorid('Kuzmin@rpi.edu')
	db.save_class(classid, 'Identity and Equality',instructorid)
	
	classid = db.generate_new_classid()
	instructorid = db.get_instructorid('Hubel@rpi.edu')
	db.save_class(classid, 'Gen Psych',instructorid)

	#add students to a class
	db.add_student(1,1)
	db.add_student(1,2)
	db.add_student(1,3)

	db.add_student(2,2)
	db.add_student(2,3)




	#add lecture
	classid = 1
	lectureid = db.generate_new_lectureid(classid)
	db.add_lecture(4, lectureid, classid, '03:00:00', '05:00:00', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ','2001-10-05')

	lectureid = db.generate_new_lectureid(classid)
	db.add_lecture(4, lectureid, classid, '03:00:00', '05:00:00', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ','2020-10-05')

	lectureid = db.generate_new_lectureid(classid)
	db.add_lecture(4, lectureid, classid, '03:00:00', '05:00:00', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ','2001-10-20')
	#add_lecture(instructorid, lectureid, classid, starttime, endtime, lectureurl,day)



	#get all lectures of a class
	print('')
	print(db.get_all_lectures(4,1))
	#no lectures
	print(db.get_all_lectures(5,1))

	#student
	print(db.get_all_lectures(1,1))


	#get all classes of a student
	print(db.get_all_classes(1))
	print(db.get_all_classes(2))
	print(db.get_all_classes(3))


	#get all classes of an instructor
	print('')
	print(db.get_all_teaching(4))
	print(db.get_all_teaching(5))
	print(db.get_all_teaching(6))



	#print(db.isStudent(2))
	#print(db.verify_user_login(2, 'passwssrd'))
	#print(db.save_class(1, "Psoft", 3))
	#print(db.add)
	#db.add_user(3, 'Carson', 'bigboy@gmail.com', 'password', False)
