// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:srv/EnrolStaff.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/srv/enrol_staff.hpp"


#ifndef ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__BUILDER_HPP_
#define ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/srv/detail/enrol_staff__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace srv
{

namespace builder
{

class Init_EnrolStaff_Request_role
{
public:
  explicit Init_EnrolStaff_Request_role(::acare_msgs::srv::EnrolStaff_Request & msg)
  : msg_(msg)
  {}
  ::acare_msgs::srv::EnrolStaff_Request role(::acare_msgs::srv::EnrolStaff_Request::_role_type arg)
  {
    msg_.role = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Request msg_;
};

class Init_EnrolStaff_Request_name
{
public:
  Init_EnrolStaff_Request_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EnrolStaff_Request_role name(::acare_msgs::srv::EnrolStaff_Request::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_EnrolStaff_Request_role(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::srv::EnrolStaff_Request>()
{
  return acare_msgs::srv::builder::Init_EnrolStaff_Request_name();
}

}  // namespace acare_msgs


namespace acare_msgs
{

namespace srv
{

namespace builder
{

class Init_EnrolStaff_Response_message
{
public:
  explicit Init_EnrolStaff_Response_message(::acare_msgs::srv::EnrolStaff_Response & msg)
  : msg_(msg)
  {}
  ::acare_msgs::srv::EnrolStaff_Response message(::acare_msgs::srv::EnrolStaff_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Response msg_;
};

class Init_EnrolStaff_Response_staff_id
{
public:
  explicit Init_EnrolStaff_Response_staff_id(::acare_msgs::srv::EnrolStaff_Response & msg)
  : msg_(msg)
  {}
  Init_EnrolStaff_Response_message staff_id(::acare_msgs::srv::EnrolStaff_Response::_staff_id_type arg)
  {
    msg_.staff_id = std::move(arg);
    return Init_EnrolStaff_Response_message(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Response msg_;
};

class Init_EnrolStaff_Response_success
{
public:
  Init_EnrolStaff_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EnrolStaff_Response_staff_id success(::acare_msgs::srv::EnrolStaff_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_EnrolStaff_Response_staff_id(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::srv::EnrolStaff_Response>()
{
  return acare_msgs::srv::builder::Init_EnrolStaff_Response_success();
}

}  // namespace acare_msgs


namespace acare_msgs
{

namespace srv
{

namespace builder
{

class Init_EnrolStaff_Event_response
{
public:
  explicit Init_EnrolStaff_Event_response(::acare_msgs::srv::EnrolStaff_Event & msg)
  : msg_(msg)
  {}
  ::acare_msgs::srv::EnrolStaff_Event response(::acare_msgs::srv::EnrolStaff_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Event msg_;
};

class Init_EnrolStaff_Event_request
{
public:
  explicit Init_EnrolStaff_Event_request(::acare_msgs::srv::EnrolStaff_Event & msg)
  : msg_(msg)
  {}
  Init_EnrolStaff_Event_response request(::acare_msgs::srv::EnrolStaff_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_EnrolStaff_Event_response(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Event msg_;
};

class Init_EnrolStaff_Event_info
{
public:
  Init_EnrolStaff_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EnrolStaff_Event_request info(::acare_msgs::srv::EnrolStaff_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_EnrolStaff_Event_request(msg_);
  }

private:
  ::acare_msgs::srv::EnrolStaff_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::srv::EnrolStaff_Event>()
{
  return acare_msgs::srv::builder::Init_EnrolStaff_Event_info();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__BUILDER_HPP_
