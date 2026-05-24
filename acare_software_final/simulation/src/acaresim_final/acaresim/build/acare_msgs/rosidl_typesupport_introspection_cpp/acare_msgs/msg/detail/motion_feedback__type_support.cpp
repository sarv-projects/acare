// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "acare_msgs/msg/detail/motion_feedback__functions.h"
#include "acare_msgs/msg/detail/motion_feedback__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace acare_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void MotionFeedback_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) acare_msgs::msg::MotionFeedback(_init);
}

void MotionFeedback_fini_function(void * message_memory)
{
  auto typed_message = static_cast<acare_msgs::msg::MotionFeedback *>(message_memory);
  typed_message->~MotionFeedback();
}

size_t size_function__MotionFeedback__joint_positions(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MotionFeedback__joint_positions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__MotionFeedback__joint_positions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotionFeedback__joint_positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__MotionFeedback__joint_positions(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__MotionFeedback__joint_positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__MotionFeedback__joint_positions(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__MotionFeedback__joint_positions(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

size_t size_function__MotionFeedback__joint_velocities(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MotionFeedback__joint_velocities(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__MotionFeedback__joint_velocities(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotionFeedback__joint_velocities(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__MotionFeedback__joint_velocities(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__MotionFeedback__joint_velocities(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__MotionFeedback__joint_velocities(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__MotionFeedback__joint_velocities(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

size_t size_function__MotionFeedback__joint_currents(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MotionFeedback__joint_currents(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__MotionFeedback__joint_currents(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotionFeedback__joint_currents(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__MotionFeedback__joint_currents(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__MotionFeedback__joint_currents(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__MotionFeedback__joint_currents(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__MotionFeedback__joint_currents(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

size_t size_function__MotionFeedback__temperatures(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MotionFeedback__temperatures(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__MotionFeedback__temperatures(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotionFeedback__temperatures(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__MotionFeedback__temperatures(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__MotionFeedback__temperatures(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__MotionFeedback__temperatures(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__MotionFeedback__temperatures(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember MotionFeedback_message_member_array[11] = {
  {
    "success",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, success),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "phase",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, phase),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "error",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, error),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "joint_positions",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, joint_positions),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotionFeedback__joint_positions,  // size() function pointer
    get_const_function__MotionFeedback__joint_positions,  // get_const(index) function pointer
    get_function__MotionFeedback__joint_positions,  // get(index) function pointer
    fetch_function__MotionFeedback__joint_positions,  // fetch(index, &value) function pointer
    assign_function__MotionFeedback__joint_positions,  // assign(index, value) function pointer
    resize_function__MotionFeedback__joint_positions  // resize(index) function pointer
  },
  {
    "joint_velocities",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, joint_velocities),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotionFeedback__joint_velocities,  // size() function pointer
    get_const_function__MotionFeedback__joint_velocities,  // get_const(index) function pointer
    get_function__MotionFeedback__joint_velocities,  // get(index) function pointer
    fetch_function__MotionFeedback__joint_velocities,  // fetch(index, &value) function pointer
    assign_function__MotionFeedback__joint_velocities,  // assign(index, value) function pointer
    resize_function__MotionFeedback__joint_velocities  // resize(index) function pointer
  },
  {
    "joint_currents",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, joint_currents),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotionFeedback__joint_currents,  // size() function pointer
    get_const_function__MotionFeedback__joint_currents,  // get_const(index) function pointer
    get_function__MotionFeedback__joint_currents,  // get(index) function pointer
    fetch_function__MotionFeedback__joint_currents,  // fetch(index, &value) function pointer
    assign_function__MotionFeedback__joint_currents,  // assign(index, value) function pointer
    resize_function__MotionFeedback__joint_currents  // resize(index) function pointer
  },
  {
    "temperatures",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, temperatures),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotionFeedback__temperatures,  // size() function pointer
    get_const_function__MotionFeedback__temperatures,  // get_const(index) function pointer
    get_function__MotionFeedback__temperatures,  // get(index) function pointer
    fetch_function__MotionFeedback__temperatures,  // fetch(index, &value) function pointer
    assign_function__MotionFeedback__temperatures,  // assign(index, value) function pointer
    resize_function__MotionFeedback__temperatures  // resize(index) function pointer
  },
  {
    "gripper_force",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, gripper_force),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "imu_roll",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, imu_roll),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "imu_pitch",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, imu_pitch),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "imu_yaw",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::MotionFeedback, imu_yaw),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers MotionFeedback_message_members = {
  "acare_msgs::msg",  // message namespace
  "MotionFeedback",  // message name
  11,  // number of fields
  sizeof(acare_msgs::msg::MotionFeedback),
  false,  // has_any_key_member_
  MotionFeedback_message_member_array,  // message members
  MotionFeedback_init_function,  // function to initialize message memory (memory has to be allocated)
  MotionFeedback_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t MotionFeedback_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &MotionFeedback_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__msg__MotionFeedback__get_type_hash,
  &acare_msgs__msg__MotionFeedback__get_type_description,
  &acare_msgs__msg__MotionFeedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace acare_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<acare_msgs::msg::MotionFeedback>()
{
  return &::acare_msgs::msg::rosidl_typesupport_introspection_cpp::MotionFeedback_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, acare_msgs, msg, MotionFeedback)() {
  return &::acare_msgs::msg::rosidl_typesupport_introspection_cpp::MotionFeedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
