// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/robot_state__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__RobotState__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x3a, 0x85, 0xc5, 0x9a, 0xd9, 0x11, 0xf2, 0xec,
      0xeb, 0x3f, 0x27, 0xb1, 0xf1, 0xa9, 0x92, 0xd9,
      0xae, 0x5a, 0x71, 0xbf, 0xe0, 0x0d, 0xdf, 0x6a,
      0x73, 0xbb, 0xaa, 0x92, 0xf0, 0x51, 0xa9, 0xb1,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__RobotState__TYPE_NAME[] = "acare_msgs/msg/RobotState";

// Define type names, field names, and default values
static char acare_msgs__msg__RobotState__FIELD_NAME__state[] = "state";
static char acare_msgs__msg__RobotState__FIELD_NAME__active_user_id[] = "active_user_id";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__RobotState__FIELDS[] = {
  {
    {acare_msgs__msg__RobotState__FIELD_NAME__state, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__RobotState__FIELD_NAME__active_user_id, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__msg__RobotState__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__RobotState__TYPE_NAME, 25, 25},
      {acare_msgs__msg__RobotState__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string state\n"
  "string active_user_id";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__RobotState__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__RobotState__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 35, 35},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__RobotState__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__RobotState__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
