// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/VisionResult.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/vision_result__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__VisionResult__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xac, 0x89, 0xeb, 0xaa, 0x14, 0x4f, 0xb5, 0x96,
      0xe6, 0x6f, 0x08, 0x89, 0xa4, 0x71, 0x31, 0x1b,
      0xeb, 0x35, 0x61, 0xde, 0x24, 0x5d, 0x22, 0x85,
      0xfa, 0x42, 0x34, 0xae, 0x03, 0x7a, 0x91, 0xb4,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__VisionResult__TYPE_NAME[] = "acare_msgs/msg/VisionResult";

// Define type names, field names, and default values
static char acare_msgs__msg__VisionResult__FIELD_NAME__found[] = "found";
static char acare_msgs__msg__VisionResult__FIELD_NAME__tool[] = "tool";
static char acare_msgs__msg__VisionResult__FIELD_NAME__x[] = "x";
static char acare_msgs__msg__VisionResult__FIELD_NAME__y[] = "y";
static char acare_msgs__msg__VisionResult__FIELD_NAME__z[] = "z";
static char acare_msgs__msg__VisionResult__FIELD_NAME__confidence[] = "confidence";
static char acare_msgs__msg__VisionResult__FIELD_NAME__zone[] = "zone";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__VisionResult__FIELDS[] = {
  {
    {acare_msgs__msg__VisionResult__FIELD_NAME__found, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__VisionResult__FIELD_NAME__tool, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__VisionResult__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__VisionResult__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__VisionResult__FIELD_NAME__z, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__VisionResult__FIELD_NAME__confidence, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__VisionResult__FIELD_NAME__zone, 4, 4},
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
acare_msgs__msg__VisionResult__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__VisionResult__TYPE_NAME, 27, 27},
      {acare_msgs__msg__VisionResult__FIELDS, 7, 7},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "bool found\n"
  "string tool\n"
  "float32 x\n"
  "float32 y\n"
  "float32 z\n"
  "float32 confidence\n"
  "string zone";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__VisionResult__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__VisionResult__TYPE_NAME, 27, 27},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 84, 84},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__VisionResult__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__VisionResult__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
