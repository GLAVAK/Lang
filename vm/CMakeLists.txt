cmake_minimum_required(VERSION 3.6)
project(vm)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
        vm.h vm.c
        opcode.h
        utils.h utils.c
        data_cell.h
        read_helpers.h read_helpers.c)

add_executable(launcher ${SOURCE_FILES} launcher.c)

set_target_properties( launcher PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin/ )