// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:srv/EnrolStaff.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/srv/enrol_staff.hpp"


#ifndef ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__STRUCT_HPP_
#define ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__srv__EnrolStaff_Request __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__srv__EnrolStaff_Request __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct EnrolStaff_Request_
{
  using Type = EnrolStaff_Request_<ContainerAllocator>;

  explicit EnrolStaff_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->role = "";
    }
  }

  explicit EnrolStaff_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : name(_alloc),
    role(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->role = "";
    }
  }

  // field types and members
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _name_type name;
  using _role_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _role_type role;

  // setters for named parameter idiom
  Type & set__name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->name = _arg;
    return *this;
  }
  Type & set__role(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->role = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__srv__EnrolStaff_Request
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__srv__EnrolStaff_Request
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EnrolStaff_Request_ & other) const
  {
    if (this->name != other.name) {
      return false;
    }
    if (this->role != other.role) {
      return false;
    }
    return true;
  }
  bool operator!=(const EnrolStaff_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EnrolStaff_Request_

// alias to use template instance with default allocator
using EnrolStaff_Request =
  acare_msgs::srv::EnrolStaff_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace acare_msgs


#ifndef _WIN32
# define DEPRECATED__acare_msgs__srv__EnrolStaff_Response __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__srv__EnrolStaff_Response __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct EnrolStaff_Response_
{
  using Type = EnrolStaff_Response_<ContainerAllocator>;

  explicit EnrolStaff_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->staff_id = "";
      this->message = "";
    }
  }

  explicit EnrolStaff_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : staff_id(_alloc),
    message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->staff_id = "";
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _staff_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _staff_id_type staff_id;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__staff_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->staff_id = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__srv__EnrolStaff_Response
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__srv__EnrolStaff_Response
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EnrolStaff_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->staff_id != other.staff_id) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const EnrolStaff_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EnrolStaff_Response_

// alias to use template instance with default allocator
using EnrolStaff_Response =
  acare_msgs::srv::EnrolStaff_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace acare_msgs


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__acare_msgs__srv__EnrolStaff_Event __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__srv__EnrolStaff_Event __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct EnrolStaff_Event_
{
  using Type = EnrolStaff_Event_<ContainerAllocator>;

  explicit EnrolStaff_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit EnrolStaff_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<acare_msgs::srv::EnrolStaff_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<acare_msgs::srv::EnrolStaff_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__srv__EnrolStaff_Event
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__srv__EnrolStaff_Event
    std::shared_ptr<acare_msgs::srv::EnrolStaff_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EnrolStaff_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const EnrolStaff_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EnrolStaff_Event_

// alias to use template instance with default allocator
using EnrolStaff_Event =
  acare_msgs::srv::EnrolStaff_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace acare_msgs

namespace acare_msgs
{

namespace srv
{

struct EnrolStaff
{
  using Request = acare_msgs::srv::EnrolStaff_Request;
  using Response = acare_msgs::srv::EnrolStaff_Response;
  using Event = acare_msgs::srv::EnrolStaff_Event;
};

}  // namespace srv

}  // namespace acare_msgs

#endif  // ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__STRUCT_HPP_
