# -*- coding: utf-8 -*-
"""
The Ha Magic Home integration iot/common File.
"""
import json
import uuid
import logging
import aiohttp
import random
import hashlib
from typing import Type, Any
from dataclasses import dataclass, asdict

from os import path
from .device_class import (ControlModel, ControlHeader, ResponseModel,
                           ControlResponse)

from homeassistant.components.light import (
    ATTR_RGB_COLOR, )

from .const import (CLOUD_SERVERS_DOMAIN, CLOUD_SERVERS_PATH, CAPABILITY_MAP)

# from paho.mqtt.matcher import MQTTMatcher
import yaml

_LOGGER = logging.getLogger(__name__)

MIOT_ROOT_PATH: str = path.dirname(path.abspath(__file__))


def gen_absolute_path(relative_path: str) -> str:
    """Generate an absolute path."""
    return path.join(MIOT_ROOT_PATH, relative_path)


def calc_group_id(uid: str, home_id: str) -> str:
    """Calculate the group ID based on a user ID and a home ID."""
    return hashlib.sha1(
        f'{uid}central_service{home_id}'.encode('utf-8')).hexdigest()[:16]


def load_json_file(json_file: str) -> dict:
    """Load a JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_yaml_file(yaml_file: str) -> dict:
    """Load a YAML file."""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def from_dict(data: dict, cls: Type):
    # 将字典中的数据映射到类的字段
    fields = {f.name: data.get(f.name) for f in dataclass.fields(cls)}
    for field, value in fields.items():
        if isinstance(value, dict) and hasattr(cls, field):
            # 如果字段是字典并且字段对应的是一个类，则递归转换
            field_type = getattr(cls, field)
            fields[field] = from_dict(value, field_type)
    return cls(**fields)


def json_unmarshal(json_str, cls):
    """
    模拟 Go 中的 json.Unmarshal 方法
    将 JSON 字符串解析并转换为类实例
    """
    # 如果输入已经是字典，直接使用；否则解析 JSON 字符串
    if isinstance(json_str, dict):
        data = json_str
    elif isinstance(json_str, (str, bytes, bytearray)):
        data = json.loads(json_str)
    else:
        raise TypeError(
            f"Invalid input type: {type(json_str)}. Expected str, bytes, bytearray, or dict."
        )

    # 转换为类实例列表
    return from_dict(cls, data)


async def control_req(self, prop: str, value: Any) -> int:
    header = ControlHeader()
    action = CAPABILITY_MAP.get(prop)
    if action == None:
        _LOGGER.error('NotSupportProp:')
        _LOGGER.error(prop)
        return
    capability = self._capability_map[action]
    header.namespace = capability.interface
    header.name = action

    header.interfaceVersion = "2"
    messageId = uuid.uuid4()
    header.messageId = messageId

    payload: dict[str, Any] = {}
    if prop == ATTR_RGB_COLOR:
        payload['red'] = value[0]
        payload['green'] = value[1]
        payload['blue'] = value[2]
    else:
        if capability.properties.supported != None:
            index = 0
            for support_action in capability.actions.supported:
                if support_action.name == action:
                    break
                index = index + 1
            payload[capability.properties.supported[index].name] = value

    config_entry = self.hass.config_entries.async_get_entry(self._entry_id)
    token = config_entry.data.get("access_token")
    cloud_server = config_entry.data.get("cloud_server")

    control = ControlModel()
    control.directive.header = header
    control.directive.endpoint.scope.type = "BearerToken"
    control.directive.endpoint.scope.token = token
    control.directive.endpoint.cookie = self._cookie
    control.directive.endpoint.endpointId = self.device_id
    control.directive.payload = payload

    json_data = control.json()

    _LOGGER.debug(json_data)

    url = CLOUD_SERVERS_DOMAIN[cloud_server] + CLOUD_SERVERS_PATH["control"]
    header = {}
    header["CLOUD_SERVERS_DOMAIN"] = cloud_server
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=json_data,headers=header) as response:
                if response.status != 200:
                    _LOGGER.error(
                        f"HTTP 请求失败: 状态码 {response.status}, 响应: {await response.text()}"
                    )
                    return -1
                res = await response.json()
                response = ControlResponse(**res)
                _LOGGER.debug(res)

                if response.event.payload.status != 0:
                    _LOGGER.error(f"control err: {res}")
                return response.event.payload.status

        except aiohttp.ClientError as e:
            _LOGGER.error(f"网络请求错误: {e}")
            return -2

        except ValueError as e:
            _LOGGER.error(f"JSON 解析错误: {e}")
            return -3

    return


async def report_state(self) -> tuple[ResponseModel, int]:
    header = ControlHeader()
    header.namespace = 'DNA'
    header.name = 'ReportState'

    header.interfaceVersion = "2"
    messageId = uuid.uuid4()
    header.messageId = messageId

    config_entry = self.hass.config_entries.async_get_entry(self._entry_id)
    token = config_entry.data.get("access_token")
    cloud_server = config_entry.data.get("cloud_server")

    control = ControlModel()
    control.directive.header = header
    control.directive.endpoint.scope.type = "BearerToken"
    control.directive.endpoint.scope.token = token
    control.directive.endpoint.cookie = self._cookie
    control.directive.endpoint.endpointId = self.device_id

    json_data = control.json()

    url = CLOUD_SERVERS_DOMAIN[cloud_server] + CLOUD_SERVERS_PATH["control"]
    header = {}
    header["CLOUD_SERVERS_DOMAIN"] = cloud_server
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=json_data,headers=header) as response:
                if response.status != 200:
                    _LOGGER.error(
                        f"HTTP 请求失败: 状态码 {response.status}, 响应: {await response.text()}"
                    )
                    return ResponseModel, -1

                res = await response.json()
                response = ResponseModel(**res)
                if response.event.payload.status != 0:
                    _LOGGER.error(res)
                _LOGGER.debug(response)
                return response, 0

        except aiohttp.ClientError as e:
            _LOGGER.error(f"网络请求错误: {e}")
            return ResponseModel, -2

        except ValueError as e:
            _LOGGER.error(f"JSON 解析错误: {e}")
            return ResponseModel, -3

    return


def randomize_int(value: int, ratio: float) -> int:
    """Randomize an integer value."""
    return int(value * (1 - ratio + random.random() * 2 * ratio))
