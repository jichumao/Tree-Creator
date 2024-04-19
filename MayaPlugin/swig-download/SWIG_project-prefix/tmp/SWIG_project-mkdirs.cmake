# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "F:/Study/Homework/HW3/swig"
  "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix/src/SWIG_project-build"
  "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix"
  "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix/tmp"
  "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix/src/SWIG_project-stamp"
  "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix/src"
  "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix/src/SWIG_project-stamp"
)

set(configSubDirs Debug;Release;MinSizeRel;RelWithDebInfo)
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix/src/SWIG_project-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "F:/Study/Homework/HW3/swig-download/SWIG_project-prefix/src/SWIG_project-stamp${cfgdir}") # cfgdir has leading slash
endif()
