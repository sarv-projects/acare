// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/SafetyAlert.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/safety_alert__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__SafetyAlert__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x36, 0x0c, 0xff, 0x76, 0x52, 0xca, 0x26, 0x5d,
      0xe2, 0x4b, 0xf8, 0x5d, 0x0d, 0x59, 0x0d, 0x96,
      0x65, 0x44, 0x90, 0x08, 0x4c, 0x80, 0x9b, 0x16,
      0x03, 0x68, 0xe1, 0x5d, 0xd2, 0x75, 0xbe, 0xcb,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__SafetyAlert__TYPE_NAME[] = "acare_msgs/msg/SafetyAlert";

// Define type names, field names, and default values
static char acare_msgs__msg__SafetyAlert__FIELD_NAME__severity[] = "severity";
static char acare_msgs__msg__SafetyAlert__FIELD_NAME__reason[] = "reason";
static char acare_msgs__msg__SafetyAlert__FIELD_NAME__source[] = "source";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__SafetyAlert__FIELDS[] = {
  {
    {acare_msgs__msg__SafetyAlert__FIELD_NAME__severity, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__SafetyAlert__FIELD_NAME__reason, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__SafetyAlert__FIELD_NAME__source, 6, 6},
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
acare_msgs__msg__SafetyAlert__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__SafetyAlert__TYPE_NAME, 26, 26},
      {acare_msgs__msg__SafetyAlert__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string severity\n"
  "string reason\n"
  "string source";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__SafetyAlert__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__SafetyAlert__TYPE_NAME, 26, 26},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 44, 44},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__SafetyAlert__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__SafetyAlert__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
