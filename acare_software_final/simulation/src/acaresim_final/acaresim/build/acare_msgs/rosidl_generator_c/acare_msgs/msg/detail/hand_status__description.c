// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/HandStatus.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/hand_status__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__HandStatus__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x26, 0x83, 0x77, 0x40, 0x1f, 0x50, 0x01, 0x26,
      0x3a, 0x2c, 0x4c, 0x00, 0x68, 0xeb, 0x37, 0xe6,
      0xf7, 0x9a, 0x8e, 0xc7, 0xd7, 0x6b, 0xe0, 0x54,
      0x79, 0x1b, 0x18, 0x15, 0x50, 0xdd, 0x38, 0x94,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__HandStatus__TYPE_NAME[] = "acare_msgs/msg/HandStatus";

// Define type names, field names, and default values
static char acare_msgs__msg__HandStatus__FIELD_NAME__hand_detected[] = "hand_detected";
static char acare_msgs__msg__HandStatus__FIELD_NAME__is_open[] = "is_open";
static char acare_msgs__msg__HandStatus__FIELD_NAME__palm_up[] = "palm_up";
static char acare_msgs__msg__HandStatus__FIELD_NAME__x[] = "x";
static char acare_msgs__msg__HandStatus__FIELD_NAME__y[] = "y";
static char acare_msgs__msg__HandStatus__FIELD_NAME__z[] = "z";
static char acare_msgs__msg__HandStatus__FIELD_NAME__confidence[] = "confidence";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__HandStatus__FIELDS[] = {
  {
    {acare_msgs__msg__HandStatus__FIELD_NAME__hand_detected, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__HandStatus__FIELD_NAME__is_open, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__HandStatus__FIELD_NAME__palm_up, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__HandStatus__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__HandStatus__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__HandStatus__FIELD_NAME__z, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__HandStatus__FIELD_NAME__confidence, 10, 10},
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
acare_msgs__msg__HandStatus__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__HandStatus__TYPE_NAME, 25, 25},
      {acare_msgs__msg__HandStatus__FIELDS, 7, 7},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "bool hand_detected\n"
  "bool is_open\n"
  "bool palm_up\n"
  "float32 x\n"
  "float32 y\n"
  "float32 z\n"
  "float32 confidence";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__HandStatus__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__HandStatus__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 94, 94},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__HandStatus__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__HandStatus__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
