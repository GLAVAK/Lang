cmake_minimum_required(VERSION 3.6)
project(vm)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
        vm.c
        opcode.h
        vm.h utils.h utils.c)

add_executable(launcher ${SOURCE_FILES} launcher.c)
add_executable(tester ${SOURCE_FILES} tester.c)