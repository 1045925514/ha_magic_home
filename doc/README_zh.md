# Home Assistant 魔法家集成

[English](./README.md) | [简体中文](./doc/README_zh.md)

魔法家家集成是一个由博联官方提供支持的 Home Assistant 的集成组件，它可以让您在 Home Assistant 中使用集成已经支持的博联魔法家 IoT 智能设备。

## 安装

> Home Assistant 版本要求：
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0

### 方法 1：使用 git clone 命令从 GitHub 下载

```bash
cd config  config即为本地安装的homeassistant的配置目录
git clone https://github.com/ibroadlink/ha_magic_home.git
cd ha_magic_home
./install.sh /config
```

推荐使用此方法安装魔法家家集成。当您想要更新至特定版本时，只需要切换至相应的 Tag 。

例如，更新魔法家家集成版本至 v1.0.0

```bash
cd config/ha_magic_home
git checkout v1.0.0
./install.sh /config
```

### 方法 2: [HACS](https://hacs.xyz/)

HACS > Overflow Menu > Custom repositories > Repository: https://github.com/ibroadlink/ha_magic_home.git & Category: Integration > ADD

> 魔法家集成暂未添加到 HACS 商店，敬请期待。

### 方法 3：通过 [Samba](https://github.com/home-assistant/addons/tree/master/samba) 或 [FTPS](https://github.com/hassio-addons/addon-ftp) 手动安装

下载并将 `custom_components/ha_magic_home` 文件夹复制到 Home Assistant 的 `config/custom_components` 文件夹下。

## 配置

### 授权
打开当前使用的博联app 获取授权码
点击 “我的” > 点击 “语音等第三方服务” > 点击设备授权码下的复制按钮 > 获取授权码

[设置 > 设备与服务 > 添加集成] > 搜索“`Ha Magic Home`” > 下一步 > 根据当前使用的博联app所在集群确认选择登陆地区以及语言 > 在输入上一步复制的授权码 > 点击 提交


### 添加 IoT 设备

登录成功后，将会自动同步当前授权码家庭下的已经支持品类的设备

### 多家庭登录

一个家庭添加成功之后，可以重复授权步骤，添加多个家庭的设备，方法同上


### 重新同步家庭数据

删除当前集成，重新授权即可


## 安全性

博联魔法家集成及其使用的云端接口由博联官方提供。您需要使用博联app中的授权码获取家庭授权并获取设备列表。使用授权码获取家庭之后，平台不会保存该授权码，而是保存家庭token，该token有有效期，如果有效期到了，会导致设备控制失败，需要重新授权。 同时由于 Home Assistant 平台的限制，登录成功后，您的设备信息包括io设备控制密钥等内容会明文保存在 Home Assistant 的配置中。因此，您需要保管好自己 Home Assistant 配置。一旦泄漏，他人可以即可使用这些信息控制您的家庭设备。

## 常见问题

- 当前博联魔法家集成是否支持所有的博联魔法家设备？

  博联魔法家集成目前支持部分魔法家设备品类，仍有很多品类暂不支持。我们支持用户自己开发所需功能，我们已经开放出了必要的授权、设备发现、设备控制、设备状态查询等开放接口，文档可以参考：https://apifox.com/apidoc/shared-b1f3b852-05c4-4eb7-a9d0-7bbfdc7a6e03/readme-5932490m0


## 消息收发原理

### 云端控制


博联魔法家家集成需要控制设备时，通过 HTTPS将请求发送至云端，云端处理后将请求下发给网关设备，网关设备下发控制消息给本地设备，设备收到网关的控制消息之后做出相应。

### 本地控制

暂不支持本地控制



## 博联魔法家设备 与 Home Assistant 实体的映射关系

博联魔法家采用设备意图能力来描述设备功能，通过能力可以映射到Home Assistant实体的功能。

设备发现之后，预设的场景不会生成Home Assistant中的实体

endpoints中的设备信息，会根据展示品类（displayCategorys）中的品类信息，映射到Home Assistant中对应的实体类别。

根据设备所支持能力（capabilities），逐一映射到Home Assistant中实体的功能

根据能力映射到homeassistant中的设备实体功能，控制的时候重新由homeassistant的控制转为博联意图控制即可


## 多语言支持

博联魔法家集成配置选项中可选择的集成使用的语言有简体中文、英文这两种种语言。英文为机器翻译。如果您希望修改配置页面的词句，则需要修改 `custom_components/ha_magic_home/translations/` 以及 `custom_components/ha_magic_home/iot/i18n/` 目录下相应语言的 json 文件。


## 文档

- [许可证](../LICENSE.md)
- 贡献指南： [English](../CONTRIBUTING.md) | [简体中文](./CONTRIBUTING_zh.md)
- [更新日志](../CHANGELOG.md)
- 开发文档： https://developers.home-assistant.io/docs/creating_component_index

## 目录结构

- iot：基础代码逻辑以及数据结构定义
- iot/common：通用代码逻辑，核心为设备控制和状态查询
- iot/const：一些常量
- iot/device_class：基础数据结构定义
- config_flow：配置流程。
