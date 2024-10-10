#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""try-accept.py within https://github.com/wilsonmar/python-samples/blob/main/try-accept.py
Program to demo try/except blocks catch errors to provide a smoother custom message.
GLOSSARY: Exception = an event detected during execution that interrupt the flow of a program.
To run using pytest on CLI, first pip install -U pytest (version pytest 8.3.3) https://docs.pytest.org/en/stable/getting-started.html

gas "v010 + logging videos :try-accept.py"

TODO: + Debug using import pdb; pdb.set_trace() or ic()

References:
* https://docs.python.org/3/library/exceptions.html provides all details.
* https://www.programiz.com/python-programming/exceptions
* https://blog.airbrake.io/blog/python/class-hierarchy
* https://www.geeksforgeeks.org/built-exceptions-python/
* https://www.youtube.com/watch?v=NIWwJbo-9_8 by Corey Schafe [smooth presentation on file exceptions]
* https://www.youtube.com/watch?v=nlCKrKGHSSk by dominatrix Socratica at http://bit.ly/PythonHelloWorld
* https://www.youtube.com/watch?v=j_q6NGOwDJo&t=22s by Bro Code [uses manual input()]
Alternatives:
* https://www.youtube.com/watch?v=ZUqGMDppEDs&t=49s 
* https://www.youtube.com/watch?v=6SPDvPK38tw&t=25s types of errors
* https://www.youtube.com/watch?v=fhxByMe0mq8 by techTFQ
* https://www.youtube.com/watch?v=w_ZRcN-hpGI "Multiple Exceptions"
* https://www.youtube.com/watch?v=odrgC7T-q2s&list=PLXovS_5EZGh7MMmgukUeg8rE8pfean17G&pp=iAQB by leardata
* https://www.youtube.com/watch?v=ZsvftkbbrR0&t=1m53 by AjanCodes catches Flask route errors (connection)
* https://www.linkedin.com/learning/certified-entry-level-python-programmer-pcep-30-02-cert-prep/using-exceptions-and-try-except?autoSkip=true&resume=false
Ignore (not much value):
* https://www.youtube.com/watch?v=qOuOV4pDVGY by Patrick Loeber
* https://www.youtube.com/watch?v=68pauJ81pKs by Anjali Sharma "Nested try-except-finally"
* https://www.youtube.com/watch?v=Iflu9zEJipQ "Exceptions vs Errors" by Lex Friedman interviewing Chris Lattner 
* https://www.youtube.com/watch?v=KdMAj8Et4xk by Giraffe Academy [basic]
* https://www.w3schools.com/python/python_ref_exceptions.asp glossary of exceptions

# Logging the new way vs. old dunder method:
* https://www.youtube.com/watch?v=m08LtvC3jaY by NeuralNine
* https://www.youtube.com/watch?v=aJCK0LWz8kg by BetterStack
* https://www.youtube.com/watch?v=gCD-Wsb_Iw4 by Richard Schwabe
* https://www.youtube.com/watch?v=p3HWzTYUfu8 by teclado
* https://www.youtube.com/watch?v=gsa1oFn9n0M by techTFQ
"""
import pytest

def divide_num(a, b) -> int:
    try:  # PROTIP: Specify the severity of each message:
        print(f"INFO: Trying to divide {a} / {b}...")
        #divided = float(a) / float(b)  # to ensure it works.
        divided = a / b
    except TypeError as e:
        print(f"WARNING: TypeError: {a}")  # if a or b is a not converted to a float:
        # Cannot be divided = float(a) / float(b)  # to ensure it works.
        return None # PROTIP: Return value None so caller can take approriate action.
    except ValueError as e:  #  wrong value in a specified data type.
        print(f"WARNING: ValueError: {a}")  # if a or b is a string that can't be converted to a number.
        return None
    except ZeroDivisionError as e:  # PROTIP: Include official name of exception in message:
        print(f"FATAL: ZeroDivisionError: {e}")
        return None
    except ArithmeticError as e:
        print(f"WARNING: ArithmeticError: {a}")
        return None
    except KeyboardInterrupt as e:
        sys.exit('FATAL: User-issued interrupt stopping program!')
    except Exception as e:  # Catch all other exceptions. PROTIP: Put this last.
        print(f"FATAL: Generic exception: {e}")
        # Instead of return 1
        sys.exit('CRITICAL: Unanticipated exception: Terminating program!')
    else:  # when no exception was found:
        print(f"INFO: all fine...")
        return divided  # from try: above.

# TODO: OverFlowError
# TODO: AttributeError

def input_file_a_read() -> int:
    input_file_a="somefile.txt"
    try:
        print(f"INFO: Trying to open file {input_file_a}...")
        f = open(input_file_a)
        if f.name == input_file_a:
            print(f"ERROR: Raising exception open file {input_file_a}: {e}")
            raise Exception
    # except PermissionError as e:
    # except TimeoutError as e:
    except FileNotFoundError as e:
        print(f"ERROR: opening file: {e}")  # assuming file name is in error message.
        return 1
    except Exception as e:  # Catch all other exceptions. PROTIP: Put this last.
        print(f"ERROR: Generic exception: {e}")
        return 1
    else:  # when no exception was found:
        print(f"INFO: Reading opened file {input_file_a}...")
        print(f.read())
    finally:  # executed even if exiting program (no matter what, error or no error): https://www.youtube.com/watch?v=92JdbyISpCo
        print(f"INFO: Finally: closing {input_file_a}...")
        f.close()
        return 0

# TODO: def LookupIndexError & LookupKeyError

# Run in CLI: pytest try-accept.py
def test_happy_path():
    assert divide_num(8,2) == 4     # Happy path.
def test_data_type_err():
    assert divide_num('9',3) == 3     # Data Type Error expected.
def test_divide_by_zero():
    assert divide_num(4,0) == None


if __name__ == "__main__":

#     print(dir(locals()['__builtins__']))  # all exceptions in one line.

    divided = divide_num(4,2)    # Happy path.
    divided = divide_num('9',3)   # Data Type Error expected.
    if divided == None:
       print(f"YIKES: divide_num={divided}" )
    else:
        print(f"divide_num={divided}" )
    divided = divide_num('x',1) # ValueError expected.
    divided = divide_num(9,0)     # ZeroDivisionError expected.

#    print( input_file_a_read() )