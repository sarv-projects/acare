// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/VisionSearchRequest.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/vision_search_request__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__VisionSearchRequest__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xd7, 0xc8, 0x0e, 0xdb, 0x56, 0xc6, 0x3c, 0xb2,
      0x67, 0x65, 0xca, 0x1d, 0x52, 0x96, 0x66, 0x89,
      0x73, 0xc5, 0xbc, 0x18, 0x3c, 0x93, 0x21, 0x8b,
      0xa0, 0x1a, 0x7e, 0x57, 0x03, 0x9b, 0xc7, 0xc4,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__VisionSearchRequest__TYPE_NAME[] = "acare_msgs/msg/VisionSearchRequest";

// Define type names, field names, and default values
static char acare_msgs__msg__VisionSearchRequest__FIELD_NAME__tool[] = "tool";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__VisionSearchRequest__FIELDS[] = {
  {
    {acare_msgs__msg__VisionSearchRequest__FIELD_NAME__tool, 4, 4},
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
acare_msgs__msg__VisionSearchRequest__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__VisionSearchRequest__TYPE_NAME, 34, 34},
      {acare_msgs__msg__VisionSearchRequest__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string tool";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__VisionSearchRequest__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__VisionSearchRequest__TYPE_NAME, 34, 34},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 12, 12},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__VisionSearchRequest__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__VisionSearchRequest__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
