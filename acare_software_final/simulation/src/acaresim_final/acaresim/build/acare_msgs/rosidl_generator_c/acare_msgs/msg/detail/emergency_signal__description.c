// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/EmergencySignal.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/emergency_signal__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__EmergencySignal__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x48, 0x57, 0x7c, 0xf0, 0x1c, 0x98, 0xc0, 0xd8,
      0x71, 0x20, 0x72, 0xb8, 0xfb, 0x99, 0xd0, 0xbb,
      0x28, 0xba, 0x00, 0xba, 0x04, 0xed, 0x12, 0x13,
      0xa7, 0x1a, 0x8a, 0x87, 0xb5, 0xa1, 0x64, 0x0e,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__EmergencySignal__TYPE_NAME[] = "acare_msgs/msg/EmergencySignal";

// Define type names, field names, and default values
static char acare_msgs__msg__EmergencySignal__FIELD_NAME__reason[] = "reason";
static char acare_msgs__msg__EmergencySignal__FIELD_NAME__source[] = "source";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__EmergencySignal__FIELDS[] = {
  {
    {acare_msgs__msg__EmergencySignal__FIELD_NAME__reason, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__EmergencySignal__FIELD_NAME__source, 6, 6},
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
acare_msgs__msg__EmergencySignal__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__EmergencySignal__TYPE_NAME, 30, 30},
      {acare_msgs__msg__EmergencySignal__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string reason\n"
  "string source";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__EmergencySignal__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__EmergencySignal__TYPE_NAME, 30, 30},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 28, 28},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__EmergencySignal__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__EmergencySignal__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
