
USE instructai;

DROP TABLE IF EXISTS Tests;
DROP TABLE IF EXISTS Assessment;
DROP TABLE IF EXISTS LectureTopic;
DROP TABLE IF EXISTS Lecture;
DROP TABLE IF EXISTS Enrolled;
DROP TABLE IF EXISTS Teaches;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Section;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Department;


CREATE TABLE Department(
    deptName VARCHAR(90),
    PRIMARY KEY(deptName)

);

CREATE TABLE Student(
    studentID VARCHAR(120),
    studentFirstName VARCHAR(90),
    studentLastName VARCHAR(90),
    deptName VARCHAR(90),
    email VARCHAR(90) UNIQUE NOT NULL,
    PRIMARY KEY(studentID),
    FOREIGN KEY (deptName) REFERENCES Department(deptName)
);

CREATE TABLE Instructor(
    instructID VARCHAR(120),
    instructFirstName VARCHAR(90),
    instructLastName VARCHAR(90), 
    deptName VARCHAR(90),
    email VARCHAR(90) UNIQUE NOT NULL,
    PRIMARY KEY(instructID),
    FOREIGN KEY (deptName) REFERENCES Department(deptName)
);

CREATE TABLE Course(
    courseCode VARCHAR(90),
    courseName VARCHAR(90),
    PRIMARY KEY(courseCode)
);

CREATE TABLE Section(
    courseCode VARCHAR(90),
    secNum INT NOT NULL,
    secSemester VARCHAR(90) NOT NULL,
    secYear INT NOT NULL,
    PRIMARY KEY(courseCode, secNum, secSemester, secYear),
    FOREIGN KEY (courseCode) REFERENCES Course(courseCode)
);

CREATE TABLE Enrolled(
    studentID VARCHAR(120),
    courseCode VARCHAR(90),
    secNum INT,
    secSemester VARCHAR(90),
    secYear INT,
    PRIMARY KEY(studentID, courseCode, secNum, secSemester, secYear),
    FOREIGN KEY(studentID) REFERENCES Student(studentID),
    FOREIGN KEY(courseCode, secNum, secSemester, secYear) REFERENCES Section(courseCode, secNum, secSemester, secYear)
);

CREATE TABLE Teaches(
    instructID VARCHAR(120),
    courseCode VARCHAR(90),
    secNum INT,
    secSemester VARCHAR(90),
    secYear INT,
    PRIMARY KEY(instructID, courseCode, secNum, secSemester, secYear),
    FOREIGN KEY(instructID) REFERENCES Instructor(instructID),
    FOREIGN KEY(courseCode, secNum, secSemester, secYear) REFERENCES Section(courseCode, secNum, secSemester, secYear)
);

CREATE TABLE Lecture(
    courseCode VARCHAR(90),
    secNum INT,
    secSemester VARCHAR(90),
    secYear INT,
    lecNum INT,
    lecName VARCHAR(90),
    lecDate DATE,
    PRIMARY KEY(courseCode, secNum, secSemester, secYear, lecNum),
    FOREIGN KEY(courseCode, secNum, secSemester, secYear) REFERENCES Section(courseCode, secNum, secSemester, secYear)
);

CREATE TABLE LectureTopic(
    courseCode VARCHAR(90),
    secNum INT,
    secSemester VARCHAR(90),
    secYear INT,
    lecNum INT,
    topicName VARCHAR(90),
    PRIMARY KEY(courseCode, secNum, secSemester, secYear, lecNum, topicName),
    FOREIGN KEY(courseCode, secNum, secSemester, secYear, lecNum) REFERENCES Lecture(courseCode, secNum, secSemester, secYear, lecNum)
);

CREATE TABLE Assessment(
    courseCode VARCHAR(90),
    secNum INT,
    secSemester VARCHAR(90),
    secYear INT,
    assessmentName VARCHAR(90),
    PRIMARY KEY(courseCode, secNum, secSemester, secYear, assessmentName),
    FOREIGN KEY(courseCode, secNum, secSemester, secYear) REFERENCES Section(courseCode, secNum, secSemester, secYear)
);

CREATE TABLE Tests(
    studentID VARCHAR(120),
    courseCode VARCHAR(90),
    secNum INT,
    secSemester VARCHAR(90),
    secYear INT,
    assessmentName VARCHAR(90),
    grade DECIMAL(5,2),
    points INT,
    PRIMARY KEY (studentID, courseCode, secNum, secSemester, secYear, assessmentName),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (courseCode, secNum, secSemester, secYear, assessmentName) REFERENCES Assessment(courseCode, secNum, secSemester, secYear, assessmentName)

);


# inserting into Department Table

INSERT INTO Department(deptName) VALUES('ECE');
INSERT INTO Department(deptName) VALUES('Comp Sci.');
INSERT INTO Department(deptName) VALUES('Math');
INSERT INTO Department(deptName) VALUES('Health');
INSERT INTO Department(deptName) VALUES('Math Physics');

# insertiing into the Instructor table

INSERT INTO Instructor(instructID,instructFirstName,instructLastName,deptName, email) VALUES('bbed4a53-d988-472d-a5db-9a3c4519774e','Sam','McDonald','ECE', 'smd@example.com');
INSERT INTO Instructor(instructID,instructFirstName,instructLastName,deptName, email) VALUES('4bb0ef35-f9c1-4ec8-b156-e475f795eaee','Don','McDonald','Comp Sci.', 'dmd@example.com');


# inserting into the Student table
INSERT INTO Student(studentID,studentFirstName,studentLastName,deptName, email) VALUES('9d7b62eb-4b6e-41d9-838e-711bfd6e08a7','Jon','Bon','ECE', 'jb@example.com');
INSERT INTO Student(studentID,studentFirstName,studentLastName,deptName, email) VALUES('eebdbe6a-d6bf-440e-a564-2986b149c0a7','Gary','Styles','ECE', 'gs@example.com');

# inserting into the Course table
INSERT INTO Course(courseCode, courseName) VALUES('CS580', 'Intro to Machine Learning');

# inserting into the Section table
INSERT INTO Section(courseCode, secNum, secSemester, secYear) VALUES('CS580',1,'Spring',2023);

# inserting into Enrolled table
INSERT INTO Enrolled(studentID, courseCode, secNum, secSemester, secYear) VALUES('9d7b62eb-4b6e-41d9-838e-711bfd6e08a7','CS580',1,'Spring',2023);

# inserting into Teaches table
INSERT INTO Teaches(instructID, courseCode, secNum, secSemester, secYear) VALUES('bbed4a53-d988-472d-a5db-9a3c4519774e','CS580',1,'Spring',2023);

# inserting into Lecture table
INSERT INTO Lecture(courseCode, secNum, secSemester, secYear, lecNum, lecName, lecDate) VALUES('CS580',1,'Spring',2023,1,'Introduction','2023-10-01');

# inserting into LectureTopic table
INSERT INTO LectureTopic(courseCode, secNum, secSemester, secYear, lecNum, topicName) VALUES('CS580',1,'Spring',2023,1,'Introduction to Machine Learning');

# inserting into Assessment Table
INSERT INTO Assessment (courseCode, secNum, secSemester, secYear, assessmentName) VALUES ('CS580', 1, 'Spring', 2023, 'Midterm');

# inserting into Tests table
INSERT INTO Tests (studentID, courseCode, secNum, secSemester, secYear, assessmentName,grade,points) VALUES ('9d7b62eb-4b6e-41d9-838e-711bfd6e08a7','CS580', 1, 'Spring', 2023,'Midterm',95.3,10000);
