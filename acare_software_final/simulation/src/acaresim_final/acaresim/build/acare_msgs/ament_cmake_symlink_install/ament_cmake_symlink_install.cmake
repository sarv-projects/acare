# generated from
# ament_cmake_core/cmake/symlink_install/ament_cmake_symlink_install.cmake.in

# create empty symlink install manifest before starting install step
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/symlink_install_manifest.txt")

#
# Reimplement CMake install(DIRECTORY) command to use symlinks instead of
# copying resources.
#
# :param cmake_current_source_dir: The CMAKE_CURRENT_SOURCE_DIR when install
#   was invoked
# :type cmake_current_source_dir: string
# :param ARGN: the same arguments as the CMake install command.
# :type ARGN: various
#
function(ament_cmake_symlink_install_directory cmake_current_source_dir)
  cmake_parse_arguments(ARG "OPTIONAL" "DESTINATION" "DIRECTORY;PATTERN;PATTERN_EXCLUDE" ${ARGN})
  if(ARG_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "ament_cmake_symlink_install_directory() called with "
      "unused/unsupported arguments: ${ARG_UNPARSED_ARGUMENTS}")
  endif()

  # make destination absolute path and ensure that it exists
  if(NOT IS_ABSOLUTE "${ARG_DESTINATION}")
    set(ARG_DESTINATION "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/install/acare_msgs/${ARG_DESTINATION}")
  endif()
  if(NOT EXISTS "${ARG_DESTINATION}")
    file(MAKE_DIRECTORY "${ARG_DESTINATION}")
  endif()

  # default pattern to include
  if(NOT ARG_PATTERN)
    set(ARG_PATTERN "*")
  endif()

  # iterate over directories
  foreach(dir ${ARG_DIRECTORY})
    # make dir an absolute path
    if(NOT IS_ABSOLUTE "${dir}")
      set(dir "${cmake_current_source_dir}/${dir}")
    endif()

    if(EXISTS "${dir}")
      # if directory has no trailing slash
      # append folder name to destination
      set(destination "${ARG_DESTINATION}")
      string(LENGTH "${dir}" length)
      math(EXPR offset "${length} - 1")
      string(SUBSTRING "${dir}" ${offset} 1 dir_last_char)
      if(NOT dir_last_char STREQUAL "/")
        get_filename_component(destination_name "${dir}" NAME)
        set(destination "${destination}/${destination_name}")
      else()
        # remove trailing slash
        string(SUBSTRING "${dir}" 0 ${offset} dir)
      endif()
      
      # Create destination directory.
      # This does *not* solve the problem of empty directories WITHIN the install tree,
      # but does make sure that the top-level directory specified by the caller gets created.
      file(MAKE_DIRECTORY "${destination}")

      # glob recursive files
      set(relative_files "")
      foreach(pattern ${ARG_PATTERN})
        file(
          GLOB_RECURSE
          include_files
          RELATIVE "${dir}"
          "${dir}/${pattern}"
        )
        if(NOT include_files STREQUAL "")
          list(APPEND relative_files ${include_files})
        endif()
      endforeach()
      foreach(pattern ${ARG_PATTERN_EXCLUDE})
        file(
          GLOB_RECURSE
          exclude_files
          RELATIVE "${dir}"
          "${dir}/${pattern}"
        )
        if(NOT exclude_files STREQUAL "")
          list(REMOVE_ITEM relative_files ${exclude_files})
        endif()
      endforeach()
      list(SORT relative_files)

      foreach(relative_file ${relative_files})
        set(absolute_file "${dir}/${relative_file}")
        # determine link name for file including destination path
        set(symlink "${destination}/${relative_file}")

        # ensure that destination exists
        get_filename_component(symlink_dir "${symlink}" PATH)
        if(NOT EXISTS "${symlink_dir}")
          file(MAKE_DIRECTORY "${symlink_dir}")
        endif()

        _ament_cmake_symlink_install_create_symlink("${absolute_file}" "${symlink}")
      endforeach()
    else()
      if(NOT ARG_OPTIONAL)
        message(FATAL_ERROR
          "ament_cmake_symlink_install_directory() can't find '${dir}'")
      endif()
    endif()
  endforeach()
endfunction()

