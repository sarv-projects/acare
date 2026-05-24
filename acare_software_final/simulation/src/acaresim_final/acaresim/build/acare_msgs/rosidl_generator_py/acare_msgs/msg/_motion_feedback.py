# generated from rosidl_generator_py/resource/_idl.py.em
# with input from acare_msgs:msg/MotionFeedback.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

# Member 'joint_positions'
# Member 'joint_velocities'
# Member 'joint_currents'
# Member 'temperatures'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MotionFeedback(type):
    """Metaclass of message 'MotionFeedback'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('acare_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'acare_msgs.msg.MotionFeedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__motion_feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__motion_feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__motion_feedback
            cls._TYPE_SUPPORT = module.type_support_msg__msg__motion_feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__motion_feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MotionFeedback(metaclass=Metaclass_MotionFeedback):
    """Message class 'MotionFeedback'."""

    __slots__ = [
        '_success',
        '_phase',
        '_error',
        '_joint_positions',
        '_joint_velocities',
        '_joint_currents',
        '_temperatures',
        '_gripper_force',
        '_imu_roll',
        '_imu_pitch',
        '_imu_yaw',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'phase': 'string',
        'error': 'string',
        'joint_positions': 'sequence<float>',
        'joint_velocities': 'sequence<float>',
        'joint_currents': 'sequence<float>',
        'temperatures': 'sequence<float>',
        'gripper_force': 'float',
        'imu_roll': 'float',
        'imu_pitch': 'float',
        'imu_yaw': 'float',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.phase = kwargs.get('phase', str())
        self.error = kwargs.get('error', str())
        self.joint_positions = array.array('f', kwargs.get('joint_positions', []))
        self.joint_velocities = array.array('f', kwargs.get('joint_velocities', []))
        self.joint_currents = array.array('f', kwargs.get('joint_currents', []))
        self.temperatures = array.array('f', kwargs.get('temperatures', []))
        self.gripper_force = kwargs.get('gripper_force', float())
        self.imu_roll = kwargs.get('imu_roll', float())
        self.imu_pitch = kwargs.get('imu_pitch', float())
        self.imu_yaw = kwargs.get('imu_yaw', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.success != other.success:
            return False
        if self.phase != other.phase:
            return False
        if self.error != other.error:
            return False
        if self.joint_positions != other.joint_positions:
            return False
        if self.joint_velocities != other.joint_velocities:
            return False
        if self.joint_currents != other.joint_currents:
            return False
        if self.temperatures != other.temperatures:
            return False
        if self.gripper_force != other.gripper_force:
            return False
        if self.imu_roll != other.imu_roll:
            return False
        if self.imu_pitch != other.imu_pitch:
            return False
        if self.imu_yaw != other.imu_yaw:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def phase(self):
        """Message field 'phase'."""
        return self._phase

    @phase.setter
    def phase(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'phase' field must be of type 'str'"
        self._phase = value

    @builtins.property
    def error(self):
        """Message field 'error'."""
        return self._error

    @error.setter
    def error(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'error' field must be of type 'str'"
        self._error = value

    @builtins.property
    def joint_positions(self):
        """Message field 'joint_positions'."""
        return self._joint_positions

    @joint_positions.setter
    def joint_positions(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'f', \
                    "The 'joint_positions' array.array() must have the type code of 'f'"
                self._joint_positions = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'joint_positions' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._joint_positions = array.array('f', value)

    @builtins.property
    def joint_velocities(self):
        """Message field 'joint_velocities'."""
        return self._joint_velocities

    @joint_velocities.setter
    def joint_velocities(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'f', \
                    "The 'joint_velocities' array.array() must have the type code of 'f'"
                self._joint_velocities = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'joint_velocities' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._joint_velocities = array.array('f', value)

    @builtins.property
    def joint_currents(self):
        """Message field 'joint_currents'."""
        return self._joint_currents

    @joint_currents.setter
    def joint_currents(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'f', \
                    "The 'joint_currents' array.array() must have the type code of 'f'"
                self._joint_currents = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'joint_currents' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._joint_currents = array.array('f', value)

    @builtins.property
    def temperatures(self):
        """Message field 'temperatures'."""
        return self._temperatures

    @temperatures.setter
    def temperatures(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'f', \
                    "The 'temperatures' array.array() must have the type code of 'f'"
                self._temperatures = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'temperatures' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._temperatures = array.array('f', value)

    @builtins.property
    def gripper_force(self):
        """Message field 'gripper_force'."""
        return self._gripper_force

    @gripper_force.setter
    def gripper_force(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'gripper_force' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'gripper_force' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._gripper_force = value

    @builtins.property
    def imu_roll(self):
        """Message field 'imu_roll'."""
        return self._imu_roll

    @imu_roll.setter
    def imu_roll(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'imu_roll' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'imu_roll' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._imu_roll = value

    @builtins.property
    def imu_pitch(self):
        """Message field 'imu_pitch'."""
        return self._imu_pitch

    @imu_pitch.setter
    def imu_pitch(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'imu_pitch' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'imu_pitch' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._imu_pitch = value

    @builtins.property
    def imu_yaw(self):
        """Message field 'imu_yaw'."""
        return self._imu_yaw

    @imu_yaw.setter
    def imu_yaw(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'imu_yaw' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'imu_yaw' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._imu_yaw = value
