#  Yishai Lutvak

import sys
import os
import operator

PATH = 0
READ_FILE = 1
WRITE_FILE = 2

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


def check_files_exist():
    """
    :return True if two file names were received
    else return False
    """
    if len(sys.argv) == 3:
        return True
    return False


def check_file_name(file_name):
    """
    :parameter file_name - string of name of file
    :return True if file is exist
    else return False
    """
    path_file = sys.argv[PATH]
    index_of_last_slash = path_file.rfind("/")
    directory = path_file[:index_of_last_slash]
    print(directory)
    print(os.listdir(directory))
    if file_name in os.listdir(directory):
        return True
    return False


def parser(line):
    """
    :parameter line - string of line from file
    :return list of items in string by space
    """
    return line.split(" ")


def check_format(my_list):
    """
    :parameter my_list - list of items in line of file
    :return True if format is valid
    else return False
    """
    if len(my_list) != 3:
        return False
    if not my_list[0].isdigit():
        return False
    if not my_list[2].isdigit():
        return False
    if not my_list[1] in ops:
        return False
    return True


def calc(my_list):
    """
    :parameter my_list - list of items in line of file
    :return number that it result of exercise
    """
    op1 = int(my_list[0])
    op2 = int(my_list[2])
    operation = my_list[1]
    if operation == '/' and op2 == 0:
        print("Error - Division by 0 is impossible")
        return
    return ops[operation](op1, op2)


def main():
    """
    get two names of file via edit configuration
    and read file of exercises
    and write to file of solution the exercises and their solution
    """
    assert check_format(["3", "+", "4"]) is True
    assert check_format(["3", "+", "4", "="]) is False
    assert check_format(["3", "%", "4"]) is False
    assert check_format(["a", "%", "4"]) is False
    assert (calc(["3", "+", "4"]) == 7) is True
    assert (calc(["3", "+", "4"]) == 8) is False
    assert (parser("3 + 4") == ["3", "+", "4"]) is True
    assert (parser("3 + 4") == [3, "+", 4]) is False

    if not check_files_exist():
        print("No two files were accepted as arguments")
        return

    if not check_file_name(sys.argv[WRITE_FILE]) or not check_file_name(sys.argv[READ_FILE]):
        print("Invalid names of files")
        return

    output_file = open(sys.argv[WRITE_FILE], 'w')
    with open(sys.argv[READ_FILE], 'r') as input_file:
        for line in input_file:
            output_file.write(line[:-1])
            my_list = parser(line[:-1])
            if check_format(my_list):
                output_file.write(" = " + str(calc(my_list)) + "\n")
            else:
                print("Error - The exercise is not in the correct format")
                output_file.write(" invalid format\n")
    output_file.close()
    return


if __name__ == "__main__":
    main()
