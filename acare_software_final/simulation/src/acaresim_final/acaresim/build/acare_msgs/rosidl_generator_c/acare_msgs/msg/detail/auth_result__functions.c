// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/AuthResult.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/auth_result__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `user_id`
// Member `name`
// Member `role`
#include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__msg__AuthResult__init(acare_msgs__msg__AuthResult * msg)
{
  if (!msg) {
    return false;
  }
  // user_id
  if (!rosidl_runtime_c__String__init(&msg->user_id)) {
    acare_msgs__msg__AuthResult__fini(msg);
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    acare_msgs__msg__AuthResult__fini(msg);
    return false;
  }
  // role
  if (!rosidl_runtime_c__String__init(&msg->role)) {
    acare_msgs__msg__AuthResult__fini(msg);
    return false;
  }
  // success
  // face_verified
  // face_confidence
  // voice_confidence
  return true;
}

void
acare_msgs__msg__AuthResult__fini(acare_msgs__msg__AuthResult * msg)
{
  if (!msg) {
    return;
  }
  // user_id
  rosidl_runtime_c__String__fini(&msg->user_id);
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // role
  rosidl_runtime_c__String__fini(&msg->role);
  // success
  // face_verified
  // face_confidence
  // voice_confidence
}

bool
acare_msgs__msg__AuthResult__are_equal(const acare_msgs__msg__AuthResult * lhs, const acare_msgs__msg__AuthResult * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // user_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->user_id), &(rhs->user_id)))
  {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // role
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->role), &(rhs->role)))
  {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // face_verified
  if (lhs->face_verified != rhs->face_verified) {
    return false;
  }
  // face_confidence
  if (lhs->face_confidence != rhs->face_confidence) {
    return false;
  }
  // voice_confidence
  if (lhs->voice_confidence != rhs->voice_confidence) {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__AuthResult__copy(
  const acare_msgs__msg__AuthResult * input,
  acare_msgs__msg__AuthResult * output)
{
  if (!input || !output) {
    return false;
  }
  // user_id
  if (!rosidl_runtime_c__String__copy(
      &(input->user_id), &(output->user_id)))
  {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // role
  if (!rosidl_runtime_c__String__copy(
      &(input->role), &(output->role)))
  {
    return false;
  }
  // success
  output->success = input->success;
  // face_verified
  output->face_verified = input->face_verified;
  // face_confidence
  output->face_confidence = input->face_confidence;
  // voice_confidence
  output->voice_confidence = input->voice_confidence;
  return true;
}

acare_msgs__msg__AuthResult *
acare_msgs__msg__AuthResult__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__AuthResult * msg = (acare_msgs__msg__AuthResult *)allocator.allocate(sizeof(acare_msgs__msg__AuthResult), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__AuthResult));
  bool success = acare_msgs__msg__AuthResult__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__AuthResult__destroy(acare_msgs__msg__AuthResult * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__AuthResult__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__AuthResult__Sequence__init(acare_msgs__msg__AuthResult__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__AuthResult * data = NULL;

  if (size) {
    data = (acare_msgs__msg__AuthResult *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__AuthResult), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__AuthResult__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__AuthResult__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
acare_msgs__msg__AuthResult__Sequence__fini(acare_msgs__msg__AuthResult__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      acare_msgs__msg__AuthResult__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

acare_msgs__msg__AuthResult__Sequence *
acare_msgs__msg__AuthResult__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__AuthResult__Sequence * array = (acare_msgs__msg__AuthResult__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__AuthResult__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__AuthResult__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__AuthResult__Sequence__destroy(acare_msgs__msg__AuthResult__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__AuthResult__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__AuthResult__Sequence__are_equal(const acare_msgs__msg__AuthResult__Sequence * lhs, const acare_msgs__msg__AuthResult__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__AuthResult__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__AuthResult__Sequence__copy(
  const acare_msgs__msg__AuthResult__Sequence * input,
  acare_msgs__msg__AuthResult__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__AuthResult);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__AuthResult * data =
      (acare_msgs__msg__AuthResult *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__AuthResult__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__AuthResult__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__AuthResult__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
