from Student_Repository_Mark_Paris import Student, Instructor, Repository
import unittest



"""test Repository"""
class RepositoryTest(unittest.TestCase):

    
    """tests if data going into student pretty table is accurate for test files"""
    def test_print_student_pretty_table(self) -> None:
 
        s1:"Student" = Student("10103", "Baldwin, C", "SFEN",{'SSW 567': 'A','SSW 564': 'A-','SSW 687': 'B', 'CS 501': 'B'})        
        s2:"Student" = Student("10115","Wyatt, X","SFEN",{'SSW 567': 'A','SSW 564': 'B+','SSW 687': 'A','CS 545': 'A'})
        students2: ["Student"] = [s1,s2]
        repo = Repository("/Users/MyICloud/Developer/HW09/tests")

        for index in range(len(repo.students)):

            self.assertTrue(repo.students[index] == students2[index])
        
        
    """tests if data going into instructor pretty table is accurate for test files"""
    def test_print_instructor_pretty_table(self) -> None:
        
        i1:"Instructor" = Instructor("98765", "Einstein, A", "SFEN",{'SSW 567': 2})        
        i2:"Instructor" = Instructor("98764","Feynman, R","SFEN",{"SSW 564": 2, "SSW 687": 2, "CS 501": 1, "CS 545": 1})
        instructors2: ["Instructor"] = [i1,i2]
        repo = Repository("/Users/MyICloud/Developer/HW09/tests")

        for index in range(len(repo.instructors)):

            self.assertTrue(repo.instructors[index] == instructors2[index])



if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)