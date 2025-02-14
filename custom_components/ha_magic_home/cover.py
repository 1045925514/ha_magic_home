# -*- coding: utf-8 -*-
"""
The Ha Magic Home integration cover File.
"""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.cover import (ATTR_POSITION, CoverEntity,
                                            CoverEntityFeature)
from .iot.device_class import (Endpoint, Capability)

from .iot.common import control_req

from .iot.const import (DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a config entry."""
    _LOGGER.debug('curtainInit')
    device_list = hass.data[DOMAIN]['devices'][
        config_entry.entry_id]["CURTAIN"]
    new_entities = []

    for device in device_list:
        new_entities.append(Cover(device, config_entry.entry_id))
    if new_entities:
        async_add_entities(new_entities)


class Cover(CoverEntity):

    def __init__(self, device: Endpoint, entry_id: str):
        self.device_id = device.endpointId
        self._cookie = device.cookie
        self._capability_map: dict[str, Capability] = {}
        self._appliance_id = device.endpointId
        self._entry_id = entry_id
        self._attr_unique_id = device.endpointId
        self._attr_name = device.friendlyName
        self._is_on = device.isReachable
        self._attr_is_on = device.isReachable
        if device.isReachable == False:
            self._status = "off"
        else:
            self._status = "on"

        self._attr_is_closed = True
        self._attr_supported_features = CoverEntityFeature(0)
        self._attr_supported_features |= (CoverEntityFeature.OPEN)
        self._attr_supported_features |= (CoverEntityFeature.CLOSE)
        self._attr_supported_features |= (CoverEntityFeature.STOP)

        for capability in device.capabilities:
            for support in capability.actions.supported:
                self._capability_map[support.name] = capability
            if capability.properties.supported == None:
                continue
            for support in capability.properties.supported:
                _LOGGER.debug(support.name)
                if support.name == 'percentage':
                    self._attr_supported_features |= (
                        CoverEntityFeature.SET_POSITION)

        _LOGGER.debug(self._capability_map)

    async def async_open_cover(self, **kwargs) -> None:
        """Open the cover."""
        _LOGGER.debug('async_open_cover')
        if 'ChangePowerState' in self._capability_map:
            res_state = await control_req(self, 'on', 'ON')
            if res_state == 0:
                self._attr_is_closed = False
        else:
            res_state = await control_req(self, 'open', '')
            if res_state == 0:
                self._attr_is_closed = False

    async def async_close_cover(self, **kwargs) -> None:
        """Close the cover."""
        _LOGGER.debug('async_close_cover')
        if 'ChangePowerState' in self._capability_map:
            res_state = await control_req(self, 'off', 'OFF')
            if res_state == 0:
                self._attr_is_closed = True
        else:
            res_state = await control_req(self, 'close', '')
            if res_state == 0:
                self._attr_is_closed = True

    async def async_stop_cover(self, **kwargs) -> None:
        """Stop the cover."""
        _LOGGER.debug('async_stop_cover')
        await control_req(self, 'stop', '')

    async def async_set_cover_position(self, **kwargs) -> None:
        _LOGGER.debug('async_set_cover_position')
        for key, value in kwargs.items():
            await control_req(self, key, value)

    async def async_remove(self):
        """Clean up the entity when it is removed from Home Assistant."""
        print(f"Removing entity {self.entity_id}")
        await super().async_remove()

    @property
    def is_on(self):
        """Return if the light is on."""
        return self._attr_is_on

    @property
    def is_closed(self):
        return self._attr_is_closed
