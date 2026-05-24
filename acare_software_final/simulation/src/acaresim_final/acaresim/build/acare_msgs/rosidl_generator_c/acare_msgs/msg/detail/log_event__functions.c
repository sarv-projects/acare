// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/LogEvent.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/log_event__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `event_type`
// Member `user_id`
// Member `tool`
// Member `state`
// Member `description`
// Member `safety_severity`
#include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__msg__LogEvent__init(acare_msgs__msg__LogEvent * msg)
{
  if (!msg) {
    return false;
  }
  // event_type
  if (!rosidl_runtime_c__String__init(&msg->event_type)) {
    acare_msgs__msg__LogEvent__fini(msg);
    return false;
  }
  // user_id
  if (!rosidl_runtime_c__String__init(&msg->user_id)) {
    acare_msgs__msg__LogEvent__fini(msg);
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__init(&msg->tool)) {
    acare_msgs__msg__LogEvent__fini(msg);
    return false;
  }
  // state
  if (!rosidl_runtime_c__String__init(&msg->state)) {
    acare_msgs__msg__LogEvent__fini(msg);
    return false;
  }
  // description
  if (!rosidl_runtime_c__String__init(&msg->description)) {
    acare_msgs__msg__LogEvent__fini(msg);
    return false;
  }
  // timestamp
  // voice_e2e_ms
  // vision_search_ms
  // motion_ms
  // total_task_ms
  // safety_severity
  if (!rosidl_runtime_c__String__init(&msg->safety_severity)) {
    acare_msgs__msg__LogEvent__fini(msg);
    return false;
  }
  return true;
}

void
acare_msgs__msg__LogEvent__fini(acare_msgs__msg__LogEvent * msg)
{
  if (!msg) {
    return;
  }
  // event_type
  rosidl_runtime_c__String__fini(&msg->event_type);
  // user_id
  rosidl_runtime_c__String__fini(&msg->user_id);
  // tool
  rosidl_runtime_c__String__fini(&msg->tool);
  // state
  rosidl_runtime_c__String__fini(&msg->state);
  // description
  rosidl_runtime_c__String__fini(&msg->description);
  // timestamp
  // voice_e2e_ms
  // vision_search_ms
  // motion_ms
  // total_task_ms
  // safety_severity
  rosidl_runtime_c__String__fini(&msg->safety_severity);
}

bool
acare_msgs__msg__LogEvent__are_equal(const acare_msgs__msg__LogEvent * lhs, const acare_msgs__msg__LogEvent * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // event_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->event_type), &(rhs->event_type)))
  {
    return false;
  }
  // user_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->user_id), &(rhs->user_id)))
  {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->tool), &(rhs->tool)))
  {
    return false;
  }
  // state
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->state), &(rhs->state)))
  {
    return false;
  }
  // description
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->description), &(rhs->description)))
  {
    return false;
  }
  // timestamp
  if (lhs->timestamp != rhs->timestamp) {
    return false;
  }
  // voice_e2e_ms
  if (lhs->voice_e2e_ms != rhs->voice_e2e_ms) {
    return false;
  }
  // vision_search_ms
  if (lhs->vision_search_ms != rhs->vision_search_ms) {
    return false;
  }
  // motion_ms
  if (lhs->motion_ms != rhs->motion_ms) {
    return false;
  }
  // total_task_ms
  if (lhs->total_task_ms != rhs->total_task_ms) {
    return false;
  }
  // safety_severity
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->safety_severity), &(rhs->safety_severity)))
  {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__LogEvent__copy(
  const acare_msgs__msg__LogEvent * input,
  acare_msgs__msg__LogEvent * output)
{
  if (!input || !output) {
    return false;
  }
  // event_type
  if (!rosidl_runtime_c__String__copy(
      &(input->event_type), &(output->event_type)))
  {
    return false;
  }
  // user_id
  if (!rosidl_runtime_c__String__copy(
      &(input->user_id), &(output->user_id)))
  {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__copy(
      &(input->tool), &(output->tool)))
  {
    return false;
  }
  // state
  if (!rosidl_runtime_c__String__copy(
      &(input->state), &(output->state)))
  {
    return false;
  }
  // description
  if (!rosidl_runtime_c__String__copy(
      &(input->description), &(output->description)))
  {
    return false;
  }
  // timestamp
  output->timestamp = input->timestamp;
  // voice_e2e_ms
  output->voice_e2e_ms = input->voice_e2e_ms;
  // vision_search_ms
  output->vision_search_ms = input->vision_search_ms;
  // motion_ms
  output->motion_ms = input->motion_ms;
  // total_task_ms
  output->total_task_ms = input->total_task_ms;
  // safety_severity
  if (!rosidl_runtime_c__String__copy(
      &(input->safety_severity), &(output->safety_severity)))
  {
    return false;
  }
  return true;
}

acare_msgs__msg__LogEvent *
acare_msgs__msg__LogEvent__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__LogEvent * msg = (acare_msgs__msg__LogEvent *)allocator.allocate(sizeof(acare_msgs__msg__LogEvent), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__LogEvent));
  bool success = acare_msgs__msg__LogEvent__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__LogEvent__destroy(acare_msgs__msg__LogEvent * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__LogEvent__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__LogEvent__Sequence__init(acare_msgs__msg__LogEvent__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__LogEvent * data = NULL;

  if (size) {
    data = (acare_msgs__msg__LogEvent *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__LogEvent), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__LogEvent__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__LogEvent__fini(&data[i - 1]);
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
acare_msgs__msg__LogEvent__Sequence__fini(acare_msgs__msg__LogEvent__Sequence * array)
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
      acare_msgs__msg__LogEvent__fini(&array->data[i]);
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

acare_msgs__msg__LogEvent__Sequence *
acare_msgs__msg__LogEvent__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__LogEvent__Sequence * array = (acare_msgs__msg__LogEvent__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__LogEvent__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__LogEvent__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__LogEvent__Sequence__destroy(acare_msgs__msg__LogEvent__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__LogEvent__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__LogEvent__Sequence__are_equal(const acare_msgs__msg__LogEvent__Sequence * lhs, const acare_msgs__msg__LogEvent__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__LogEvent__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__LogEvent__Sequence__copy(
  const acare_msgs__msg__LogEvent__Sequence * input,
  acare_msgs__msg__LogEvent__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__LogEvent);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__LogEvent * data =
      (acare_msgs__msg__LogEvent *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__LogEvent__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__LogEvent__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__LogEvent__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
