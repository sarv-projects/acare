// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/AuthResult.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/auth_result__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__AuthResult__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4b, 0x9c, 0x2c, 0xb8, 0xef, 0x96, 0x66, 0xc5,
      0x25, 0xaf, 0x25, 0x25, 0x04, 0x18, 0x1e, 0x60,
      0xf9, 0x76, 0xf8, 0xdc, 0x8e, 0xd3, 0xfb, 0x53,
      0x22, 0xe1, 0x6c, 0x65, 0xb6, 0xb6, 0x04, 0x3b,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__AuthResult__TYPE_NAME[] = "acare_msgs/msg/AuthResult";

// Define type names, field names, and default values
static char acare_msgs__msg__AuthResult__FIELD_NAME__user_id[] = "user_id";
static char acare_msgs__msg__AuthResult__FIELD_NAME__name[] = "name";
static char acare_msgs__msg__AuthResult__FIELD_NAME__role[] = "role";
static char acare_msgs__msg__AuthResult__FIELD_NAME__success[] = "success";
static char acare_msgs__msg__AuthResult__FIELD_NAME__face_verified[] = "face_verified";
static char acare_msgs__msg__AuthResult__FIELD_NAME__face_confidence[] = "face_confidence";
static char acare_msgs__msg__AuthResult__FIELD_NAME__voice_confidence[] = "voice_confidence";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__AuthResult__FIELDS[] = {
  {
    {acare_msgs__msg__AuthResult__FIELD_NAME__user_id, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__AuthResult__FIELD_NAME__name, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__AuthResult__FIELD_NAME__role, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__AuthResult__FIELD_NAME__success, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__AuthResult__FIELD_NAME__face_verified, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__AuthResult__FIELD_NAME__face_confidence, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__AuthResult__FIELD_NAME__voice_confidence, 16, 16},
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
acare_msgs__msg__AuthResult__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__AuthResult__TYPE_NAME, 25, 25},
      {acare_msgs__msg__AuthResult__FIELDS, 7, 7},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string user_id\n"
  "string name\n"
  "string role\n"
  "bool success\n"
  "bool face_verified\n"
  "float32 face_confidence\n"
  "float32 voice_confidence";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__AuthResult__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__AuthResult__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 120, 120},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__AuthResult__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__AuthResult__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
