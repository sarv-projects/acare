// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/intent__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__Intent__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x1b, 0x78, 0x5a, 0xae, 0xd7, 0x2d, 0x98, 0x95,
      0x69, 0xbd, 0x88, 0xcf, 0x0e, 0x83, 0x67, 0x6d,
      0x3c, 0x08, 0xb5, 0x1b, 0x9c, 0xd5, 0xc3, 0xf6,
      0xee, 0x27, 0x0b, 0xc5, 0x57, 0x87, 0xf4, 0xca,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__Intent__TYPE_NAME[] = "acare_msgs/msg/Intent";

// Define type names, field names, and default values
static char acare_msgs__msg__Intent__FIELD_NAME__tool[] = "tool";
static char acare_msgs__msg__Intent__FIELD_NAME__action[] = "action";
static char acare_msgs__msg__Intent__FIELD_NAME__destination[] = "destination";
static char acare_msgs__msg__Intent__FIELD_NAME__confidence[] = "confidence";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__Intent__FIELDS[] = {
  {
    {acare_msgs__msg__Intent__FIELD_NAME__tool, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__Intent__FIELD_NAME__action, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__Intent__FIELD_NAME__destination, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__Intent__FIELD_NAME__confidence, 10, 10},
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
acare_msgs__msg__Intent__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__Intent__TYPE_NAME, 21, 21},
      {acare_msgs__msg__Intent__FIELDS, 4, 4},
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
  "string destination\n"
  "float32 confidence";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__Intent__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__Intent__TYPE_NAME, 21, 21},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 64, 64},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__Intent__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__Intent__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
