from Student_Repository_Mark_Paris import Student, Instructor, Repository, Major
import unittest
from typing import Tuple
import sqlite3

s1:"Student" = Student("10103", "Baldwin, C", "SFEN",{'SSW 567': 'A','SSW 564': 'A-','SSW 687': 'B', 'CS 501': 'B'})        
s2:"Student" = Student("10115","Wyatt, X","SFEN",{'SSW 567': 'A','SSW 564': 'B+','SSW 687': 'A','CS 545': 'A'})
i1:"Instructor" = Instructor("98765", "Einstein, A", "SFEN",{'SSW 567': 2})        
i2:"Instructor" = Instructor("98764","Feynman, R","SFEN",{"SSW 564": 2, "SSW 687": 2, "CS 501": 1, "CS 545": 1})
m1: "Major" = Major("SFEN",["SSW 540","SSW 564", "SSW 555", "SSW 567"],["CS 501","CS 513", "CS 545"])
repo = Repository("/Users/MyICloud/Documents/GitHub/Student-Repository/tests")

class StudentTest(unittest.TestCase):

    def test_calculate_gpa(self) -> None:

        self.assertEqual(s1.calculate_gpa(), 3.44)



"""test Repository"""
class RepositoryTest(unittest.TestCase):

    """tests if data going into student pretty table is accurate for test files"""
    def test_print_student_pretty_table(self) -> None:
 
        
        students2: ["Student"] = [s1,s2]
        

        for index in range(len(repo.students)):

            self.assertTrue(repo.students[index] == students2[index])

    """test if data retreived from database matches expected data"""
    def test_student_grades_table_db(self) -> None:
        expected: [Tuple] = [("Bezos, J", "10115", "SSW 810","A","Rowland, J"),
            ("Bezos, J", "10115", "CS 546", "F", "Hawking, S"),
            ("Gates, B", "11714", "SSW 810", "B-", "Rowland, J"),
            ("Gates, B", "11714", "CS 546", "A" , "Cohen, R"),
            ("Gates, B", "11714", "CS 570", "A-", "Hawking, S"),
            ("Jobs, S", "10103", "SSW 810", "A-", "Rowland, J"),
            ("Jobs, S", "10103", "CS 501", "B", "Hawking, S"),
            ("Musk, E", "10183", "SSW 555", "A", "Rowland, J"),
            ("Musk, E", "10183", "SSW 810", "A", "Rowland, J")]


        db: sqlite3.Connection = sqlite3.connect("/Users/MyICloud/Developer/810_startup.db")
        i: int = 0
        for row in db.execute("SELECT Students.Name as Student, Students.CWID, Course, Grade, Instructors.Name as Instructor From Grades Join Students on Grades.StudentCWID = Students.CWID Join Instructors on Grades.InstructorCWID = Instructors.CWID Order BY Students.Name"):
            self.assertEqual(expected[i], row)
            i += 1

        
        
    """tests if data going into instructor pretty table is accurate for test files"""
    def test_print_instructor_pretty_table(self) -> None:

        
        instructors2: ["Instructor"] = [i1,i2]

        for index in range(len(repo.instructors)):
            
            self.assertTrue(repo.instructors[index] == instructors2[index])

    """tests if data going into majors pretty table is accurate for test files"""
    def test_print_majors_pretty_table(self) -> None:
        
        majors2: ["Major"] = [m1]
        for index in range(len(repo.majors)):
            
            self.assertTrue(repo.majors[index] == majors2[index])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)