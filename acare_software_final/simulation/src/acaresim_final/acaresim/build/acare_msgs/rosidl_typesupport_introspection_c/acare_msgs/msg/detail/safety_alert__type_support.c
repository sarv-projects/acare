// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from acare_msgs:msg/SafetyAlert.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "acare_msgs/msg/detail/safety_alert__rosidl_typesupport_introspection_c.h"
#include "acare_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "acare_msgs/msg/detail/safety_alert__functions.h"
#include "acare_msgs/msg/detail/safety_alert__struct.h"


// Include directives for member types
// Member `severity`
// Member `reason`
// Member `source`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  acare_msgs__msg__SafetyAlert__init(message_memory);
}

void acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_fini_function(void * message_memory)
{
  acare_msgs__msg__SafetyAlert__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_member_array[3] = {
  {
    "severity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__SafetyAlert, severity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reason",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__SafetyAlert, reason),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "source",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__SafetyAlert, source),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_members = {
  "acare_msgs__msg",  // message namespace
  "SafetyAlert",  // message name
  3,  // number of fields
  sizeof(acare_msgs__msg__SafetyAlert),
  false,  // has_any_key_member_
  acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_member_array,  // message members
  acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_init_function,  // function to initialize message memory (memory has to be allocated)
  acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_type_support_handle = {
  0,
  &acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__msg__SafetyAlert__get_type_hash,
  &acare_msgs__msg__SafetyAlert__get_type_description,
  &acare_msgs__msg__SafetyAlert__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_acare_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, msg, SafetyAlert)() {
  if (!acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_type_support_handle.typesupport_identifier) {
    acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &acare_msgs__msg__SafetyAlert__rosidl_typesupport_introspection_c__SafetyAlert_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
