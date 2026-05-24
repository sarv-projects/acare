// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/LogEvent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/log_event.h"


#ifndef ACARE_MSGS__MSG__DETAIL__LOG_EVENT__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__LOG_EVENT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'event_type'
// Member 'user_id'
// Member 'tool'
// Member 'state'
// Member 'description'
// Member 'safety_severity'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/LogEvent in the package acare_msgs.
typedef struct acare_msgs__msg__LogEvent
{
  rosidl_runtime_c__String event_type;
  rosidl_runtime_c__String user_id;
  rosidl_runtime_c__String tool;
  rosidl_runtime_c__String state;
  rosidl_runtime_c__String description;
  int64_t timestamp;
  int64_t voice_e2e_ms;
  int64_t vision_search_ms;
  int64_t motion_ms;
  int64_t total_task_ms;
  rosidl_runtime_c__String safety_severity;
} acare_msgs__msg__LogEvent;

// Struct for a sequence of acare_msgs__msg__LogEvent.
typedef struct acare_msgs__msg__LogEvent__Sequence
{
  acare_msgs__msg__LogEvent * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__LogEvent__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__LOG_EVENT__STRUCT_H_
