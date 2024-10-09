#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""try-accept.py within https://github.com/bomonike/python-samples/
Program to demo try/except blocks catch errors to provide a smoother custom message.
GLOSSARY: Exception = an event detected during execution that interrupt the flow of a program.

gas "v001 new :try-accept.py"

TODO: Log errors appropriately.
TODO: Debug using import pdb; pdb.set_trace() or ic()

References:
* https://docs.python.org/3/library/exceptions.html provides all details.
* https://www.youtube.com/watch?v=nlCKrKGHSSk by dominatrix Socratica at http://bit.ly/PythonHelloWorld
* https://www.youtube.com/watch?v=KdMAj8Et4xk by Giraffe Academy [basic]
* https://www.youtube.com/watch?v=j_q6NGOwDJo&t=22s by Bro Code [uses manual input()]
* https://www.youtube.com/watch?v=ZUqGMDppEDs&t=49s by 
* https://www.youtube.com/watch?v=ZsvftkbbrR0&t=
* https://www.youtube.com/watch?v=NIWwJbo-9_8 by Imdad Codes 
* https://www.youtube.com/watch?v=fhxByMe0mq8 by techTFQ
* https://www.youtube.com/watch?v=odrgC7T-q2s&list=PLXovS_5EZGh7MMmgukUeg8rE8pfean17G&pp=iAQB by leardata
* https://www.youtube.com/watch?v=ZsvftkbbrR0&t=1m53 by AjanCodes catches Flask route errors (connection)
"""

def divide_num(a, b) -> int:
    try:
        print(f"INFO: Trying to divide {a} / {b}...")
        divided = a / b
    except ValueError as e:
        print(f"WARNING: ValueError: {a}")
        pass
    except ZeroDivisionError as e:
        print(f"FATAL: ZeroDivisionError: {e}")
        return 1
    except Exception as e:  # The most generic of exception catching. Put this last.
        print(f"FATAL: Generic exception: {e}")
        # Instead of return 1
        sys.exit('Unanticipated exception: Terminating program!')
    else:  # when no exception was found:
        print(f"INFO: all fine...")
        return divided

def input_file_a_read() -> int:
    input_file_a="somefile.txt"
    try:
        print(f"INFO: Trying to open file {input_file_a}...")
        f = open(input_file_a)
        if f.name == input_file_a:
            print(f"ERROR: Raising exception open file {input_file_a}: {e}")
            raise Exception
    except FileNotFoundError as e:
        print(f"ERROR: opening file: {e}")  # assuming file name is in error message.
        return 1
    except Exception as e:  # The most generic of exception catching. Put this last.
        print(f"ERROR: Generic exception: {e}")
        return 1
    else:  # when no exception was found:
        print(f"INFO: Reading opened file {input_file_a}...")
        print(f.read())
    finally:  # executed even if exiting program (no matter what, error or no error): https://www.youtube.com/watch?v=92JdbyISpCo
        print(f"INFO: Finally: closing {input_file_a}...")
        f.close()
        return 0

if __name__ == "__main__":

#     print("divide_num=", divide_num(9,3) )  # Happy path.
     print("divide_num=", divide_num(9.9,0.1) )  # ValueError expected.
#     print("divide_num=", divide_num(9,0) )  # ZeroDivisionError expected.

#     print( input_file_a_read() )