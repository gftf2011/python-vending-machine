<div align="center">
	<h1>(STUDY) CLEAN Python Vending Machine • :snake: :computer:</h1>
</div>

<br/>

<div align="center">
  <a href="#page_facing_up-about">About</a> •
  <a href="#hammer_and_wrench-supported-os">Supported OS</a> • 
  <a href="#large_blue_diamond-design-patterns">Design Patterns</a> •
  <a href="#blue_book-principles">Principles</a> •
  <a href="#clipboard-required-tools">Required Tools</a> •
  <a href="#racing_car-running-project">Running Project</a> •
  <a href="#test_tube-running-tests">Running Tests</a> •
  <a href="#memo-license">License</a>
</div>

<br/>

<div align="center">
  <img src="https://github.com/gftf2011/python-vending-machine/blob/main/.github/images/background.png" />
</div>

<br/>

## :page_facing_up: About

This a LLD (Low Level Design) Code backend from a Vending Machine made with python.

The objective from this project is to show how to create an API with a well-defined and decoupled architecture, using Clean Architecture concepts, dividing the layers responsibility and exploring the usage of several design patterns !

We will be exploring many advanced concepts of databases such as partitioning and CRON jobs !

<br/>

## :hammer_and_wrench: Supported OS

- [x] Mac OS
- [x] Linux
- [x] Windows - WSL

<br/>

## :large_blue_diamond: Design Patterns

### Creational

- [Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)
- [Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Builder](https://refactoring.guru/design-patterns/builder)
- [Singleton](https://refactoring.guru/design-patterns/singleton)

### Structural

- [Adapter](https://refactoring.guru/design-patterns/adapter)
- [Decorator](https://refactoring.guru/design-patterns/decorator)

<br/>

## :blue_book: Principles

- [Single Responsibility Principle (SRP)](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Open Closed Principle (OCP)](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)
- [Liskov Substitution Principle (LSP)](https://en.wikipedia.org/wiki/Liskov_substitution_principle)
- [Interface Segregation Principle (ISP)](https://en.wikipedia.org/wiki/Interface_segregation_principle)
- [Dependency Inversion Principle (DIP)](https://en.wikipedia.org/wiki/Dependency_inversion_principle)
- [Separation of Concerns (SOC)](https://en.wikipedia.org/wiki/Separation_of_concerns)
- [Don't Repeat Yourself (DRY)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
- [You Aren't Gonna Need It (YAGNI)](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it)
- [Keep It Simple, Stupid (KISS)](https://en.wikipedia.org/wiki/KISS_principle)
- [Composition Over Inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)

<br/>

## :clipboard: Required Tools

- [x] Python - [https://www.python.org/](https://www.python.org/)
  - Python version: 3.12.4
- [x] Docker - [https://www.docker.com/](https://www.docker.com/)

<br/>

## :racing_car: Running Project

```sh
  $ python -m pip install --upgrade pip
  $ pip install poetry==1.8.3
  $ poetry install --no-root
  $ ./cmds/run_dev.sh
```

### OBS.: Ensure to install all dependencies in <a href="#clipboard-required-tools">Required Tools</a>

<br/>

## :test_tube: Running Tests

> ### Unit Tests

```sh
  $ ./cmds/test_unit.sh
```

> ### Integration Tests

```sh
  $ ./cmds/test_integration.sh
```

> ### E2E Tests

```sh
  $ ./cmds/test_e2e.sh
```

> ### Full Test Coverage Report

```sh
  $ ./cmds/test_all.sh
```

<br/>

## :memo: License

This project is under MIT license. See the [LICENSE](https://github.com/gftf2011/python-vending-machine/blob/main/LICENSE) file for more details.

---

Made with lots of :heart: by [Gabriel Ferrari Tarallo Ferraz](https://www.linkedin.com/in/gabriel-ferrari-tarallo-ferraz/)
