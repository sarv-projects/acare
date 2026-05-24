// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/ValidatedIntent.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/validated_intent__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__ValidatedIntent__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x32, 0x64, 0x1a, 0x4f, 0x3d, 0x21, 0xd5, 0x5e,
      0x3f, 0x6f, 0x21, 0x9a, 0x72, 0x46, 0x3c, 0x78,
      0x0d, 0x66, 0x22, 0x24, 0xbc, 0x0a, 0xa2, 0xb5,
      0x2d, 0x99, 0x7e, 0x96, 0xaa, 0x6e, 0x15, 0x4a,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__ValidatedIntent__TYPE_NAME[] = "acare_msgs/msg/ValidatedIntent";

// Define type names, field names, and default values
static char acare_msgs__msg__ValidatedIntent__FIELD_NAME__tool[] = "tool";
static char acare_msgs__msg__ValidatedIntent__FIELD_NAME__action[] = "action";
static char acare_msgs__msg__ValidatedIntent__FIELD_NAME__user_id[] = "user_id";
static char acare_msgs__msg__ValidatedIntent__FIELD_NAME__name[] = "name";
static char acare_msgs__msg__ValidatedIntent__FIELD_NAME__authenticated[] = "authenticated";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__ValidatedIntent__FIELDS[] = {
  {
    {acare_msgs__msg__ValidatedIntent__FIELD_NAME__tool, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ValidatedIntent__FIELD_NAME__action, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ValidatedIntent__FIELD_NAME__user_id, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ValidatedIntent__FIELD_NAME__name, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ValidatedIntent__FIELD_NAME__authenticated, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__msg__ValidatedIntent__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__ValidatedIntent__TYPE_NAME, 30, 30},
      {acare_msgs__msg__ValidatedIntent__FIELDS, 5, 5},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string tool\n"
  "string action\n"
  "string user_id\n"
  "string name\n"
  "bool authenticated";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__ValidatedIntent__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__ValidatedIntent__TYPE_NAME, 30, 30},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 72, 72},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__ValidatedIntent__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__ValidatedIntent__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
