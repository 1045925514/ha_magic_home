# Guidelines for Contributing

[English](./CONTRIBUTING.md) | [Simplified Chinese](./doc/CONTRIBUTING_zh.md)

Thank you for considering contributing to our program! Your efforts will make our project better.

Before you start contributing, please take a moment to read the following guidelines:

### How can I contribute?

### Report a problem

If you encounter a bug in your project, please [report the issue](https://github.com/ibroadlink/ha_magic_home/issues/new/) on GitHub and provide detailed information about the bug, including steps to reproduce it, debug-level logging, and when the bug appeared.

Integrate a [method](https://www.home-assistant.io/integrations/logger/#log-filters) for turning on debug-level logging:

```
# configuration.yaml set print logging level

logger: default: critical
  default: critical
  logs.
    custom_components.ha_magic_home: debug
```

### Suggested enhancements

If you have an idea for an enhancement or new feature, feel free to [create idea](https://github.com/ibroadlink/ha_magic_home/discussions/new?category=ideas) in the GitHub discussion forum. We look forward to your suggestions!

### Contribute code

1. Fork the repository and create your branch from `main`. 2.
2. Make sure your code conforms to the project's coding specification. 3.
3. Make sure your commit message is clearly described. 4.
4. The commit request should be accompanied by a clear description of the problem and its solution. 5.
5. Update the documentation if necessary. 6.

## Pull Request Guidelines

Before submitting a pull request, make sure the following requirements are met:

- Your pull request solves a single problem or feature.
- You have tested your changes locally.
- Any dependency changes are documented.

## Commit Message format

```
<type>: <subject>
<BLANK LINE
<body
<BLANK LINE
<footer
```

type : There are several types of changes

- feat: add a new feature.
- fix: fixes a problem.
- docs: only modifies the document.
- style: only formatting changes, such as commas, indentation, spaces, etc., without changing the code logic.
- refactor: refactoring the code without adding new features or fixing problems.
- perf: optimize performance.
- test: add or modify test cases.
- chore: modify the compilation process, or change dependent libraries and tools.
- revert: version rollback.

subject: A concise title describing the summary of the commit. Use imperative, present tense, lowercase initial letters, and no period at the end.

body ：Description of the details of the commit, explaining why the changes are needed. Change types other than docs must include body.

footer: (optional) The number of the associated issue or pull request.

## License

By contributing to the Project, you agree that your contribution follows the Project's [LICENSE] (.../LICENSE.md). /LICENSE.md).

## Getting Help

If you need help or have questions, ask in the GitHub [discussion forum](https://github.com/ibroadlink/ha_magic_home/discussions/).
