import json
import os


class StudentRecordError(Exception):
    pass


def validate_student(student, student_ids):

    if not isinstance(student, dict):
        raise TypeError("Student record must be a dictionary")

    student_id = student["student_id"]
    name = student["name"]
    department = student["department"]
    marks = student["marks"]

    if not isinstance(student_id, str):
        raise TypeError("Student ID must be text")

    if not isinstance(name, str):
        raise TypeError("Name must be text")

    if not isinstance(department, str):
        raise TypeError("Department must be text")

    if student_id == "" or name == "" or department == "":
        raise ValueError("Fields cannot be empty")

    if student_id in student_ids:
        raise StudentRecordError("Duplicate student ID")

    if not isinstance(marks, list):
        raise TypeError("Marks must be a list")

    if len(marks) != 3:
        raise StudentRecordError(
            "Marks must contain exactly 3 values"
        )

    for mark in marks:

        if isinstance(mark, bool):
            raise StudentRecordError("Boolean marks are not allowed")

        if not isinstance(mark, (int, float)):
            raise TypeError("Marks must be numeric")

        if mark < 0 or mark > 100:
            raise StudentRecordError(
                "Marks must be between 0 and 100"
            )

    student_ids.append(student_id)

    return student


def main():

    file_name = input(
        "Enter input file name (press Enter for default): "
    )

    if file_name == "":
        file_name = "students_input.json"

    print("\nImport started:", file_name)

    valid_students = []
    errors = []
    student_ids = []

    try:

        with open(file_name, "r", encoding="utf-8") as file:
            students = json.load(file)

        if not isinstance(students, list):
            raise TypeError("JSON data must contain a list")

    except FileNotFoundError:
        print("Error: File not found")
        errors.append("File not found: " + file_name)
        write_errors(errors)
        return

    except PermissionError:
        print("Error: Permission denied")
        errors.append("Permission denied")
        write_errors(errors)
        return

    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        errors.append("Invalid JSON format")
        write_errors(errors)
        return

    except TypeError as e:
        print("Error:", e)
        errors.append(str(e))
        write_errors(errors)
        return

    except OSError as e:
        print("File error:", e)
        errors.append(str(e))
        write_errors(errors)
        return

    else:

        for i in range(len(students)):

            try:

                student = validate_student(
                    students[i], student_ids
                )

                valid_students.append(student)

                print(
                    "Accepted:",
                    student["student_id"],
                    "-",
                    student["name"]
                )

            except KeyError as e:
                errors.append(
                    "Record " + str(i + 1) +
                    ": Missing field " + str(e)
                )

            except TypeError as e:
                errors.append(
                    "Record " + str(i + 1) +
                    ": " + str(e)
                )

            except ValueError as e:
                errors.append(
                    "Record " + str(i + 1) +
                    ": " + str(e)
                )

            except StudentRecordError as e:
                errors.append(
                    "Record " + str(i + 1) +
                    ": " + str(e)
                )

            except IndexError:
                errors.append(
                    "Record " + str(i + 1) +
                    ": Invalid record index"
                )

    finally:
        print("\nImport process finished.")


    try:

        with open(
            "students_valid.json", "w", encoding="utf-8"
        ) as file:

            json.dump(valid_students, file, indent=4)

        with open(
            "import_errors.txt", "w", encoding="utf-8"
        ) as file:

            for error in errors:
                file.write(error + "\n")

    except OSError as e:
        print("Output file error:", e)
        return

    print("\nImport completed.")

    print("Accepted records:", len(valid_students))
    print("Rejected records:", len(errors))

    print("Valid output: students_valid.json")
    print("Error log: import_errors.txt")


def write_errors(errors):

    try:
        with open(
            "import_errors.txt", "w", encoding="utf-8"
        ) as file:

            for error in errors:
                file.write(error + "\n")

    except OSError:
        print("Could not create error log file")


main()