# -*- coding: utf-8 -*-
"""
The Ha Magic Home integration Init File.
"""
import logging
import aiohttp
from collections import defaultdict
from datetime import timedelta
from urllib.parse import quote

import uuid
import json

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .iot.const import (SUPPORTED_PLATFORMS)
from homeassistant.helpers.event import async_call_later
from .iot.device_class import Discovery


from .iot.const import (DOMAIN, CLOUD_SERVERS_DOMAIN, CLOUD_SERVERS_PATH)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    family_id = entry.data.get("family_id")
    token = entry.data.get("access_token")
    cloud_server = entry.data.get("cloud_server")

    expires_in = entry.data.get("expires_in")

    async def dynamic_task():
        """周期性任务，执行后修改下一次运行时间"""
        #refresh token
        expires_in = await refresh_token_handle(hass, entry)

        async_call_later(hass, timedelta(seconds=expires_in), dynamic_task)

    async_call_later(hass, timedelta(seconds=expires_in), dynamic_task)

    _LOGGER.debug('家庭信息:%s,%s,%s',family_id,token,cloud_server)

    await async_get_devices(hass, token, cloud_server, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload an integration."""
    await hass.config_entries.async_unload_platforms(
        entry, SUPPORTED_PLATFORMS)

    return True


async def async_get_devices(hass: HomeAssistant, token, cloud_server,
                            entry: ConfigEntry):
    """Device Dsicover """
    url = CLOUD_SERVERS_DOMAIN[cloud_server] + CLOUD_SERVERS_PATH["discover"]
    random_uuid = uuid.uuid4()
    header = {}
    header["CLOUD_SERVERS_DOMAIN"] = cloud_server
    
    body_dict = {
        "directive": {
            "header": {
                "namespace": "DNA.Discovery",
                "name": "Discover",
                "interfaceVersion": "2",
                "messageId": f"{random_uuid}"
            },
            "payload": {
                "scope": {
                    "type": "BearerToken",
                    "token": f"{token}"
                }
            }
        }
    }
    body = json.dumps(body_dict)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=body,headers=header) as response:
                res = await response.text()
                _LOGGER.debug(f"discoverDev:,{res}")
                discovery = Discovery.parse_raw(res)
                device_category_map = defaultdict(list)
                for device in discovery.event.endpoints:
                    device_type = device.displayCategories[0]

                    tmp_dev_list = device_category_map[device_type]
                    tmp_dev_list.append(device)

                if 'devices' not in hass.data[DOMAIN]:
                    hass.data[DOMAIN]['devices'] = {}

                hass.data[DOMAIN]['devices'][
                    entry.entry_id] = device_category_map
                await hass.config_entries.async_forward_entry_setups(
                    entry, SUPPORTED_PLATFORMS)
        except aiohttp.ClientError as e:
            _LOGGER.error(str(e))
            raise ValueError()


async def refresh_token_handle(hass: HomeAssistant, entry: ConfigEntry) -> int:
    cloud_server = entry.data.get("cloud_server")
    refresh_token = entry.data.get("refresh_token")

    url = CLOUD_SERVERS_DOMAIN[cloud_server] + CLOUD_SERVERS_PATH['getToken']
    # payload = {"auth_code": auth_code}
    url = url + "?grant_type=refresh_token"
    url = url + '&refresh_token=' + refresh_token 
    
    header = {}
    header["CLOUD_SERVERS_DOMAIN"] = cloud_server
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url,headers=header) as response:
                if response.status != 200:
                    raise ValueError(
                        _LOGGER.error(f"invalid res status:{response.status}"))

                response_data = await response.json()
                _LOGGER.debug(response_data)

                if response_data["expires_in"] == 0:
                    raise ValueError(
                        _LOGGER.error(f"server_validation_failed:{response}"))
                hass.config_entries.async_update_entry(
                    entry,
                    data={
                        **entry.data, "access_token":
                        response_data["access_token"],
                        "refresh_token": response_data["refresh_token"],
                        "expires_in": response_data["expires_in"]
                    },
                )
                return response_data["expires_in"] // 2
        except aiohttp.ClientError as e:

            raise ValueError(_LOGGER.error(f"http err:{str(e)}"))

    return
