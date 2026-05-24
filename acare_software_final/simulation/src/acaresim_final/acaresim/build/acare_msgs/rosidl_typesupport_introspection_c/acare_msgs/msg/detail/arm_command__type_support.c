// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from acare_msgs:msg/ArmCommand.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "acare_msgs/msg/detail/arm_command__rosidl_typesupport_introspection_c.h"
#include "acare_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "acare_msgs/msg/detail/arm_command__functions.h"
#include "acare_msgs/msg/detail/arm_command__struct.h"


// Include directives for member types
// Member `command`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_angles`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  acare_msgs__msg__ArmCommand__init(message_memory);
}

void acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_fini_function(void * message_memory)
{
  acare_msgs__msg__ArmCommand__fini(message_memory);
}

size_t acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__size_function__ArmCommand__joint_angles(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__get_const_function__ArmCommand__joint_angles(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__get_function__ArmCommand__joint_angles(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__fetch_function__ArmCommand__joint_angles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__get_const_function__ArmCommand__joint_angles(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__assign_function__ArmCommand__joint_angles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__get_function__ArmCommand__joint_angles(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__resize_function__ArmCommand__joint_angles(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_member_array[5] = {
  {
    "command",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__ArmCommand, command),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joint_angles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__ArmCommand, joint_angles),  // bytes offset in struct
    NULL,  // default value
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__size_function__ArmCommand__joint_angles,  // size() function pointer
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__get_const_function__ArmCommand__joint_angles,  // get_const(index) function pointer
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__get_function__ArmCommand__joint_angles,  // get(index) function pointer
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__fetch_function__ArmCommand__joint_angles,  // fetch(index, &value) function pointer
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__assign_function__ArmCommand__joint_angles,  // assign(index, value) function pointer
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__resize_function__ArmCommand__joint_angles  // resize(index) function pointer
  },
  {
    "velocity_scale",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__ArmCommand, velocity_scale),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "accel_limit",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__ArmCommand, accel_limit),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "blocking",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__ArmCommand, blocking),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_members = {
  "acare_msgs__msg",  // message namespace
  "ArmCommand",  // message name
  5,  // number of fields
  sizeof(acare_msgs__msg__ArmCommand),
  false,  // has_any_key_member_
  acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_member_array,  // message members
  acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_init_function,  // function to initialize message memory (memory has to be allocated)
  acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_type_support_handle = {
  0,
  &acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__msg__ArmCommand__get_type_hash,
  &acare_msgs__msg__ArmCommand__get_type_description,
  &acare_msgs__msg__ArmCommand__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_acare_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, msg, ArmCommand)() {
  if (!acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_type_support_handle.typesupport_identifier) {
    acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &acare_msgs__msg__ArmCommand__rosidl_typesupport_introspection_c__ArmCommand_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
