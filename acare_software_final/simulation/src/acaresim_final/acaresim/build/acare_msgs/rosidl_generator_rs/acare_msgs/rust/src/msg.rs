#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to acare_msgs__msg__RobotState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub active_user_id: std::string::String,

}



impl Default for RobotState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotState::default())
  }
}

impl rosidl_runtime_rs::Message for RobotState {
  type RmwMsg = super::msg::rmw::RobotState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        state: msg.state.as_str().into(),
        active_user_id: msg.active_user_id.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        state: msg.state.as_str().into(),
        active_user_id: msg.active_user_id.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      state: msg.state.to_string(),
      active_user_id: msg.active_user_id.to_string(),
    }
  }
}


// Corresponds to acare_msgs__msg__StateTransition

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StateTransition {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

}



impl Default for StateTransition {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::StateTransition::default())
  }
}

impl rosidl_runtime_rs::Message for StateTransition {
  type RmwMsg = super::msg::rmw::StateTransition;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_state: msg.target_state.as_str().into(),
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_state: msg.target_state.as_str().into(),
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_state: msg.target_state.to_string(),
      reason: msg.reason.to_string(),
    }
  }
}


// Corresponds to acare_msgs__msg__Intent

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Intent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub action: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub destination: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,

}



impl Default for Intent {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Intent::default())
  }
}

impl rosidl_runtime_rs::Message for Intent {
  type RmwMsg = super::msg::rmw::Intent;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool: msg.tool.as_str().into(),
        action: msg.action.as_str().into(),
        destination: msg.destination.as_str().into(),
        confidence: msg.confidence,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool: msg.tool.as_str().into(),
        action: msg.action.as_str().into(),
        destination: msg.destination.as_str().into(),
      confidence: msg.confidence,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tool: msg.tool.to_string(),
      action: msg.action.to_string(),
      destination: msg.destination.to_string(),
      confidence: msg.confidence,
    }
  }
}


// Corresponds to acare_msgs__msg__ValidatedIntent

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ValidatedIntent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub action: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub user_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub authenticated: bool,

}



impl Default for ValidatedIntent {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ValidatedIntent::default())
  }
}

impl rosidl_runtime_rs::Message for ValidatedIntent {
  type RmwMsg = super::msg::rmw::ValidatedIntent;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool: msg.tool.as_str().into(),
        action: msg.action.as_str().into(),
        user_id: msg.user_id.as_str().into(),
        name: msg.name.as_str().into(),
        authenticated: msg.authenticated,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool: msg.tool.as_str().into(),
        action: msg.action.as_str().into(),
        user_id: msg.user_id.as_str().into(),
        name: msg.name.as_str().into(),
      authenticated: msg.authenticated,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tool: msg.tool.to_string(),
      action: msg.action.to_string(),
      user_id: msg.user_id.to_string(),
      name: msg.name.to_string(),
      authenticated: msg.authenticated,
    }
  }
}


// Corresponds to acare_msgs__msg__SafetyAlert

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SafetyAlert {

    // This member is not documented.
    #[allow(missing_docs)]
    pub severity: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub source: std::string::String,

}



impl Default for SafetyAlert {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SafetyAlert::default())
  }
}

impl rosidl_runtime_rs::Message for SafetyAlert {
  type RmwMsg = super::msg::rmw::SafetyAlert;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        severity: msg.severity.as_str().into(),
        reason: msg.reason.as_str().into(),
        source: msg.source.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        severity: msg.severity.as_str().into(),
        reason: msg.reason.as_str().into(),
        source: msg.source.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      severity: msg.severity.to_string(),
      reason: msg.reason.to_string(),
      source: msg.source.to_string(),
    }
  }
}


// Corresponds to acare_msgs__msg__HandStatus

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct HandStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub hand_detected: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub is_open: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub palm_up: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,

}



impl Default for HandStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::HandStatus::default())
  }
}

impl rosidl_runtime_rs::Message for HandStatus {
  type RmwMsg = super::msg::rmw::HandStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        hand_detected: msg.hand_detected,
        is_open: msg.is_open,
        palm_up: msg.palm_up,
        x: msg.x,
        y: msg.y,
        z: msg.z,
        confidence: msg.confidence,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      hand_detected: msg.hand_detected,
      is_open: msg.is_open,
      palm_up: msg.palm_up,
      x: msg.x,
      y: msg.y,
      z: msg.z,
      confidence: msg.confidence,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      hand_detected: msg.hand_detected,
      is_open: msg.is_open,
      palm_up: msg.palm_up,
      x: msg.x,
      y: msg.y,
      z: msg.z,
      confidence: msg.confidence,
    }
  }
}