#
# Reimplement CMake install(FILES) command to use symlinks instead of copying
# resources.
#
# :param cmake_current_source_dir: The CMAKE_CURRENT_SOURCE_DIR when install
#   was invoked
# :type cmake_current_source_dir: string
# :param ARGN: the same arguments as the CMake install command.
# :type ARGN: various
#
function(ament_cmake_symlink_install_files cmake_current_source_dir)
  cmake_parse_arguments(ARG "OPTIONAL" "DESTINATION;RENAME" "FILES" ${ARGN})
  if(ARG_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "ament_cmake_symlink_install_files() called with "
      "unused/unsupported arguments: ${ARG_UNPARSED_ARGUMENTS}")
  endif()

  # make destination an absolute path and ensure that it exists
  if(NOT IS_ABSOLUTE "${ARG_DESTINATION}")
    set(ARG_DESTINATION "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/install/acare_msgs/${ARG_DESTINATION}")
  endif()
  if(NOT EXISTS "${ARG_DESTINATION}")
    file(MAKE_DIRECTORY "${ARG_DESTINATION}")
  endif()

  if(ARG_RENAME)
    list(LENGTH ARG_FILES file_count)
    if(NOT file_count EQUAL 1)
    message(FATAL_ERROR "ament_cmake_symlink_install_files() called with "
      "RENAME argument but not with a single file")
    endif()
  endif()

  # iterate over files
  foreach(file ${ARG_FILES})
    # make file an absolute path
    if(NOT IS_ABSOLUTE "${file}")
      set(file "${cmake_current_source_dir}/${file}")
    endif()

    if(EXISTS "${file}")
      # determine link name for file including destination path
      get_filename_component(filename "${file}" NAME)
      if(NOT ARG_RENAME)
        set(symlink "${ARG_DESTINATION}/${filename}")
      else()
        set(symlink "${ARG_DESTINATION}/${ARG_RENAME}")
      endif()
      _ament_cmake_symlink_install_create_symlink("${file}" "${symlink}")
    else()
      if(NOT ARG_OPTIONAL)
        message(FATAL_ERROR
          "ament_cmake_symlink_install_files() can't find '${file}'")
      endif()
    endif()
  endforeach()
endfunction()

#
# Reimplement CMake install(PROGRAMS) command to use symlinks instead of copying
# resources.
#
# :param cmake_current_source_dir: The CMAKE_CURRENT_SOURCE_DIR when install
#   was invoked
# :type cmake_current_source_dir: string
# :param ARGN: the same arguments as the CMake install command.
# :type ARGN: various
#
function(ament_cmake_symlink_install_programs cmake_current_source_dir)
  cmake_parse_arguments(ARG "OPTIONAL" "DESTINATION" "PROGRAMS" ${ARGN})
  if(ARG_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "ament_cmake_symlink_install_programs() called with "
      "unused/unsupported arguments: ${ARG_UNPARSED_ARGUMENTS}")
  endif()

  # make destination an absolute path and ensure that it exists
  if(NOT IS_ABSOLUTE "${ARG_DESTINATION}")
    set(ARG_DESTINATION "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/install/acare_msgs/${ARG_DESTINATION}")
  endif()
  if(NOT EXISTS "${ARG_DESTINATION}")
    file(MAKE_DIRECTORY "${ARG_DESTINATION}")
  endif()

  # iterate over programs
  foreach(file ${ARG_PROGRAMS})
    # make file an absolute path
    if(NOT IS_ABSOLUTE "${file}")
      set(file "${cmake_current_source_dir}/${file}")
    endif()

    if(EXISTS "${file}")
      # determine link name for file including destination path
      get_filename_component(filename "${file}" NAME)
      set(symlink "${ARG_DESTINATION}/${filename}")
      _ament_cmake_symlink_install_create_symlink("${file}" "${symlink}")
    else()
      if(NOT ARG_OPTIONAL)
        message(FATAL_ERROR
          "ament_cmake_symlink_install_programs() can't find '${file}'")
      endif()
    endif()
  endforeach()
endfunction()

