// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/ValidatedIntent.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/validated_intent__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `tool`
// Member `action`
// Member `user_id`
// Member `name`
#include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__msg__ValidatedIntent__init(acare_msgs__msg__ValidatedIntent * msg)
{
  if (!msg) {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__init(&msg->tool)) {
    acare_msgs__msg__ValidatedIntent__fini(msg);
    return false;
  }
  // action
  if (!rosidl_runtime_c__String__init(&msg->action)) {
    acare_msgs__msg__ValidatedIntent__fini(msg);
    return false;
  }
  // user_id
  if (!rosidl_runtime_c__String__init(&msg->user_id)) {
    acare_msgs__msg__ValidatedIntent__fini(msg);
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    acare_msgs__msg__ValidatedIntent__fini(msg);
    return false;
  }
  // authenticated
  return true;
}

void
acare_msgs__msg__ValidatedIntent__fini(acare_msgs__msg__ValidatedIntent * msg)
{
  if (!msg) {
    return;
  }
  // tool
  rosidl_runtime_c__String__fini(&msg->tool);
  // action
  rosidl_runtime_c__String__fini(&msg->action);
  // user_id
  rosidl_runtime_c__String__fini(&msg->user_id);
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // authenticated
}

bool
acare_msgs__msg__ValidatedIntent__are_equal(const acare_msgs__msg__ValidatedIntent * lhs, const acare_msgs__msg__ValidatedIntent * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->tool), &(rhs->tool)))
  {
    return false;
  }
  // action
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->action), &(rhs->action)))
  {
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
  // authenticated
  if (lhs->authenticated != rhs->authenticated) {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__ValidatedIntent__copy(
  const acare_msgs__msg__ValidatedIntent * input,
  acare_msgs__msg__ValidatedIntent * output)
{
  if (!input || !output) {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__copy(
      &(input->tool), &(output->tool)))
  {
    return false;
  }
  // action
  if (!rosidl_runtime_c__String__copy(
      &(input->action), &(output->action)))
  {
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
  // authenticated
  output->authenticated = input->authenticated;
  return true;
}

acare_msgs__msg__ValidatedIntent *
acare_msgs__msg__ValidatedIntent__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__ValidatedIntent * msg = (acare_msgs__msg__ValidatedIntent *)allocator.allocate(sizeof(acare_msgs__msg__ValidatedIntent), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__ValidatedIntent));
  bool success = acare_msgs__msg__ValidatedIntent__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__ValidatedIntent__destroy(acare_msgs__msg__ValidatedIntent * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__ValidatedIntent__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__ValidatedIntent__Sequence__init(acare_msgs__msg__ValidatedIntent__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__ValidatedIntent * data = NULL;

  if (size) {
    data = (acare_msgs__msg__ValidatedIntent *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__ValidatedIntent), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__ValidatedIntent__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__ValidatedIntent__fini(&data[i - 1]);
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
acare_msgs__msg__ValidatedIntent__Sequence__fini(acare_msgs__msg__ValidatedIntent__Sequence * array)
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
      acare_msgs__msg__ValidatedIntent__fini(&array->data[i]);
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

acare_msgs__msg__ValidatedIntent__Sequence *
acare_msgs__msg__ValidatedIntent__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__ValidatedIntent__Sequence * array = (acare_msgs__msg__ValidatedIntent__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__ValidatedIntent__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__ValidatedIntent__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__ValidatedIntent__Sequence__destroy(acare_msgs__msg__ValidatedIntent__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__ValidatedIntent__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__ValidatedIntent__Sequence__are_equal(const acare_msgs__msg__ValidatedIntent__Sequence * lhs, const acare_msgs__msg__ValidatedIntent__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__ValidatedIntent__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__ValidatedIntent__Sequence__copy(
  const acare_msgs__msg__ValidatedIntent__Sequence * input,
  acare_msgs__msg__ValidatedIntent__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__ValidatedIntent);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__ValidatedIntent * data =
      (acare_msgs__msg__ValidatedIntent *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__ValidatedIntent__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__ValidatedIntent__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__ValidatedIntent__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
