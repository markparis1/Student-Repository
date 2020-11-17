from typing import Dict, Tuple, List, Iterator, IO
from prettytable import PrettyTable
from os import path

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


class Repository:

    """constructor adds list of students and instructors to instance and path of directory files are stored in"""
    def __init__(self, dir_path: str):
        self.students: List["Student"] = []
        self.instructors: List["Instructor"] = []
        self.dir_path = dir_path
        self.read_students()
        self.read_instructors()
        self.read_grades()
    
    """reads students.txt in directory and adds student data to students list"""
    def read_students(self):
    
        students_gen: Iterator[List[str]] = file_reader(path.join(self.dir_path, "students.txt"), 3, sep = ";", header = True)
        for student in students_gen:
            self.students.append(Student(student[0],student[1],student[2],{}))
       
    """reads instructors.txt in directory and adds instructor data to instructor list"""
    def read_instructors(self):

        instructors_gen: Iterator[List[str]] = file_reader(path.join(self.dir_path, "instructors.txt"), 3, sep = "|", header = True)
        for instructor in instructors_gen:
            self.instructors.append(Instructor(instructor[0],instructor[1],instructor[2],{}))
        
    """reads grades.txt in directory and adds grades to each student in list of students, and add course to each instructor in list of instructors"""
    def read_grades(self):

        grades_gen: Iterator[List[str]] = file_reader(path.join(self.dir_path, "grades.txt"), 4, sep = "|", header = True)

        for line in grades_gen:

            self.add_course_to_student(line[0], line[1], line[2])

            self.add_course_to_instructor(line[3],line[1])
    
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
                
    """print a pretty table of the list of students"""
    def print_student_pretty_table(self):

        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])

        for student in self.students:

            pt.add_row([student.cwid, student.name, sorted(list(student.course_grades.keys()))])
        
        print(pt)

    """print a pretty table of list of instructors"""
    def print_instructor_pretty_table(self):
        
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])

        for instructor in self.instructors:
            
            if instructor.courses != {}: 
                for key in instructor.courses.keys():
                    pt.add_row([instructor.cwid, instructor.name, instructor.department, key, instructor.courses[key]])
        
        print(pt)

if __name__ == "__main__":
    repo = Repository("/Users/MyICloud/Documents/GitHub/Student-Repository")
    repo.print_student_pretty_table()