#
# Reimplement CMake install(TARGETS) command to use symlinks instead of copying
# resources.
#
# :param TARGET_FILES: the absolute files, replacing the name of targets passed
#   in as TARGETS
# :type TARGET_FILES: list of files
# :param ARGN: the same arguments as the CMake install command except that
#   keywords identifying the kind of type and the DESTINATION keyword must be
#   joined with an underscore, e.g. ARCHIVE_DESTINATION.
# :type ARGN: various
#
function(ament_cmake_symlink_install_targets)
  cmake_parse_arguments(ARG "OPTIONAL" "ARCHIVE_DESTINATION;DESTINATION;LIBRARY_DESTINATION;RUNTIME_DESTINATION"
    "TARGETS;TARGET_FILES" ${ARGN})
  if(ARG_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "ament_cmake_symlink_install_targets() called with "
      "unused/unsupported arguments: ${ARG_UNPARSED_ARGUMENTS}")
  endif()

  # iterate over target files
  foreach(file ${ARG_TARGET_FILES})
    if(NOT IS_ABSOLUTE "${file}")
      message(FATAL_ERROR "ament_cmake_symlink_install_targets() target file "
        "'${file}' must be an absolute path")
    endif()

    # determine destination of file based on extension
    set(destination "")
    get_filename_component(fileext "${file}" EXT)
    if(fileext STREQUAL ".a" OR fileext STREQUAL ".lib")
      set(destination "${ARG_ARCHIVE_DESTINATION}")
    elseif(fileext STREQUAL ".dylib" OR fileext MATCHES "\\.so(\\.[0-9]+)?(\\.[0-9]+)?(\\.[0-9]+)?$")
      set(destination "${ARG_LIBRARY_DESTINATION}")
    elseif(fileext STREQUAL "" OR fileext STREQUAL ".dll" OR fileext STREQUAL ".exe")
      set(destination "${ARG_RUNTIME_DESTINATION}")
    endif()
    if(destination STREQUAL "")
      set(destination "${ARG_DESTINATION}")
    endif()

    # make destination an absolute path and ensure that it exists
    if(NOT IS_ABSOLUTE "${destination}")
      set(destination "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/install/acare_msgs/${destination}")
    endif()
    if(NOT EXISTS "${destination}")
      file(MAKE_DIRECTORY "${destination}")
    endif()

    if(EXISTS "${file}")
      # determine link name for file including destination path
      get_filename_component(filename "${file}" NAME)
      set(symlink "${destination}/${filename}")
      _ament_cmake_symlink_install_create_symlink("${file}" "${symlink}")
    else()
      if(NOT ARG_OPTIONAL)
        message(FATAL_ERROR
          "ament_cmake_symlink_install_targets() can't find '${file}'")
      endif()
    endif()
  endforeach()
endfunction()

function(_ament_cmake_symlink_install_create_symlink absolute_file symlink)
  # register symlink for being removed during install step
  file(APPEND "${CMAKE_CURRENT_BINARY_DIR}/symlink_install_manifest.txt"
    "${symlink}\n")

  # avoid any work if correct symlink is already in place
  if(EXISTS "${symlink}" AND IS_SYMLINK "${symlink}")
    get_filename_component(destination "${symlink}" REALPATH)
    get_filename_component(real_absolute_file "${absolute_file}" REALPATH)
    if(destination STREQUAL real_absolute_file)
      message(STATUS "Up-to-date symlink: ${symlink}")
      return()
    endif()
  endif()

  message(STATUS "Symlinking: ${symlink}")
  if(EXISTS "${symlink}" OR IS_SYMLINK "${symlink}")
    file(REMOVE "${symlink}")
  endif()

  execute_process(
    COMMAND "/usr/bin/cmake" "-E" "create_symlink"
      "${absolute_file}"
      "${symlink}"
  )
  # the CMake command does not provide a return code so check manually
  if(NOT EXISTS "${symlink}" OR NOT IS_SYMLINK "${symlink}")
    get_filename_component(destination "${symlink}" REALPATH)
    message(FATAL_ERROR
      "Could not create symlink '${symlink}' pointing to '${absolute_file}'")
  endif()
endfunction()

# end of template

message(STATUS "Execute custom install script")

