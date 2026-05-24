// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/GripperCommand.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/gripper_command__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__GripperCommand__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x7a, 0x47, 0x36, 0x5f, 0x11, 0xf3, 0x43, 0x2d,
      0xe3, 0x89, 0xe8, 0x2a, 0xbd, 0xb4, 0xb5, 0xee,
      0xc7, 0xeb, 0xa1, 0x75, 0x60, 0x77, 0x10, 0xa7,
      0x47, 0xfe, 0x0d, 0xea, 0xe0, 0x40, 0x40, 0xc6,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__GripperCommand__TYPE_NAME[] = "acare_msgs/msg/GripperCommand";

// Define type names, field names, and default values
static char acare_msgs__msg__GripperCommand__FIELD_NAME__command[] = "command";
static char acare_msgs__msg__GripperCommand__FIELD_NAME__force_target[] = "force_target";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__GripperCommand__FIELDS[] = {
  {
    {acare_msgs__msg__GripperCommand__FIELD_NAME__command, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__GripperCommand__FIELD_NAME__force_target, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__msg__GripperCommand__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__GripperCommand__TYPE_NAME, 29, 29},
      {acare_msgs__msg__GripperCommand__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string command\n"
  "float32 force_target";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__GripperCommand__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__GripperCommand__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 36, 36},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__GripperCommand__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__GripperCommand__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
