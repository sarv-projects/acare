// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/StateTransition.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/state_transition__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__StateTransition__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xf2, 0x1f, 0x60, 0x67, 0xfb, 0x25, 0x0a, 0x9e,
      0x54, 0xb1, 0x6c, 0xc7, 0xc7, 0x79, 0xff, 0x64,
      0x7e, 0x43, 0xab, 0xda, 0x5f, 0xf8, 0xbb, 0x5f,
      0x0a, 0xd2, 0x47, 0x85, 0x7a, 0x4d, 0x34, 0x30,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__StateTransition__TYPE_NAME[] = "acare_msgs/msg/StateTransition";

// Define type names, field names, and default values
static char acare_msgs__msg__StateTransition__FIELD_NAME__target_state[] = "target_state";
static char acare_msgs__msg__StateTransition__FIELD_NAME__reason[] = "reason";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__StateTransition__FIELDS[] = {
  {
    {acare_msgs__msg__StateTransition__FIELD_NAME__target_state, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__StateTransition__FIELD_NAME__reason, 6, 6},
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
acare_msgs__msg__StateTransition__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__StateTransition__TYPE_NAME, 30, 30},
      {acare_msgs__msg__StateTransition__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string target_state\n"
  "string reason";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__StateTransition__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__StateTransition__TYPE_NAME, 30, 30},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 34, 34},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__StateTransition__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__StateTransition__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