// Corresponds to acare_msgs__msg__AuthResult

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AuthResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub user_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub role: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub face_verified: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub face_confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub voice_confidence: f32,

}



impl Default for AuthResult {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AuthResult::default())
  }
}

impl rosidl_runtime_rs::Message for AuthResult {
  type RmwMsg = super::msg::rmw::AuthResult;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        user_id: msg.user_id.as_str().into(),
        name: msg.name.as_str().into(),
        role: msg.role.as_str().into(),
        success: msg.success,
        face_verified: msg.face_verified,
        face_confidence: msg.face_confidence,
        voice_confidence: msg.voice_confidence,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        user_id: msg.user_id.as_str().into(),
        name: msg.name.as_str().into(),
        role: msg.role.as_str().into(),
      success: msg.success,
      face_verified: msg.face_verified,
      face_confidence: msg.face_confidence,
      voice_confidence: msg.voice_confidence,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      user_id: msg.user_id.to_string(),
      name: msg.name.to_string(),
      role: msg.role.to_string(),
      success: msg.success,
      face_verified: msg.face_verified,
      face_confidence: msg.face_confidence,
      voice_confidence: msg.voice_confidence,
    }
  }
}


// Corresponds to acare_msgs__msg__VisionResult

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct VisionResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub found: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub zone: std::string::String,

}



impl Default for VisionResult {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::VisionResult::default())
  }
}

impl rosidl_runtime_rs::Message for VisionResult {
  type RmwMsg = super::msg::rmw::VisionResult;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        found: msg.found,
        tool: msg.tool.as_str().into(),
        x: msg.x,
        y: msg.y,
        z: msg.z,
        confidence: msg.confidence,
        zone: msg.zone.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      found: msg.found,
        tool: msg.tool.as_str().into(),
      x: msg.x,
      y: msg.y,
      z: msg.z,
      confidence: msg.confidence,
        zone: msg.zone.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      found: msg.found,
      tool: msg.tool.to_string(),
      x: msg.x,
      y: msg.y,
      z: msg.z,
      confidence: msg.confidence,
      zone: msg.zone.to_string(),
    }
  }
}


// Corresponds to acare_msgs__msg__VisionSearchRequest

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct VisionSearchRequest {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: std::string::String,

}



impl Default for VisionSearchRequest {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::VisionSearchRequest::default())
  }
}

impl rosidl_runtime_rs::Message for VisionSearchRequest {
  type RmwMsg = super::msg::rmw::VisionSearchRequest;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool: msg.tool.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool: msg.tool.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tool: msg.tool.to_string(),
    }
  }
}


// Corresponds to acare_msgs__msg__ArmCommand

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ArmCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub command: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_angles: Vec<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity_scale: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub accel_limit: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub blocking: bool,

}



impl Default for ArmCommand {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ArmCommand::default())
  }
}

impl rosidl_runtime_rs::Message for ArmCommand {
  type RmwMsg = super::msg::rmw::ArmCommand;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
        joint_angles: msg.joint_angles.into(),
        velocity_scale: msg.velocity_scale,
        accel_limit: msg.accel_limit,
        blocking: msg.blocking,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
        joint_angles: msg.joint_angles.as_slice().into(),
      velocity_scale: msg.velocity_scale,
      accel_limit: msg.accel_limit,
      blocking: msg.blocking,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      command: msg.command.to_string(),
      joint_angles: msg.joint_angles
          .into_iter()
          .collect(),
      velocity_scale: msg.velocity_scale,
      accel_limit: msg.accel_limit,
      blocking: msg.blocking,
    }
  }
}


// Corresponds to acare_msgs__msg__GripperCommand

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GripperCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub command: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub force_target: f32,

}



impl Default for GripperCommand {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GripperCommand::default())
  }
}

impl rosidl_runtime_rs::Message for GripperCommand {
  type RmwMsg = super::msg::rmw::GripperCommand;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
        force_target: msg.force_target,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
      force_target: msg.force_target,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      command: msg.command.to_string(),
      force_target: msg.force_target,
    }
  }
}


