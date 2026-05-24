// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/Intent.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/intent__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `tool`
// Member `action`
// Member `destination`
#include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__msg__Intent__init(acare_msgs__msg__Intent * msg)
{
  if (!msg) {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__init(&msg->tool)) {
    acare_msgs__msg__Intent__fini(msg);
    return false;
  }
  // action
  if (!rosidl_runtime_c__String__init(&msg->action)) {
    acare_msgs__msg__Intent__fini(msg);
    return false;
  }
  // destination
  if (!rosidl_runtime_c__String__init(&msg->destination)) {
    acare_msgs__msg__Intent__fini(msg);
    return false;
  }
  // confidence
  return true;
}

void
acare_msgs__msg__Intent__fini(acare_msgs__msg__Intent * msg)
{
  if (!msg) {
    return;
  }
  // tool
  rosidl_runtime_c__String__fini(&msg->tool);
  // action
  rosidl_runtime_c__String__fini(&msg->action);
  // destination
  rosidl_runtime_c__String__fini(&msg->destination);
  // confidence
}

bool
acare_msgs__msg__Intent__are_equal(const acare_msgs__msg__Intent * lhs, const acare_msgs__msg__Intent * rhs)
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
  // destination
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->destination), &(rhs->destination)))
  {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__Intent__copy(
  const acare_msgs__msg__Intent * input,
  acare_msgs__msg__Intent * output)
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
  // destination
  if (!rosidl_runtime_c__String__copy(
      &(input->destination), &(output->destination)))
  {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  return true;
}

acare_msgs__msg__Intent *
acare_msgs__msg__Intent__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__Intent * msg = (acare_msgs__msg__Intent *)allocator.allocate(sizeof(acare_msgs__msg__Intent), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__Intent));
  bool success = acare_msgs__msg__Intent__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__Intent__destroy(acare_msgs__msg__Intent * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__Intent__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__Intent__Sequence__init(acare_msgs__msg__Intent__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__Intent * data = NULL;

  if (size) {
    data = (acare_msgs__msg__Intent *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__Intent), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__Intent__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__Intent__fini(&data[i - 1]);
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
acare_msgs__msg__Intent__Sequence__fini(acare_msgs__msg__Intent__Sequence * array)
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
      acare_msgs__msg__Intent__fini(&array->data[i]);
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

acare_msgs__msg__Intent__Sequence *
acare_msgs__msg__Intent__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__Intent__Sequence * array = (acare_msgs__msg__Intent__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__Intent__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__Intent__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__Intent__Sequence__destroy(acare_msgs__msg__Intent__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__Intent__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__Intent__Sequence__are_equal(const acare_msgs__msg__Intent__Sequence * lhs, const acare_msgs__msg__Intent__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__Intent__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__Intent__Sequence__copy(
  const acare_msgs__msg__Intent__Sequence * input,
  acare_msgs__msg__Intent__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__Intent);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__Intent * data =
      (acare_msgs__msg__Intent *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__Intent__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__Intent__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__Intent__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
