drop table users CASCADE;
drop table class CASCADE;
drop table teaches CASCADE;
drop table member CASCADE;
drop table lecture CASCADE;
drop table muted CASCADE;


create table users (
	userid int primary key
	, name text
	, email text
	, passwordHash text
	, isStudent boolean
	, UNIQUE(email)
);

create table class (
	classid int primary key
	,name text
);

create table teaches (
	classid int
	, instructorid int
	, primary key (classid, instructorid)
	, foreign key (classid) references class(classid) ON DELETE CASCADE ON UPDATE CASCADE
	, foreign key(instructorid) references users(userid) ON DELETE CASCADE ON UPDATE CASCADE
);

create table member (
	studentid int
	,classid int
	, primary key (studentid, classid)
	, foreign key (classid) references class(classid) ON DELETE CASCADE ON UPDATE CASCADE
	, foreign key(studentid) references users(userid) ON DELETE CASCADE ON UPDATE CASCADE
);

create table lecture (
	lectureid int primary key
	, classid int
	, starttime time
	, endtime time
	, lectureurl text
	, day date
	, foreign key (classid) references class(classid) ON DELETE CASCADE ON UPDATE CASCADE
);

create table muted (
	studentid int
	, lectureid int
	, primary key (studentid, lectureid)
	, foreign key (studentid) references users(userid) ON DELETE CASCADE ON UPDATE CASCADE
	, foreign key (lectureid) references lecture(lectureid) ON DELETE CASCADE ON UPDATE CASCADE
);
