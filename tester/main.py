import os
import sys
from os import listdir
from subprocess import call

files = listdir("tests")

tests = []

for file in files:
    if file.endswith(".out.txt"):
        tests.append(file[0:-len(".out.txt")])

print(str(len(tests)) + " tests loaded")

passed_tests = 0
for test_name in tests:
    bytecode = open("tests/" + test_name + ".bytecode.txt", "w")
    actual_output = open("tests/" + test_name + ".actual_output.txt", "w")
    input_file = open("tests/" + test_name + ".in.txt")

    call([sys.executable, "compiler/main.py", "tests/" + test_name + ".txt", "tests/" + test_name + ".bin"],
         stdout=bytecode)
    call(["vm/bin/launcher.exe", "tests/" + test_name + ".bin"], stdin=input_file, stdout=actual_output)

    bytecode.close()
    actual_output.close()
    input_file.close()

    actual_output = open("tests/" + test_name + ".actual_output.txt")
    expected_output = open("tests/" + test_name + ".out.txt")

    if actual_output.read() == expected_output.read():
        actual_output.close()
        expected_output.close()

        print(" Test '" + test_name + "' passed")
        passed_tests += 1

        os.remove("tests/" + test_name + ".actual_output.txt")
        os.remove("tests/" + test_name + ".bytecode.txt")
        os.remove("tests/" + test_name + ".bin")
    else:
        print(" Test '" + test_name + "' failed. Program bytecode and actual output saved")

if passed_tests == len(tests):
    print("[OK] All "+str(passed_tests)+" tests passed!")
else:
    print("[FAIL] "+str(passed_tests)+"/"+str(len(tests))+" tests passed!")
