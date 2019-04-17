# Tries to find a local version of Python installed
# Andre Anjos - 09.july.2010

# If the user has not opted for something fixed, just get the first one
find_program(PYTHON_EXECUTABLE ${WITH_PYTHON} python DOC "Default python interpreter")

execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; print '%d.%d' % (sys.version_info[0], sys.version_info[1])" OUTPUT_VARIABLE PYTHON_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)
set(PYTHON_VERSION "${PYTHON_VERSION}" CACHE STRING "Python version")

string(REPLACE "." "" PYVER ${PYTHON_VERSION})

execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; print sys.version_info[0]" OUTPUT_VARIABLE PYTHON_MAJOR_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)
set(PYTHON_MAJOR_VERSION "${PYTHON_MAJOR_VERSION}" CACHE STRING "Python major version")

include(FindPackageHandleStandardArgs)

# This function checks for python packages that should be installed before you
# try to compile this project
function(find_python_module module)
	string(TOUPPER ${module} module_upper)
  if(NOT PYTHON_${module_upper})
		if(ARGC GREATER 1 AND ARGV1 STREQUAL "REQUIRED")
      set(PYTHON_${module}_FIND_REQUIRED TRUE)
		endif()
		# A module's location is usually a directory, but for binary modules
		# it's a .so file.
    execute_process(COMMAND "${PYTHON_EXECUTABLE}" "-c"
			"import re, ${module}; print re.compile('/__init__.py.*').sub('',${module}.__file__)"
			RESULT_VARIABLE _${module}_status
			OUTPUT_VARIABLE _${module}_location
			ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)
		if(NOT _${module}_status)
      set(PYTHON_${module_upper} ${_${module}_location} CACHE STRING
				"Location of Python module ${module}")
		endif(NOT _${module}_status)
  endif(NOT PYTHON_${module_upper})
  find_package_handle_standard_args(PYTHON_${module} DEFAULT_MSG PYTHON_${module_upper})
endfunction(find_python_module)

# *************************** READ THIS ***********************************
# IMPORTANT: When you update this file, think about updating both the
# ubuntu/debian control file and our Portfile (OSX installation) so the
# package installations for those systems continue to work properly.
# *************************** READ THIS ***********************************

# Now double-check for all required python modules
find_python_module(setuptools REQUIRED)
find_python_module(argparse REQUIRED)
find_python_module(numpy REQUIRED)
find_python_module(matplotlib REQUIRED)
find_python_module(sqlalchemy REQUIRED)
find_python_module(scipy REQUIRED)
find_python_module(sphinx REQUIRED)
find_python_module(nose REQUIRED)
if(WIN32)
  find_python_module(Image REQUIRED)
else()
  find_python_module(PIL REQUIRED)
endif()

# A trick, to make FindPythonLibs work in the expected way in the presence of
# externally compiled python versions.
get_filename_component(BOB_PYTHON_PREFIX1 ${PYTHON_EXECUTABLE} PATH)
get_filename_component(BOB_PYTHON_PREFIX ${BOB_PYTHON_PREFIX1} PATH)
set(CMAKE_SYSTEM_PREFIX_OLD ${CMAKE_SYSTEM_PREFIX_PATH}) #memorize old path
set(CMAKE_SYSTEM_PREFIX_PATH "${BOB_PYTHON_PREFIX};${CMAKE_SYSTEM_PREFIX_PATH}")
set(Python_ADDITIONAL_VERSIONS ${PYTHON_VERSION})
include(FindPythonLibs)
set(CMAKE_SYSTEM_PREFIX_PATH ${CMAKE_SYSTEM_PREFIX_OLD}) #reset to old path

# This calculates the correct python installation prefix for the current
# interpreter
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; print sys.prefix" OUTPUT_VARIABLE PYTHON_PREFIX OUTPUT_STRIP_TRAILING_WHITESPACE)

# This will calculate the include path for numpy
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print numpy.get_include()" OUTPUT_VARIABLE PYTHON_NUMPY_INCLUDE_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)

# Do not use the include dir path found by FindPythonLibs as it does not
# work properly on OSX (we end up getting the system path if another python
# version is selected). This may cause compilation problems.
set(python_INCLUDE_DIRS "${PYTHON_NUMPY_INCLUDE_DIR};${PYTHON_PREFIX}/include/python${PYTHON_VERSION}" CACHE INTERNAL "incdirs")
get_filename_component(python_LIBRARY_DIRS ${PYTHON_LIBRARY} PATH CACHE)

execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; print '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])" OUTPUT_VARIABLE PYTHON_VERSION_COMPLETE OUTPUT_STRIP_TRAILING_WHITESPACE)

execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print numpy.version.version" OUTPUT_VARIABLE NUMPY_VERSION_COMPLETE OUTPUT_STRIP_TRAILING_WHITESPACE)

if(PYTHON_VERSION_COMPLETE AND NUMPY_VERSION_COMPLETE)
  find_package_message(PYTHON "Found Python ${PYTHON_VERSION_COMPLETE} and NumPy ${NUMPY_VERSION_COMPLETE}: interpreter@${PYTHON_EXECUTABLE}; library@${PYTHON_LIBRARY}; includes@${python_INCLUDE_DIRS}" "[${PYTHON_LIBRARY}][${python_INCLUDE_DIRS}]")
endif()

# Finally, we setup the python installation prefix centrally. This value is
# standardized by Python as defined in http://docs.python.org/install/index.html
set(PYTHON_SITE_PACKAGES "${CMAKE_INSTALL_LIBDIR}/python${PYTHON_VERSION}/site-packages" CACHE
  PATH "Default package installation prefix for Python packages")
