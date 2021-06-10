cmake_minimum_required(VERSION 3.11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS_DEBUG "-O3 -Wall")

project(flush-shanten)

add_subdirectory(shanten-number-calculator)

add_executable(verify verify.cpp shanten-number-calculator/calsht.cpp)
