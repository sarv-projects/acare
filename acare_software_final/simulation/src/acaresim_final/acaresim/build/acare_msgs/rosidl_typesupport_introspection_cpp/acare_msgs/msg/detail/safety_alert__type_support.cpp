// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from acare_msgs:msg/SafetyAlert.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "acare_msgs/msg/detail/safety_alert__functions.h"
#include "acare_msgs/msg/detail/safety_alert__struct.hpp"
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

void SafetyAlert_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) acare_msgs::msg::SafetyAlert(_init);
}

void SafetyAlert_fini_function(void * message_memory)
{
  auto typed_message = static_cast<acare_msgs::msg::SafetyAlert *>(message_memory);
  typed_message->~SafetyAlert();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember SafetyAlert_message_member_array[3] = {
  {
    "severity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::SafetyAlert, severity),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "reason",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::SafetyAlert, reason),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "source",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs::msg::SafetyAlert, source),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers SafetyAlert_message_members = {
  "acare_msgs::msg",  // message namespace
  "SafetyAlert",  // message name
  3,  // number of fields
  sizeof(acare_msgs::msg::SafetyAlert),
  false,  // has_any_key_member_
  SafetyAlert_message_member_array,  // message members
  SafetyAlert_init_function,  // function to initialize message memory (memory has to be allocated)
  SafetyAlert_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t SafetyAlert_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &SafetyAlert_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__msg__SafetyAlert__get_type_hash,
  &acare_msgs__msg__SafetyAlert__get_type_description,
  &acare_msgs__msg__SafetyAlert__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace acare_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<acare_msgs::msg::SafetyAlert>()
{
  return &::acare_msgs::msg::rosidl_typesupport_introspection_cpp::SafetyAlert_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, acare_msgs, msg, SafetyAlert)() {
  return &::acare_msgs::msg::rosidl_typesupport_introspection_cpp::SafetyAlert_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
