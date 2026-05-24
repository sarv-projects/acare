// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/StateTransition.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/state_transition__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `target_state`
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__msg__StateTransition__init(acare_msgs__msg__StateTransition * msg)
{
  if (!msg) {
    return false;
  }
  // target_state
  if (!rosidl_runtime_c__String__init(&msg->target_state)) {
    acare_msgs__msg__StateTransition__fini(msg);
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    acare_msgs__msg__StateTransition__fini(msg);
    return false;
  }
  return true;
}

void
acare_msgs__msg__StateTransition__fini(acare_msgs__msg__StateTransition * msg)
{
  if (!msg) {
    return;
  }
  // target_state
  rosidl_runtime_c__String__fini(&msg->target_state);
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
}

bool
acare_msgs__msg__StateTransition__are_equal(const acare_msgs__msg__StateTransition * lhs, const acare_msgs__msg__StateTransition * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // target_state
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->target_state), &(rhs->target_state)))
  {
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reason), &(rhs->reason)))
  {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__StateTransition__copy(
  const acare_msgs__msg__StateTransition * input,
  acare_msgs__msg__StateTransition * output)
{
  if (!input || !output) {
    return false;
  }
  // target_state
  if (!rosidl_runtime_c__String__copy(
      &(input->target_state), &(output->target_state)))
  {
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  return true;
}

acare_msgs__msg__StateTransition *
acare_msgs__msg__StateTransition__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__StateTransition * msg = (acare_msgs__msg__StateTransition *)allocator.allocate(sizeof(acare_msgs__msg__StateTransition), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__StateTransition));
  bool success = acare_msgs__msg__StateTransition__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__StateTransition__destroy(acare_msgs__msg__StateTransition * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__StateTransition__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__StateTransition__Sequence__init(acare_msgs__msg__StateTransition__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__StateTransition * data = NULL;

  if (size) {
    data = (acare_msgs__msg__StateTransition *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__StateTransition), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__StateTransition__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__StateTransition__fini(&data[i - 1]);
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
acare_msgs__msg__StateTransition__Sequence__fini(acare_msgs__msg__StateTransition__Sequence * array)
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
      acare_msgs__msg__StateTransition__fini(&array->data[i]);
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

acare_msgs__msg__StateTransition__Sequence *
acare_msgs__msg__StateTransition__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__StateTransition__Sequence * array = (acare_msgs__msg__StateTransition__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__StateTransition__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__StateTransition__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__StateTransition__Sequence__destroy(acare_msgs__msg__StateTransition__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__StateTransition__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__StateTransition__Sequence__are_equal(const acare_msgs__msg__StateTransition__Sequence * lhs, const acare_msgs__msg__StateTransition__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__StateTransition__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__StateTransition__Sequence__copy(
  const acare_msgs__msg__StateTransition__Sequence * input,
  acare_msgs__msg__StateTransition__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__StateTransition);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__StateTransition * data =
      (acare_msgs__msg__StateTransition *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__StateTransition__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__StateTransition__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__StateTransition__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
