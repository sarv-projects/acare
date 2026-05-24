// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from acare_msgs:msg/StateTransition.idl
// generated code does not contain a copyright notice
#ifndef ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "acare_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "acare_msgs/msg/detail/state_transition__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_serialize_acare_msgs__msg__StateTransition(
  const acare_msgs__msg__StateTransition * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_deserialize_acare_msgs__msg__StateTransition(
  eprosima::fastcdr::Cdr &,
  acare_msgs__msg__StateTransition * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t get_serialized_size_acare_msgs__msg__StateTransition(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t max_serialized_size_acare_msgs__msg__StateTransition(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_serialize_key_acare_msgs__msg__StateTransition(
  const acare_msgs__msg__StateTransition * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t get_serialized_size_key_acare_msgs__msg__StateTransition(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t max_serialized_size_key_acare_msgs__msg__StateTransition(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, msg, StateTransition)();

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