# begin of custom install code

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/rosidl_interfaces/acare_msgs" "DESTINATION" "share/ament_index/resource_index/rosidl_interfaces")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/rosidl_interfaces/acare_msgs" "DESTINATION" "share/ament_index/resource_index/rosidl_interfaces")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/RobotState.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/RobotState.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/StateTransition.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/StateTransition.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/Intent.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/Intent.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/ValidatedIntent.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/ValidatedIntent.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/SafetyAlert.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/SafetyAlert.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/HandStatus.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/HandStatus.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/AuthResult.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/AuthResult.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/VisionResult.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/VisionResult.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/VisionSearchRequest.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/VisionSearchRequest.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/ArmCommand.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/ArmCommand.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/GripperCommand.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/GripperCommand.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/MotionFeedback.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/MotionFeedback.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/LogEvent.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/LogEvent.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/EmergencySignal.json" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/msg/EmergencySignal.json" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/srv/EnrolStaff.json" "DESTINATION" "share/acare_msgs/srv")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_type_description/acare_msgs/srv/EnrolStaff.json" "DESTINATION" "share/acare_msgs/srv")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_c/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.h")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_c/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.h")

# install(FILES "/opt/ros/jazzy/lib/python3.12/site-packages/ament_package/template/environment_hook/library_path.sh" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/opt/ros/jazzy/lib/python3.12/site-packages/ament_package/template/environment_hook/library_path.sh" "DESTINATION" "share/acare_msgs/environment")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/library_path.dsv" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/library_path.dsv" "DESTINATION" "share/acare_msgs/environment")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_fastrtps_c/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN_EXCLUDE" "*.cpp")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_fastrtps_c/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN_EXCLUDE" "*.cpp")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_introspection_c/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.h")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_introspection_c/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.h")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_cpp/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.hpp")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_cpp/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.hpp")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_fastrtps_cpp/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN_EXCLUDE" "*.cpp")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_fastrtps_cpp/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN_EXCLUDE" "*.cpp")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_introspection_cpp/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.hpp")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_typesupport_introspection_cpp/acare_msgs/" "DESTINATION" "include/acare_msgs/acare_msgs" "PATTERN" "*.hpp")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/pythonpath.sh" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/pythonpath.sh" "DESTINATION" "share/acare_msgs/environment")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/pythonpath.dsv" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/pythonpath.dsv" "DESTINATION" "share/acare_msgs/environment")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_python/acare_msgs/acare_msgs.egg-info/" "DESTINATION" "lib/python3.12/site-packages/acare_msgs-0.0.0-py3.12.egg-info")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_python/acare_msgs/acare_msgs.egg-info/" "DESTINATION" "lib/python3.12/site-packages/acare_msgs-0.0.0-py3.12.egg-info")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_py/acare_msgs/" "DESTINATION" "lib/python3.12/site-packages/acare_msgs" "PATTERN_EXCLUDE" "*.pyc" "PATTERN_EXCLUDE" "__pycache__")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_py/acare_msgs/" "DESTINATION" "lib/python3.12/site-packages/acare_msgs" "PATTERN_EXCLUDE" "*.pyc" "PATTERN_EXCLUDE" "__pycache__")

# install("TARGETS" "acare_msgs_s__rosidl_typesupport_fastrtps_c" "DESTINATION" "lib/python3.12/site-packages/acare_msgs")
include("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_symlink_install_targets_0_${CMAKE_INSTALL_CONFIG_NAME}.cmake")

# install("TARGETS" "acare_msgs_s__rosidl_typesupport_introspection_c" "DESTINATION" "lib/python3.12/site-packages/acare_msgs")
include("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_symlink_install_targets_1_${CMAKE_INSTALL_CONFIG_NAME}.cmake")

# install("TARGETS" "acare_msgs_s__rosidl_typesupport_c" "DESTINATION" "lib/python3.12/site-packages/acare_msgs")
include("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_symlink_install_targets_2_${CMAKE_INSTALL_CONFIG_NAME}.cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/rust_packages/acare_msgs" "DESTINATION" "share/ament_index/resource_index/rust_packages")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/rust_packages/acare_msgs" "DESTINATION" "share/ament_index/resource_index/rust_packages")

