# ha_magic_home

BroadLink Magic Home Integration for Home Assistant
# Home Assistant Magic Home Integration

[English](./README.md) | [Simplified Chinese](./doc/README_zh.md)

Magic Home Integration is an officially supported Home Assistant integration component from broadlink Associates that allows you to use the integration with an already supported broadlink Associates Magic Home IoT smart device in Home Assistant.

## Installation

> Home Assistant version requirements:
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0

### Method 1: Download from GitHub using the git clone command.

```bash
cd config config is the configuration directory of the locally installed homeassistant.
git clone https://github.com/ibroadlink/ha_magic_home.git
cd ha_magic_home
. /install.sh /config
``

This is the recommended method to install the Magic Home integration. When you want to update to a specific version, just switch to the appropriate Tag.

For example, to update the Magic Home Integration version to v1.0.0

```bash
cd config/ha_magic_home
git checkout v1.0.0
. /install.sh /config
```

### Method 2: [HACS](https://hacs.xyz/)

HACS > Overflow Menu > Custom repositories > Repository: https://github.com/ibroadlink/ha_magic_home.git & Category: Integration > ADD

> The Wizard integration has not been added to the HACS store yet, so stay tuned.

### Method 3: Manually via [Samba](https://github.com/home-assistant/addons/tree/master/samba) or [FTPS](https://github.com/hassio-addons/addon-ftp) Installation

Download and copy the `custom_components/ha_magic_home` folder to the `config/custom_components` folder in Home Assistant.

## Configuration

### Authorization
Open the currently used BofA app to get the authorization code
Tap “My” > tap “Third-party services such as voice” > tap the copy button under the device authorization code > get the authorization code.

[Settings > Devices & Services > Add Integration] > Search for “`Ha Magic Home`” > Next > Select the region and language according to the cluster where broadlink Associates app is currently used > Enter the authorization code you copied in the previous step > Click Submit.


### Add IoT devices

After successfully logging in, it will automatically synchronize the supported devices under the current authorization code home.

### Multi-Family Login

After a family has been successfully added, you can repeat the authorization steps to add devices in multiple families, the method is the same as above.


### Resynchronize family data

Delete the current integration and re-synchronize the authorization


## Security

Broadlink Associates Magic Home integration and the cloud interface it uses are provided by broadlink Associates. You need to use the authorization code in broadlink Associates app to get the family authorization and get the device list. After using the authorization code to get the home, the platform will not save the authorization code, but save the home token, which has an expiration date, and if the expiration date is up, it will cause the device control to fail and need to be re-authorized. Meanwhile, due to the limitation of Home Assistant platform, after successful login, your device information including io device control key will be explicitly saved in Home Assistant's configuration. Therefore, you need to keep your Home Assistant configuration safe. Once leaked, others can use this information to control your home devices.

## Frequently Asked Questions

- Does broadlink Associates Magic Home Integration currently support all broadlink Associates Magic Home devices?

  broadlink Associates Magic Home Integration currently supports some categories of Magic Home devices, but there are still many categories that are not supported at this time. We support users to develop the required functions by themselves, and we have already opened up the necessary open interfaces for authorization, device discovery, device control, device status query, etc. The documentation can be referred to: https://apifox.com/apidoc/shared-b1f3b852-05c4-4eb7-a9d0-7bbfdc7a6e03/readme-5932490m0


## Principle of sending and receiving messages

### Cloud control


When BofA Magic Home Integration needs to control a device, it sends the request to the cloud via HTTPS, the cloud processes the request and sends it to the gateway device, which then sends a control message to the local device, which responds accordingly after receiving the control message from the gateway.

### Local Control

Local control is not supported for the time being.



### Mapping relationship between Brolink Magic Home devices and Home Assistant entities

broadlink Associates Magic Home uses device intent capabilities to describe device functions, and the capabilities can be mapped to the functions of Home Assistant entities.

After device discovery, the preset scenarios do not generate entities in Home Assistant

The device information in endpoints will be mapped to the corresponding entity categories in Home Assistant based on the category information in displayCategories.

Maps the device information to the Home Assistant entity based on the capabilities supported by the device.

According to the capabilities mapped to the functions of the device entities in Home Assistant, when controlling the device, we can change the control from Home Assistant to BLC Intent Control.


## Multi-language support

broadlink Associates Magic Home Integration Configuration Options allows you to select two languages for integration: Simplified Chinese and English. English is machine translated. If you want to change the words in the configuration page, you need to modify the json file of the corresponding language in the `custom_components/ha_magic_home/translations/` and `custom_components/ha_magic_home/iot/i18n/` directories.


## Documentation

- [LICENSE](../LICENSE.md)
- Contributing guidelines: [English](../CONTRIBUTING.md) | [Simplified Chinese](./CONTRIBUTING_zh.md)
- [Update Log](../CONTRIBUTING_zh.md)
- Development documentation: https://developers.home-assistant.io/docs/creating_component_index

## Catalog structure

- iot: Basic code logic and data structure definitions.
- iot/common: common code logic, the core is device control and status query.
- iot/const: some constants.
- iot/device_class: basic data structure definition.
- config_flow: configuration flow.