// Corresponds to acare_msgs__msg__MotionFeedback

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionFeedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub phase: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_positions: Vec<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_velocities: Vec<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_currents: Vec<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub temperatures: Vec<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper_force: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_roll: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_pitch: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_yaw: f32,

}



impl Default for MotionFeedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MotionFeedback::default())
  }
}

impl rosidl_runtime_rs::Message for MotionFeedback {
  type RmwMsg = super::msg::rmw::MotionFeedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        phase: msg.phase.as_str().into(),
        error: msg.error.as_str().into(),
        joint_positions: msg.joint_positions.into(),
        joint_velocities: msg.joint_velocities.into(),
        joint_currents: msg.joint_currents.into(),
        temperatures: msg.temperatures.into(),
        gripper_force: msg.gripper_force,
        imu_roll: msg.imu_roll,
        imu_pitch: msg.imu_pitch,
        imu_yaw: msg.imu_yaw,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        phase: msg.phase.as_str().into(),
        error: msg.error.as_str().into(),
        joint_positions: msg.joint_positions.as_slice().into(),
        joint_velocities: msg.joint_velocities.as_slice().into(),
        joint_currents: msg.joint_currents.as_slice().into(),
        temperatures: msg.temperatures.as_slice().into(),
      gripper_force: msg.gripper_force,
      imu_roll: msg.imu_roll,
      imu_pitch: msg.imu_pitch,
      imu_yaw: msg.imu_yaw,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      phase: msg.phase.to_string(),
      error: msg.error.to_string(),
      joint_positions: msg.joint_positions
          .into_iter()
          .collect(),
      joint_velocities: msg.joint_velocities
          .into_iter()
          .collect(),
      joint_currents: msg.joint_currents
          .into_iter()
          .collect(),
      temperatures: msg.temperatures
          .into_iter()
          .collect(),
      gripper_force: msg.gripper_force,
      imu_roll: msg.imu_roll,
      imu_pitch: msg.imu_pitch,
      imu_yaw: msg.imu_yaw,
    }
  }
}


// Corresponds to acare_msgs__msg__LogEvent

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LogEvent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub event_type: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub user_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub description: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub voice_e2e_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vision_search_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub motion_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub total_task_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub safety_severity: std::string::String,

}



impl Default for LogEvent {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::LogEvent::default())
  }
}

impl rosidl_runtime_rs::Message for LogEvent {
  type RmwMsg = super::msg::rmw::LogEvent;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        event_type: msg.event_type.as_str().into(),
        user_id: msg.user_id.as_str().into(),
        tool: msg.tool.as_str().into(),
        state: msg.state.as_str().into(),
        description: msg.description.as_str().into(),
        timestamp: msg.timestamp,
        voice_e2e_ms: msg.voice_e2e_ms,
        vision_search_ms: msg.vision_search_ms,
        motion_ms: msg.motion_ms,
        total_task_ms: msg.total_task_ms,
        safety_severity: msg.safety_severity.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        event_type: msg.event_type.as_str().into(),
        user_id: msg.user_id.as_str().into(),
        tool: msg.tool.as_str().into(),
        state: msg.state.as_str().into(),
        description: msg.description.as_str().into(),
      timestamp: msg.timestamp,
      voice_e2e_ms: msg.voice_e2e_ms,
      vision_search_ms: msg.vision_search_ms,
      motion_ms: msg.motion_ms,
      total_task_ms: msg.total_task_ms,
        safety_severity: msg.safety_severity.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      event_type: msg.event_type.to_string(),
      user_id: msg.user_id.to_string(),
      tool: msg.tool.to_string(),
      state: msg.state.to_string(),
      description: msg.description.to_string(),
      timestamp: msg.timestamp,
      voice_e2e_ms: msg.voice_e2e_ms,
      vision_search_ms: msg.vision_search_ms,
      motion_ms: msg.motion_ms,
      total_task_ms: msg.total_task_ms,
      safety_severity: msg.safety_severity.to_string(),
    }
  }
}


// Corresponds to acare_msgs__msg__EmergencySignal

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EmergencySignal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub source: std::string::String,

}



impl Default for EmergencySignal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::EmergencySignal::default())
  }
}

impl rosidl_runtime_rs::Message for EmergencySignal {
  type RmwMsg = super::msg::rmw::EmergencySignal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        reason: msg.reason.as_str().into(),
        source: msg.source.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        reason: msg.reason.as_str().into(),
        source: msg.source.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      reason: msg.reason.to_string(),
      source: msg.source.to_string(),
    }
  }
}