# install(DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_rs/acare_msgs/rust" "DESTINATION" "share/acare_msgs")
ament_cmake_symlink_install_directory("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" DIRECTORY "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_generator_rs/acare_msgs/rust" "DESTINATION" "share/acare_msgs")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/RobotState.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/RobotState.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/StateTransition.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/StateTransition.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/Intent.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/Intent.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/ValidatedIntent.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/ValidatedIntent.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/SafetyAlert.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/SafetyAlert.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/HandStatus.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/HandStatus.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/AuthResult.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/AuthResult.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/VisionResult.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/VisionResult.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/VisionSearchRequest.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/VisionSearchRequest.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/ArmCommand.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/ArmCommand.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/GripperCommand.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/GripperCommand.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/MotionFeedback.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/MotionFeedback.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/LogEvent.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/LogEvent.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/EmergencySignal.idl" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/msg/EmergencySignal.idl" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/srv/EnrolStaff.idl" "DESTINATION" "share/acare_msgs/srv")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_adapter/acare_msgs/srv/EnrolStaff.idl" "DESTINATION" "share/acare_msgs/srv")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/RobotState.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/RobotState.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/StateTransition.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/StateTransition.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/Intent.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/Intent.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/ValidatedIntent.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/ValidatedIntent.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/SafetyAlert.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/SafetyAlert.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/HandStatus.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/HandStatus.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/AuthResult.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/AuthResult.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/VisionResult.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/VisionResult.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/VisionSearchRequest.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/VisionSearchRequest.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/ArmCommand.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/ArmCommand.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/GripperCommand.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/GripperCommand.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/MotionFeedback.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/MotionFeedback.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/LogEvent.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/LogEvent.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/EmergencySignal.msg" "DESTINATION" "share/acare_msgs/msg")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/msg/EmergencySignal.msg" "DESTINATION" "share/acare_msgs/msg")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/srv/EnrolStaff.srv" "DESTINATION" "share/acare_msgs/srv")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/srv/EnrolStaff.srv" "DESTINATION" "share/acare_msgs/srv")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/acare_msgs" "DESTINATION" "share/ament_index/resource_index/package_run_dependencies")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/acare_msgs" "DESTINATION" "share/ament_index/resource_index/package_run_dependencies")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/acare_msgs" "DESTINATION" "share/ament_index/resource_index/parent_prefix_path")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/acare_msgs" "DESTINATION" "share/ament_index/resource_index/parent_prefix_path")

# install(FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh" "DESTINATION" "share/acare_msgs/environment")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/ament_prefix_path.dsv" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/ament_prefix_path.dsv" "DESTINATION" "share/acare_msgs/environment")

# install(FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh" "DESTINATION" "share/acare_msgs/environment")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/path.dsv" "DESTINATION" "share/acare_msgs/environment")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/path.dsv" "DESTINATION" "share/acare_msgs/environment")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.bash" "DESTINATION" "share/acare_msgs")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.bash" "DESTINATION" "share/acare_msgs")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.sh" "DESTINATION" "share/acare_msgs")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.sh" "DESTINATION" "share/acare_msgs")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.zsh" "DESTINATION" "share/acare_msgs")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.zsh" "DESTINATION" "share/acare_msgs")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.dsv" "DESTINATION" "share/acare_msgs")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/local_setup.dsv" "DESTINATION" "share/acare_msgs")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/package.dsv" "DESTINATION" "share/acare_msgs")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_environment_hooks/package.dsv" "DESTINATION" "share/acare_msgs")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/packages/acare_msgs" "DESTINATION" "share/ament_index/resource_index/packages")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_index/share/ament_index/resource_index/packages/acare_msgs" "DESTINATION" "share/ament_index/resource_index/packages")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_cmake/rosidl_cmake-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_cmake/rosidl_cmake-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_dependencies/ament_cmake_export_dependencies-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_dependencies/ament_cmake_export_dependencies-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_include_directories/ament_cmake_export_include_directories-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_include_directories/ament_cmake_export_include_directories-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_libraries/ament_cmake_export_libraries-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_libraries/ament_cmake_export_libraries-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_targets/ament_cmake_export_targets-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_export_targets/ament_cmake_export_targets-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_cmake/rosidl_cmake_export_typesupport_targets-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_cmake/rosidl_cmake_export_typesupport_targets-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_cmake/rosidl_cmake_export_typesupport_libraries-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/rosidl_cmake/rosidl_cmake_export_typesupport_libraries-extras.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_core/acare_msgsConfig.cmake" "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_core/acare_msgsConfig-version.cmake" "DESTINATION" "share/acare_msgs/cmake")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_core/acare_msgsConfig.cmake" "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/build/acare_msgs/ament_cmake_core/acare_msgsConfig-version.cmake" "DESTINATION" "share/acare_msgs/cmake")

# install(FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/package.xml" "DESTINATION" "share/acare_msgs")
ament_cmake_symlink_install_files("/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs" FILES "/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/src/acare_msgs/package.xml" "DESTINATION" "share/acare_msgs")
