// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/motion_feedback.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/motion_feedback__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotionFeedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: phase
  {
    out << "phase: ";
    rosidl_generator_traits::value_to_yaml(msg.phase, out);
    out << ", ";
  }

  // member: error
  {
    out << "error: ";
    rosidl_generator_traits::value_to_yaml(msg.error, out);
    out << ", ";
  }

  // member: joint_positions
  {
    if (msg.joint_positions.size() == 0) {
      out << "joint_positions: []";
    } else {
      out << "joint_positions: [";
      size_t pending_items = msg.joint_positions.size();
      for (auto item : msg.joint_positions) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joint_velocities
  {
    if (msg.joint_velocities.size() == 0) {
      out << "joint_velocities: []";
    } else {
      out << "joint_velocities: [";
      size_t pending_items = msg.joint_velocities.size();
      for (auto item : msg.joint_velocities) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joint_currents
  {
    if (msg.joint_currents.size() == 0) {
      out << "joint_currents: []";
    } else {
      out << "joint_currents: [";
      size_t pending_items = msg.joint_currents.size();
      for (auto item : msg.joint_currents) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: temperatures
  {
    if (msg.temperatures.size() == 0) {
      out << "temperatures: []";
    } else {
      out << "temperatures: [";
      size_t pending_items = msg.temperatures.size();
      for (auto item : msg.temperatures) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: gripper_force
  {
    out << "gripper_force: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_force, out);
    out << ", ";
  }

  // member: imu_roll
  {
    out << "imu_roll: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_roll, out);
    out << ", ";
  }

  // member: imu_pitch
  {
    out << "imu_pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_pitch, out);
    out << ", ";
  }

  // member: imu_yaw
  {
    out << "imu_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_yaw, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotionFeedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: phase
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "phase: ";
    rosidl_generator_traits::value_to_yaml(msg.phase, out);
    out << "\n";
  }

  // member: error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error: ";
    rosidl_generator_traits::value_to_yaml(msg.error, out);
    out << "\n";
  }

  // member: joint_positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_positions.size() == 0) {
      out << "joint_positions: []\n";
    } else {
      out << "joint_positions:\n";
      for (auto item : msg.joint_positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joint_velocities
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_velocities.size() == 0) {
      out << "joint_velocities: []\n";
    } else {
      out << "joint_velocities:\n";
      for (auto item : msg.joint_velocities) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joint_currents
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_currents.size() == 0) {
      out << "joint_currents: []\n";
    } else {
      out << "joint_currents:\n";
      for (auto item : msg.joint_currents) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: temperatures
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.temperatures.size() == 0) {
      out << "temperatures: []\n";
    } else {
      out << "temperatures:\n";
      for (auto item : msg.temperatures) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: gripper_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gripper_force: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_force, out);
    out << "\n";
  }

  // member: imu_roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu_roll: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_roll, out);
    out << "\n";
  }

  // member: imu_pitch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu_pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_pitch, out);
    out << "\n";
  }

  // member: imu_yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_yaw, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotionFeedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace acare_msgs

namespace rosidl_generator_traits
{

[[deprecated("use acare_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const acare_msgs::msg::MotionFeedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::MotionFeedback & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::MotionFeedback>()
{
  return "acare_msgs::msg::MotionFeedback";
}

template<>
inline const char * name<acare_msgs::msg::MotionFeedback>()
{
  return "acare_msgs/msg/MotionFeedback";
}

template<>
struct has_fixed_size<acare_msgs::msg::MotionFeedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::MotionFeedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::MotionFeedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__TRAITS_HPP_
