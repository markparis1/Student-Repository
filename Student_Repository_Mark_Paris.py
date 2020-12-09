from typing import Dict, Tuple, List, Iterator, IO
from prettytable import PrettyTable
from os import path
import sqlite3
from flask import Flask

"""read a file and split it by the provided separator"""
def file_reader(path: str, fields: int, sep = ',', header = False) -> Iterator[List[str]]:

    #try to open file
    try:

        fp: IO = open(path, 'r')

    except FileNotFoundError:

        print(f"Unable to open {path}")

    else:
        with fp:
            i: int = 0
            #loop through files lines
            for line in fp:
    
                i += 1
                line_split: [str] = line.strip('\n').split(sep)
                
                if len(line_split) != fields:
                    raise ValueError(f"{path} has {len(line_split)} fields on line {i} but expected {fields}")
                
                if header == True and i == 1:
                    pass
                else:
                    yield line_split


"""Object to represent a student"""
class Student:

    """constructor provides unique identifier, cwid, and the students name, major, and courses with the grade in the course"""
    def __init__(self, cwid: str, name: str, major: str, course_grades: Dict[str,str]):
        
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grades = course_grades

    """adds a new course the student is taking"""
    def add_course(self, course_name: str, grade: str):

        self.course_grades[course_name] = grade

    """returns a tuple of instance data"""
    def get_data(self) -> (int, str, str, Dict[str,str]):
        
        return (self.cwid, self.name, self.major, self.course_grades)

    """takes a lettewr grade, converts it top a gpa value and returns it"""    
    def __convert_letter_to_gpa(self, letter_grade: str) -> float:
        
        grades: Dict[str, float] = {
            'A': 4.0,
            'A-': 3.75,
            'B+': 3.25,
            'B': 3.0,
            'B-': 2.75,
            'C+': 2.25,
            'C': 2.0,
            'C-': 0,
            'D+': 0,
            'D': 0,
            'D-': 0,
            'F': 0
        }

        return grades.get(letter_grade, "Invalid Grade")

        

    """returns students gpa"""
    def calculate_gpa(self) -> float:

        sum: float = 0.0
        for key in self.course_grades.keys():

            sum += self.__convert_letter_to_gpa(self.course_grades[key])

        return round(sum/len(self.course_grades), 2)


    """returns a string representation of student"""
    def __str__(self) -> str:

        return f"cwid: {self.cwid}, name: {self.name}, major: {self.major}, courses: {self.course_grades}"

    """compares two students and returns True if instance data is the same"""
    def __eq__(self, other: "Student") -> bool:

        if self.cwid == other.cwid:
            if self.name == other.name:
                if self.major == other.major:
                    if sorted(self.course_grades.keys()) == sorted(other.course_grades.keys()):
                        for key in self.course_grades.keys():
                            if self.course_grades[key] != other.course_grades[key]:
                                return False
                        return True
        return False

"""Object to represent an Instructor"""
class Instructor:

    """constructor provides unique identifier, cwid, and the instructors name, department, and courses the instructor teaches"""
    def __init__(self, cwid: str, name: str, department: str, courses: Dict[str, int]):

        self.cwid = cwid
        self.name = name
        self.department = department
        self.courses = courses
    
    """adds 1 student to given course instructor teaches"""
    def add_student_to_course(self, course: str):

        if course in self.courses.keys():
            self.courses[course] += 1
        else:
            self.courses[course] = 1

    """returns a tuple of instance data"""
    def get_data(self) -> (int, str, str, Dict[str,int]):
        
        return (self.cwid, self.name, self.department, self.courses)

    """returns a string representation of instructor"""
    def __str__(self) -> str:

        return f"{self.cwid}, {self.name}, {self.department}, {self.courses}"

    """compares two instructors and returns True if instance data is the same"""
    def __eq__(self, other: "Instructor") -> bool:

        if self.cwid == other.cwid:
            if self.name == other.name:
                if self.department == other.department:
                    if sorted(self.courses.keys()) == sorted(other.courses.keys()):
                        for key in self.courses.keys():
                            if self.courses[key] != other.courses[key]:
                                return False
                        return True
        return False

class Major:

    """constructor provides name of major, a list of required courses and a list of elective courses"""
    def __init__(self, major: str, required_courses: List[str], elective_courses: List[str]):

        self.major = major
        self.required_courses = required_courses
        self.elective_courses = elective_courses
    
    """adds the given coure to either required or elective courses depending on flag"""
    def add_course_to_major(self, course: str, flag: str):

        if flag == 'R':
            self.required_courses.append(course)
        elif flag == 'E':
            self.elective_courses.append(course)
        else:
            raise Exception("Invalid course flag, must be R or E")
    
    """if instance data is equal to other object returns true"""
    def __eq__(self, other: "Major") -> bool:

        if self.elective_courses == other.elective_courses:
            if self.required_courses == other.required_courses:
                if self.major == other.major:
                    return True

        return False



