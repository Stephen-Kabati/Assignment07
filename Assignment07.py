# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
#       with structured error handling and class inheritance
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Stephen Kabati,8/11/2026,Added Person and Student classes with inheritance
#   Stephen Kabati,8/11/2026,Added properties with validation per Mod07-Lab02
#   Stephen Kabati,8/11/2026,Converted dictionary data to Student objects per Mod07-Lab01
#   Stephen Kabati,8/11/2026,Implemented JSON conversion per Demo05
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str = ""  # Hold the choice made by the user.


class Person:
    """
    A class representing person data.

    Properties:
        first_name (str): The person's first name.
        last_name (str): The person's last name.

    ChangeLog:
        - RRoot, 1.1.2030: Created the class.
        - Stephen Kabati, 8/11/2026: Added properties with validation per Mod07-Notes
    """

    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name  # Uses property setter for validation
        self.last_name = last_name    # Uses property setter for validation

    @property  # (getter or accessor)
    def first_name(self):
        return self.__first_name.title()  # Formatting data in title case

    @first_name.setter  # (setter or mutator)
    def first_name(self, value: str):
        if value.isalpha() or value == "":  # Simple validation per Mod07-Lab02
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property  # (getter or accessor)
    def last_name(self):
        return self.__last_name.title()  # Formatting data in title case

    @last_name.setter  # (setter or mutator)
    def last_name(self, value: str):
        if value.isalpha() or value == "":  # Simple validation per Mod07-Lab02
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self):
        """Override default __str__ to return comma-separated person data."""
        return f'{self.first_name},{self.last_name}'


class Student(Person):
    """
    A class representing student data that inherits from Person.

    Properties:
        first_name (str): The student's first name (inherited from Person).
        last_name (str): The student's last name (inherited from Person).
        course_name (str): The course name.

    ChangeLog:
        - RRoot, 1.1.2030: Created the class.
        - Stephen Kabati, 8/11/2026: Inherited from Person per Mod07-Lab03
        - Stephen Kabati, 8/11/2026: Added course_name property
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        # Call to the Person constructor per Mod07-Lab03 instructions
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name  # Uses property setter

    @property  # (getter or accessor)
    def course_name(self):
        return self.__course_name

    @course_name.setter  # (setter or mutator)
    def course_name(self, value: str):
        if not isinstance(value, str):  # Simple type validation
            raise ValueError("Course name must be a string.")
        self.__course_name = value

    def __str__(self):
        """Override Parent __str__ to return comma-separated student data."""
        return f'{self.first_name},{self.last_name},{self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    Stephen Kabati,8/11/2026,Converted code to use student objects per Mod07-Lab01
    Stephen Kabati,8/11/2026,Added JSON conversion logic per Demo05
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of dictionary rows
        then converts them to Student objects.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stephen Kabati,8/11/2026,Converted list of dictionaries to list of student objects

        :param file_name: string data with name of file to read from
        :param student_data: list of student rows to be filled with file data

        :return: list
        """
        file = None

        try:
            # Get a list of dictionary rows from the data file
            file = open(file_name, "r")
            json_students = json.load(file)

            # Convert the list of dictionary rows into a list of Student objects
            # Referencing Demo05-ConvertingJsonAndStudentObjects.py
            for student in json_students:
                student_object = Student(first_name=student["FirstName"],
                                         last_name=student["LastName"],
                                         course_name=student["CourseName"])
                student_data.append(student_object)

        except FileNotFoundError as e:
            IO.output_error_messages(message="Error: The file was not found.", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            if file is not None and file.closed == False:
                file.close()

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of Student objects

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stephen Kabati,8/11/2026,Converted Student objects to dictionaries for JSON

        :param file_name: string data with name of file to write to
        :param student_data: list of Student rows to be written to the file

        :return: None
        """
        file = None

        try:
            # Convert Student objects into dictionaries per Demo05 and Mod07-Lab01
            list_of_dictionary_data: list = []
            for student in student_data:
                student_json: dict = {"FirstName": student.first_name,
                                      "LastName": student.last_name,
                                      "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)

            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file, indent=2)

            IO.output_student_and_course_names(student_data=student_data)
        except TypeError as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file is not None and file.closed == False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    Stephen Kabati,8/11/2026,Converted methods to use student objects per Mod07-Labs
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the a custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stephen Kabati,8/11/2026,Converted to display Student object data using __str__

        :param student_data: list of Student rows to be displayed

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            # Uses the overridden __str__() method to display comma-separated values
            # per Mod07-Assignment requirements and Mod07-Lab03
            print(student)
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stephen Kabati,8/11/2026,Converted to use Student objects with property validation

        :param student_data: list of Student rows to be filled with input data

        :return: list
        """
        try:
            # Input the data with validation per Mod07-Lab02 and Mod07-Assignment
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the name of the course: ")

            # Create a Student object using property validation
            # Properties enforce validation via setters per Mod07-Notes and Demo03
            student = Student(first_name=student_first_name,
                              last_name=student_last_name,
                              course_name=course_name)

            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was not the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of Student objects
# Conversion pattern referenced from Demo05-ConvertingJsonAndStudentObjects.py
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")
