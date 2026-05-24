// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from acare_msgs:msg/ValidatedIntent.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "acare_msgs/msg/detail/validated_intent__struct.h"
#include "acare_msgs/msg/detail/validated_intent__type_support.h"
#include "acare_msgs/msg/detail/validated_intent__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace acare_msgs
{

namespace msg
{

namespace rosidl_typesupport_c
{

typedef struct _ValidatedIntent_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ValidatedIntent_type_support_ids_t;

static const _ValidatedIntent_type_support_ids_t _ValidatedIntent_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ValidatedIntent_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ValidatedIntent_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ValidatedIntent_type_support_symbol_names_t _ValidatedIntent_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, msg, ValidatedIntent)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, msg, ValidatedIntent)),
  }
};

typedef struct _ValidatedIntent_type_support_data_t
{
  void * data[2];
} _ValidatedIntent_type_support_data_t;

static _ValidatedIntent_type_support_data_t _ValidatedIntent_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ValidatedIntent_message_typesupport_map = {
  2,
  "acare_msgs",
  &_ValidatedIntent_message_typesupport_ids.typesupport_identifier[0],
  &_ValidatedIntent_message_typesupport_symbol_names.symbol_name[0],
  &_ValidatedIntent_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ValidatedIntent_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ValidatedIntent_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &acare_msgs__msg__ValidatedIntent__get_type_hash,
  &acare_msgs__msg__ValidatedIntent__get_type_description,
  &acare_msgs__msg__ValidatedIntent__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace msg

}  // namespace acare_msgs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, acare_msgs, msg, ValidatedIntent)() {
  return &::acare_msgs::msg::rosidl_typesupport_c::ValidatedIntent_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
