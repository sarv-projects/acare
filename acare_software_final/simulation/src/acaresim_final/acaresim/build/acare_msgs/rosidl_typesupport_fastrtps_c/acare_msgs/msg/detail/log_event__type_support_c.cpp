// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from acare_msgs:msg/LogEvent.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/log_event__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "acare_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "acare_msgs/msg/detail/log_event__struct.h"
#include "acare_msgs/msg/detail/log_event__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // description, event_type, safety_severity, state, tool, user_id
#include "rosidl_runtime_c/string_functions.h"  // description, event_type, safety_severity, state, tool, user_id

// forward declare type support functions


using _LogEvent__ros_msg_type = acare_msgs__msg__LogEvent;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_serialize_acare_msgs__msg__LogEvent(
  const acare_msgs__msg__LogEvent * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: event_type
  {
    const rosidl_runtime_c__String * str = &ros_message->event_type;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: user_id
  {
    const rosidl_runtime_c__String * str = &ros_message->user_id;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: tool
  {
    const rosidl_runtime_c__String * str = &ros_message->tool;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: state
  {
    const rosidl_runtime_c__String * str = &ros_message->state;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: description
  {
    const rosidl_runtime_c__String * str = &ros_message->description;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: timestamp
  {
    cdr << ros_message->timestamp;
  }

  // Field name: voice_e2e_ms
  {
    cdr << ros_message->voice_e2e_ms;
  }

  // Field name: vision_search_ms
  {
    cdr << ros_message->vision_search_ms;
  }

  // Field name: motion_ms
  {
    cdr << ros_message->motion_ms;
  }

  // Field name: total_task_ms
  {
    cdr << ros_message->total_task_ms;
  }

  // Field name: safety_severity
  {
    const rosidl_runtime_c__String * str = &ros_message->safety_severity;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_deserialize_acare_msgs__msg__LogEvent(
  eprosima::fastcdr::Cdr & cdr,
  acare_msgs__msg__LogEvent * ros_message)
{
  // Field name: event_type
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->event_type.data) {
      rosidl_runtime_c__String__init(&ros_message->event_type);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->event_type,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'event_type'\n");
      return false;
    }
  }

  // Field name: user_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->user_id.data) {
      rosidl_runtime_c__String__init(&ros_message->user_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->user_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'user_id'\n");
      return false;
    }
  }

  // Field name: tool
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->tool.data) {
      rosidl_runtime_c__String__init(&ros_message->tool);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->tool,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'tool'\n");
      return false;
    }
  }

  // Field name: state
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->state.data) {
      rosidl_runtime_c__String__init(&ros_message->state);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->state,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'state'\n");
      return false;
    }
  }

  // Field name: description
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->description.data) {
      rosidl_runtime_c__String__init(&ros_message->description);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->description,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'description'\n");
      return false;
    }
  }

  // Field name: timestamp
  {
    cdr >> ros_message->timestamp;
  }

  // Field name: voice_e2e_ms
  {
    cdr >> ros_message->voice_e2e_ms;
  }

  // Field name: vision_search_ms
  {
    cdr >> ros_message->vision_search_ms;
  }

  // Field name: motion_ms
  {
    cdr >> ros_message->motion_ms;
  }

  // Field name: total_task_ms
  {
    cdr >> ros_message->total_task_ms;
  }

  // Field name: safety_severity
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->safety_severity.data) {
      rosidl_runtime_c__String__init(&ros_message->safety_severity);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->safety_severity,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'safety_severity'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t get_serialized_size_acare_msgs__msg__LogEvent(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _LogEvent__ros_msg_type * ros_message = static_cast<const _LogEvent__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: event_type
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->event_type.size + 1);

  // Field name: user_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->user_id.size + 1);

  // Field name: tool
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->tool.size + 1);

  // Field name: state
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->state.size + 1);

  // Field name: description
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->description.size + 1);

  // Field name: timestamp
  {
    size_t item_size = sizeof(ros_message->timestamp);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: voice_e2e_ms
  {
    size_t item_size = sizeof(ros_message->voice_e2e_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: vision_search_ms
  {
    size_t item_size = sizeof(ros_message->vision_search_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: motion_ms
  {
    size_t item_size = sizeof(ros_message->motion_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: total_task_ms
  {
    size_t item_size = sizeof(ros_message->total_task_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: safety_severity
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->safety_severity.size + 1);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t max_serialized_size_acare_msgs__msg__LogEvent(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: event_type
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: user_id
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: tool
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: state
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: description
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: timestamp
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: voice_e2e_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: vision_search_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: motion_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: total_task_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: safety_severity
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = acare_msgs__msg__LogEvent;
    is_plain =
      (
      offsetof(DataType, safety_severity) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_serialize_key_acare_msgs__msg__LogEvent(
  const acare_msgs__msg__LogEvent * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: event_type
  {
    const rosidl_runtime_c__String * str = &ros_message->event_type;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: user_id
  {
    const rosidl_runtime_c__String * str = &ros_message->user_id;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: tool
  {
    const rosidl_runtime_c__String * str = &ros_message->tool;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: state
  {
    const rosidl_runtime_c__String * str = &ros_message->state;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: description
  {
    const rosidl_runtime_c__String * str = &ros_message->description;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: timestamp
  {
    cdr << ros_message->timestamp;
  }

  // Field name: voice_e2e_ms
  {
    cdr << ros_message->voice_e2e_ms;
  }

  // Field name: vision_search_ms
  {
    cdr << ros_message->vision_search_ms;
  }

  // Field name: motion_ms
  {
    cdr << ros_message->motion_ms;
  }

  // Field name: total_task_ms
  {
    cdr << ros_message->total_task_ms;
  }

  // Field name: safety_severity
  {
    const rosidl_runtime_c__String * str = &ros_message->safety_severity;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t get_serialized_size_key_acare_msgs__msg__LogEvent(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _LogEvent__ros_msg_type * ros_message = static_cast<const _LogEvent__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: event_type
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->event_type.size + 1);

  // Field name: user_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->user_id.size + 1);

  // Field name: tool
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->tool.size + 1);

  // Field name: state
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->state.size + 1);

  // Field name: description
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->description.size + 1);

  // Field name: timestamp
  {
    size_t item_size = sizeof(ros_message->timestamp);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: voice_e2e_ms
  {
    size_t item_size = sizeof(ros_message->voice_e2e_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: vision_search_ms
  {
    size_t item_size = sizeof(ros_message->vision_search_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: motion_ms
  {
    size_t item_size = sizeof(ros_message->motion_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: total_task_ms
  {
    size_t item_size = sizeof(ros_message->total_task_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: safety_severity
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->safety_severity.size + 1);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t max_serialized_size_key_acare_msgs__msg__LogEvent(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: event_type
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: user_id
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: tool
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: state
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: description
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: timestamp
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: voice_e2e_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: vision_search_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: motion_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: total_task_ms
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: safety_severity
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = acare_msgs__msg__LogEvent;
    is_plain =
      (
      offsetof(DataType, safety_severity) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _LogEvent__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const acare_msgs__msg__LogEvent * ros_message = static_cast<const acare_msgs__msg__LogEvent *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_acare_msgs__msg__LogEvent(ros_message, cdr);
}

static bool _LogEvent__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  acare_msgs__msg__LogEvent * ros_message = static_cast<acare_msgs__msg__LogEvent *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_acare_msgs__msg__LogEvent(cdr, ros_message);
}

static uint32_t _LogEvent__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_acare_msgs__msg__LogEvent(
      untyped_ros_message, 0));
}

static size_t _LogEvent__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_acare_msgs__msg__LogEvent(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_LogEvent = {
  "acare_msgs::msg",
  "LogEvent",
  _LogEvent__cdr_serialize,
  _LogEvent__cdr_deserialize,
  _LogEvent__get_serialized_size,
  _LogEvent__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _LogEvent__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_LogEvent,
  get_message_typesupport_handle_function,
  &acare_msgs__msg__LogEvent__get_type_hash,
  &acare_msgs__msg__LogEvent__get_type_description,
  &acare_msgs__msg__LogEvent__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, msg, LogEvent)() {
  return &_LogEvent__type_support;
}

#if defined(__cplusplus)
}
#endif
