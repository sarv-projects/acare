cmake_minimum_required(VERSION 3.8)
project(urdf_assembly_6dof_moveit_config)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