class Repository:

    """constructor adds list of students and instructors to instance and path of directory files are stored in"""
    def __init__(self, dir_path: str):
        self.students: List["Student"] = []
        self.instructors: List["Instructor"] = []
        self.majors: List["Major"] = []
        self.dir_path = dir_path
        self.read_majors()
        self.read_students()
        self.read_instructors()
        self.read_grades()
        
        

    """Print student grades pretty table using database data"""
    def student_grades_table_db(self, db_path):
        
        db: sqlite3.Connection = sqlite3.connect(db_path)
        print("Student Grade Summary")
        pt: PrettyTable = PrettyTable(field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])

        for row in db.execute("SELECT Students.Name as Student, Students.CWID, Course, Grade, Instructors.Name as Instructor From Grades Join Students on Grades.StudentCWID = Students.CWID Join Instructors on Grades.InstructorCWID = Instructors.CWID Order BY Students.Name"):
            pt.add_row(row)

        
        print(pt)

    
    """reads students.txt in directory and adds student data to students list"""
    def read_students(self):
    
        students_gen: Iterator[List[str]] = file_reader(path.join(self.dir_path, "students.txt"), 3, sep = "\t", header = True)
        for student in students_gen:
            self.students.append(Student(student[0],student[1],student[2],{}))
       
    """reads instructors.txt in directory and adds instructor data to instructor list"""
    def read_instructors(self):

        instructors_gen: Iterator[List[str]] = file_reader(path.join(self.dir_path, "instructors.txt"), 3, sep = "\t", header = True)
        for instructor in instructors_gen:
            self.instructors.append(Instructor(instructor[0],instructor[1],instructor[2],{}))
        
    """reads grades.txt in directory and adds grades to each student in list of students, and add course to each instructor in list of instructors"""
    def read_grades(self):

        grades_gen: Iterator[List[str]] = file_reader(path.join(self.dir_path, "grades.txt"), 4, sep = "\t", header = True)

        for line in grades_gen:

            

            self.add_course_to_student(line[0], line[1], line[2])

            self.add_course_to_instructor(line[3],line[1])

    """reads majors.txt in directory and adds new majors to majors list and also adds the required courses to the majors in the list"""
    def read_majors(self):

        majors_gen: Iterator[List[str]] = file_reader(path.join(self.dir_path, "majors.txt"), 3, sep = "\t", header = True)

        for line in majors_gen:

            is_in_list: bool = False
            if len(self.majors) > 0:
                for m in self.majors:

                    if line[0] == m.major:
                        is_in_list = True
                        m.add_course_to_major(line[2], line[1])

            if is_in_list == False:
                m: "Major" = Major(line[0],[],[])
                m.add_course_to_major(line[2],line[1])
                self.majors.append(m)
            
    """add the given course and grade to the student in list of students with given cwid"""
    def add_course_to_student(self, cwid: int, course: str, grade: str):

        new_student: bool = False
        for student in self.students:

                if student.cwid == cwid:

                    new_student = True
                    student.course_grades[course] = grade

        if new_student == False:

            print("grades.txt includes unknown student")
                    
    """add the given course to instructor with given cwid in list of instructors"""
    def add_course_to_instructor(self, cwid: int, course: str):

        new_instructor: bool = False

        for instructor in self.instructors:

                new_instructor = True

                if instructor.cwid == cwid:

                    instructor.add_student_to_course(course)

        if new_instructor == False:

            print("grades.txt includes unknown instructor")

    """returns True if grade is failing, False if it is passing"""
    def __did_fail_course(self, grade: str):

        if grade in ('A', 'A-', 'B+', 'B', 'B-', 'C+','C'):
            return False
        else:
            return True
                
    """print a pretty table of the list of students"""
    def print_student_pretty_table(self):

        print("Student Summary")
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives', 'GPA'])

        for student in self.students:

            for m in self.majors:
                if m.major == student.major:
                    major: "Major" = m
            
            courses: [str] = []
            for key in student.course_grades.keys():
                
                if not self.__did_fail_course(student.course_grades[key]):
                    courses.append(key)


            remaining_required = []
            for course in major.required_courses:
                if course not in courses:
                    remaining_required.append(course)

            remaining_electives = major.elective_courses
            did_take_elective: bool = False
            for course in major.elective_courses:
                if course in courses:
                    did_take_elective = True

            if did_take_elective:
                remaining_electives = []

            pt.add_row([student.cwid, student.name, student.major, sorted(courses), sorted(remaining_required), sorted(remaining_electives), student.calculate_gpa()])
        
        print(pt)

    """print a pretty table of list of instructors"""
    def print_instructor_pretty_table(self):
        
        print("Instructor Summary")
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])

        for instructor in self.instructors:
            
            if instructor.courses != {}: 
                for key in instructor.courses.keys():
                    pt.add_row([instructor.cwid, instructor.name, instructor.department, key, instructor.courses[key]])
        
        print(pt)

    """print a pretty table of list of Majors"""
    def print_majors_pretty_table(self):

        print("Majors Summary")
        pt: PrettyTable = PrettyTable(field_names=['Major', 'Required Courses', 'Electives'])

        for m in self.majors:

            pt.add_row([m.major, sorted(m.required_courses), sorted(m.elective_courses)])

        print(pt)


if __name__ == "__main__":
    repo = Repository("/Users/MyICloud/Documents/GitHub/Student-Repository")