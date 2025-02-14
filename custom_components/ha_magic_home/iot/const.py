# -*- coding: utf-8 -*-
"""
The Ha Magic Home integration iot/const File.
"""
DOMAIN: str = 'ha_magic_home'
DEFAULT_NAME: str = 'Ha Magic Home'

DEFAULT_NICK_NAME: str = 'ibroadlink'

DEFAULT_CLOUD_SERVER: str = 'cn'

CLOUD_SERVERS: dict = {
    'cn': '中国集群',
    'us': '美国集群',
    'eu': '欧洲集群',
}

SUPPORT_CENTRAL_GATEWAY_CTRL: list = ['cn']

DEFAULT_INTEGRATION_LANGUAGE: str = 'cn'
INTEGRATION_LANGUAGES = {
    'en': 'English',
    'zh-Hans': '简体中文',
}

CLOUD_SERVERS_DOMAIN: dict = {
    'cn': "https://ha-magic-home-mfdddeskcg.cn-hangzhou.fcapp.run",
    'us': "https://ha-magic-home-mfdddeskcg.cn-hangzhou.fcapp.run",
    'eu': "https://ha-magic-home-mfdddeskcg.cn-hangzhou.fcapp.run"
}

CLOUD_SERVERS_PATH: dict = {
    'getToken': "/oauth/v2/token",
    'discover': "/dnaproxy/v2/discover?license=",
    'control': "/dnaproxy/v2/control?license="
}


HA_REDIRECT_URL: str = 'http://homeassistant.local:8123'

SUPPORTED_PLATFORMS: list = ['light', 'climate', 'cover']

#action
CAPABILITY_MAP: dict[str, str] = {
    'on': 'ChangePowerState',
    'off': 'ChangePowerState',
    'brightness': 'SetBrightness',
    'color_temp_kelvin': "SetColorTemp",
    'rgb_color': "SetColor",
    'open': "UpTrip",
    'close': "DownTrip",
    'stop': "Pause",
    'position': "SetPercentage",
    'mode': "SetMode",
    'fan_mode': "SetWindSpeed",
    'set_temperature': "SetFixedTargetTemperature"
}
