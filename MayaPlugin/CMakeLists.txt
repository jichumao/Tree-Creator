cmake_minimum_required(VERSION 3.18)
project(LSystem)

set(CMAKE_CONFIGURATION_TYPES "Release" CACHE STRING "Limited configurations" FORCE)
set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Set the build type to Release by default" FORCE)

mark_as_advanced(CMAKE_BUILD_TYPE CMAKE_CONFIGURATION_TYPES)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(MAYA_LOCATION "D:\\App\\Autodesk\\Maya2024")

if (NOT EXISTS "${MAYA_LOCATION}")
  message(FATAL_ERROR "Maya not found at ${MAYA_LOCATION}, please set MAYA_LOCATION to the correct path!!!")
endif()

set(BUILD_WITH_PYTHON_3 ON)
set(MAYA_PY_EXECUTABLE "${MAYA_LOCATION}/bin/mayapy.exe")
set(Python_EXECUTABLE "${MAYA_PY_EXECUTABLE}")

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(python)
include(swig)

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

include_directories(${PYTHON_INCLUDE_DIRS})

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

set_property(SOURCE src/LSystem.i PROPERTY CPLUSPLUS ON)
swig_add_library(LSystem
  TYPE MODULE
  LANGUAGE python
  SOURCES src/LSystem.i src/LSystem.cpp src/vec.cpp)

add_custom_command(TARGET LSystem POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${CMAKE_CURRENT_BINARY_DIR}/LSystem.py"
    "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Release/LSystem.py"
    COMMENT "Copying LSystem.py to bin directory")
swig_link_libraries(LSystem ${PYTHON_LIBRARIES})

target_include_directories(LSystem PRIVATE ${PYTHON_INCLUDE_DIRS})

set_target_properties(LSystem PROPERTIES OUTPUT_NAME "_LSystem" PREFIX "" SUFFIX ".pyd")
