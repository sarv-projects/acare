// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "acare_msgs/msg/detail/motion_feedback__rosidl_typesupport_introspection_c.h"
#include "acare_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "acare_msgs/msg/detail/motion_feedback__functions.h"
#include "acare_msgs/msg/detail/motion_feedback__struct.h"


// Include directives for member types
// Member `phase`
// Member `error`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_positions`
// Member `joint_velocities`
// Member `joint_currents`
// Member `temperatures`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  acare_msgs__msg__MotionFeedback__init(message_memory);
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_fini_function(void * message_memory)
{
  acare_msgs__msg__MotionFeedback__fini(message_memory);
}

size_t acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__joint_positions(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_positions(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_positions(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__joint_positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_positions(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__joint_positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_positions(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__joint_positions(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__joint_velocities(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_velocities(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_velocities(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__joint_velocities(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_velocities(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__joint_velocities(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_velocities(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__joint_velocities(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__joint_currents(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_currents(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_currents(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__joint_currents(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_currents(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__joint_currents(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_currents(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__joint_currents(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__temperatures(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__temperatures(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__temperatures(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__temperatures(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__temperatures(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__temperatures(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__temperatures(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__temperatures(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_member_array[11] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "phase",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, phase),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, error),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joint_positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, joint_positions),  // bytes offset in struct
    NULL,  // default value
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__joint_positions,  // size() function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_positions,  // get_const(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_positions,  // get(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__joint_positions,  // fetch(index, &value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__joint_positions,  // assign(index, value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__joint_positions  // resize(index) function pointer
  },
  {
    "joint_velocities",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, joint_velocities),  // bytes offset in struct
    NULL,  // default value
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__joint_velocities,  // size() function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_velocities,  // get_const(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_velocities,  // get(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__joint_velocities,  // fetch(index, &value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__joint_velocities,  // assign(index, value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__joint_velocities  // resize(index) function pointer
  },
  {
    "joint_currents",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, joint_currents),  // bytes offset in struct
    NULL,  // default value
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__joint_currents,  // size() function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__joint_currents,  // get_const(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__joint_currents,  // get(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__joint_currents,  // fetch(index, &value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__joint_currents,  // assign(index, value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__joint_currents  // resize(index) function pointer
  },
  {
    "temperatures",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, temperatures),  // bytes offset in struct
    NULL,  // default value
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__size_function__MotionFeedback__temperatures,  // size() function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_const_function__MotionFeedback__temperatures,  // get_const(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__get_function__MotionFeedback__temperatures,  // get(index) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__fetch_function__MotionFeedback__temperatures,  // fetch(index, &value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__assign_function__MotionFeedback__temperatures,  // assign(index, value) function pointer
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__resize_function__MotionFeedback__temperatures  // resize(index) function pointer
  },
  {
    "gripper_force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, gripper_force),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "imu_roll",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, imu_roll),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "imu_pitch",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, imu_pitch),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "imu_yaw",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__msg__MotionFeedback, imu_yaw),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_members = {
  "acare_msgs__msg",  // message namespace
  "MotionFeedback",  // message name
  11,  // number of fields
  sizeof(acare_msgs__msg__MotionFeedback),
  false,  // has_any_key_member_
  acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_member_array,  // message members
  acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_init_function,  // function to initialize message memory (memory has to be allocated)
  acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_type_support_handle = {
  0,
  &acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__msg__MotionFeedback__get_type_hash,
  &acare_msgs__msg__MotionFeedback__get_type_description,
  &acare_msgs__msg__MotionFeedback__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_acare_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, msg, MotionFeedback)() {
  if (!acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_type_support_handle.typesupport_identifier) {
    acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &acare_msgs__msg__MotionFeedback__rosidl_typesupport_introspection_c__MotionFeedback_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
