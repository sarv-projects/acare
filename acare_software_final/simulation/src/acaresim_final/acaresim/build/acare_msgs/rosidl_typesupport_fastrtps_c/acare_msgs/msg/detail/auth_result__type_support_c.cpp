// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from acare_msgs:msg/AuthResult.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/auth_result__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "acare_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "acare_msgs/msg/detail/auth_result__struct.h"
#include "acare_msgs/msg/detail/auth_result__functions.h"
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

#include "rosidl_runtime_c/string.h"  // name, role, user_id
#include "rosidl_runtime_c/string_functions.h"  // name, role, user_id

// forward declare type support functions


using _AuthResult__ros_msg_type = acare_msgs__msg__AuthResult;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_serialize_acare_msgs__msg__AuthResult(
  const acare_msgs__msg__AuthResult * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
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

  // Field name: name
  {
    const rosidl_runtime_c__String * str = &ros_message->name;
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

  // Field name: role
  {
    const rosidl_runtime_c__String * str = &ros_message->role;
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

  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: face_verified
  {
    cdr << (ros_message->face_verified ? true : false);
  }

  // Field name: face_confidence
  {
    cdr << ros_message->face_confidence;
  }

  // Field name: voice_confidence
  {
    cdr << ros_message->voice_confidence;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_deserialize_acare_msgs__msg__AuthResult(
  eprosima::fastcdr::Cdr & cdr,
  acare_msgs__msg__AuthResult * ros_message)
{
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

  // Field name: name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->name.data) {
      rosidl_runtime_c__String__init(&ros_message->name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'name'\n");
      return false;
    }
  }

  // Field name: role
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->role.data) {
      rosidl_runtime_c__String__init(&ros_message->role);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->role,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'role'\n");
      return false;
    }
  }

  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: face_verified
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->face_verified = tmp ? true : false;
  }

  // Field name: face_confidence
  {
    cdr >> ros_message->face_confidence;
  }

  // Field name: voice_confidence
  {
    cdr >> ros_message->voice_confidence;
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t get_serialized_size_acare_msgs__msg__AuthResult(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _AuthResult__ros_msg_type * ros_message = static_cast<const _AuthResult__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: user_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->user_id.size + 1);

  // Field name: name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->name.size + 1);

  // Field name: role
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->role.size + 1);

  // Field name: success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: face_verified
  {
    size_t item_size = sizeof(ros_message->face_verified);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: face_confidence
  {
    size_t item_size = sizeof(ros_message->face_confidence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: voice_confidence
  {
    size_t item_size = sizeof(ros_message->voice_confidence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t max_serialized_size_acare_msgs__msg__AuthResult(
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

  // Field name: name
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

  // Field name: role
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

  // Field name: success
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: face_verified
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: face_confidence
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: voice_confidence
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = acare_msgs__msg__AuthResult;
    is_plain =
      (
      offsetof(DataType, voice_confidence) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
bool cdr_serialize_key_acare_msgs__msg__AuthResult(
  const acare_msgs__msg__AuthResult * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
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

  // Field name: name
  {
    const rosidl_runtime_c__String * str = &ros_message->name;
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

  // Field name: role
  {
    const rosidl_runtime_c__String * str = &ros_message->role;
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

  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: face_verified
  {
    cdr << (ros_message->face_verified ? true : false);
  }

  // Field name: face_confidence
  {
    cdr << ros_message->face_confidence;
  }

  // Field name: voice_confidence
  {
    cdr << ros_message->voice_confidence;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t get_serialized_size_key_acare_msgs__msg__AuthResult(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _AuthResult__ros_msg_type * ros_message = static_cast<const _AuthResult__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: user_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->user_id.size + 1);

  // Field name: name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->name.size + 1);

  // Field name: role
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->role.size + 1);

  // Field name: success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: face_verified
  {
    size_t item_size = sizeof(ros_message->face_verified);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: face_confidence
  {
    size_t item_size = sizeof(ros_message->face_confidence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: voice_confidence
  {
    size_t item_size = sizeof(ros_message->voice_confidence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_acare_msgs
size_t max_serialized_size_key_acare_msgs__msg__AuthResult(
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

  // Field name: name
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

  // Field name: role
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

  // Field name: success
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: face_verified
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: face_confidence
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: voice_confidence
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = acare_msgs__msg__AuthResult;
    is_plain =
      (
      offsetof(DataType, voice_confidence) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _AuthResult__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const acare_msgs__msg__AuthResult * ros_message = static_cast<const acare_msgs__msg__AuthResult *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_acare_msgs__msg__AuthResult(ros_message, cdr);
}

static bool _AuthResult__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  acare_msgs__msg__AuthResult * ros_message = static_cast<acare_msgs__msg__AuthResult *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_acare_msgs__msg__AuthResult(cdr, ros_message);
}

static uint32_t _AuthResult__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_acare_msgs__msg__AuthResult(
      untyped_ros_message, 0));
}

static size_t _AuthResult__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_acare_msgs__msg__AuthResult(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_AuthResult = {
  "acare_msgs::msg",
  "AuthResult",
  _AuthResult__cdr_serialize,
  _AuthResult__cdr_deserialize,
  _AuthResult__get_serialized_size,
  _AuthResult__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _AuthResult__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_AuthResult,
  get_message_typesupport_handle_function,
  &acare_msgs__msg__AuthResult__get_type_hash,
  &acare_msgs__msg__AuthResult__get_type_description,
  &acare_msgs__msg__AuthResult__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, msg, AuthResult)() {
  return &_AuthResult__type_support;
}

#if defined(__cplusplus)
}
#endif
