# 贡献指南

[English](./CONTRIBUTING.md) | [简体中文](./doc/CONTRIBUTING_zh.md)

感谢您考虑为我们的项目做出贡献！您的努力将使我们的项目变得更好。

在您开始贡献之前，请花一点时间阅读以下准则：

## 我可以如何贡献？

### 报告问题

如果您在项目中遇到错误，请在 GitHub 上[报告问题](https://github.com/ibroadlink/ha_magic_home/issues/new/)，并提供关于错误的详细信息，包括复现步骤、 debug 级日志以及错误出现的时间。

集成开启 debug 级日志的[方法](https://www.home-assistant.io/integrations/logger/#log-filters)：

```
# configuration.yaml 设置打印日志等级

logger:
  default: critical
  logs:
    custom_components.ha_magic_home: debug
```

### 建议增强功能

如果您有增强或新功能的想法，欢迎您在 GitHub 讨论区[创建想法](https://github.com/ibroadlink/ha_magic_home/discussions/new?category=ideas) 。我们期待您的建议！

### 贡献代码

1. Fork 该仓库并从 `main` 创建您的分支。
2. 确保您的代码符合项目的编码规范。
3. 确保您的提交消息描述清晰。
4. 提交请求应附有明确的问题描述和解决方案。
5. 如果必要，请更新文档。

## 拉取请求准则

在提交拉取请求之前，请确保满足以下要求：

- 您的拉取请求解决了单个问题或功能。
- 您已在本地测试过您的更改。
- 任何依赖更改都有文档说明。


## Commit Message 格式

```
<type>: <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

type ：有以下几种变更类型

- feat：新增功能。
- fix：修复问题。
- docs：仅仅修改了文档。
- style：仅仅是对格式进行修改，如逗号、缩进、空格等，不改变代码逻辑。
- refactor：代码重构，没有新增功能或修复问题。
- perf：优化性能。
- test：增加或修改测试用例。
- chore：修改编译流程，或变更依赖库和工具等。
- revert：版本回滚。

subject ：简洁的标题，描述本次提交的概要。使用祈使句、现在时态，首字母小写，结尾不加句号。

body ：描述本次提交的详细内容，解释为什么需要这些变更。除 docs 之外的变更类型必须包含 body。

footer ：（可选）关联的 issue 或 pull request 编号。

## 许可

在为本项目做出贡献时，您同意您的贡献遵循本项目的[许可证](../LICENSE.md) 。

## 获取帮助

如果您需要帮助或有疑问，可在 GitHub 的[讨论区](https://github.com/ibroadlink/ha_magic_home/discussions/)询问。
