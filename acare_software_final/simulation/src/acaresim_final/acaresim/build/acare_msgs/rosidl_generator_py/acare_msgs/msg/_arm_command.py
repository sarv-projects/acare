# generated from rosidl_generator_py/resource/_idl.py.em
# with input from acare_msgs:msg/ArmCommand.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

# Member 'joint_angles'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ArmCommand(type):
    """Metaclass of message 'ArmCommand'."""

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
                'acare_msgs.msg.ArmCommand')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__arm_command
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__arm_command
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__arm_command
            cls._TYPE_SUPPORT = module.type_support_msg__msg__arm_command
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__arm_command

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ArmCommand(metaclass=Metaclass_ArmCommand):
    """Message class 'ArmCommand'."""

    __slots__ = [
        '_command',
        '_joint_angles',
        '_velocity_scale',
        '_accel_limit',
        '_blocking',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'command': 'string',
        'joint_angles': 'sequence<float>',
        'velocity_scale': 'float',
        'accel_limit': 'float',
        'blocking': 'boolean',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
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
        self.command = kwargs.get('command', str())
        self.joint_angles = array.array('f', kwargs.get('joint_angles', []))
        self.velocity_scale = kwargs.get('velocity_scale', float())
        self.accel_limit = kwargs.get('accel_limit', float())
        self.blocking = kwargs.get('blocking', bool())

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
        if self.command != other.command:
            return False
        if self.joint_angles != other.joint_angles:
            return False
        if self.velocity_scale != other.velocity_scale:
            return False
        if self.accel_limit != other.accel_limit:
            return False
        if self.blocking != other.blocking:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def command(self):
        """Message field 'command'."""
        return self._command

    @command.setter
    def command(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'command' field must be of type 'str'"
        self._command = value

    @builtins.property
    def joint_angles(self):
        """Message field 'joint_angles'."""
        return self._joint_angles

    @joint_angles.setter
    def joint_angles(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'f', \
                    "The 'joint_angles' array.array() must have the type code of 'f'"
                self._joint_angles = value
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
                "The 'joint_angles' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._joint_angles = array.array('f', value)

    @builtins.property
    def velocity_scale(self):
        """Message field 'velocity_scale'."""
        return self._velocity_scale

    @velocity_scale.setter
    def velocity_scale(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'velocity_scale' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'velocity_scale' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._velocity_scale = value

    @builtins.property
    def accel_limit(self):
        """Message field 'accel_limit'."""
        return self._accel_limit

    @accel_limit.setter
    def accel_limit(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'accel_limit' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'accel_limit' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._accel_limit = value

    @builtins.property
    def blocking(self):
        """Message field 'blocking'."""
        return self._blocking

    @blocking.setter
    def blocking(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'blocking' field must be of type 'bool'"
        self._blocking = value
