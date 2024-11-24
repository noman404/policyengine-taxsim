# PolicyEngine-TAXSIM

A TAXSIM emulator using the PolicyEngine US federal and state tax calculator.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
  - [From Source](#from-source)
  - [From PyPI](#from-pypi)
- [Usage](#usage)
- [Input Variables](#input-variables)
  - [Demographics](#demographics)
  - [Income](#income)
  - [Supported Output Type](#Supported output types as like taxsim)
  - [Supported Households](#Supported household types)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

This project provides an emulator for TAXSIM-35, utilizing PolicyEngine's US federal and state tax calculator. It processes tax calculations through a CSV input format compatible with TAXSIM-35 specifications.

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/PolicyEngine/policyengine-taxsim.git
   cd policyengine-taxsim
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```
3. To update the project codebase (for existing project)
    ```bash
   git pull origin main
   ```

4. To update dependencies used by the project (for existing project):
   ```bash
   pip install -e . --upgrade
   ```

### From PyPI

```bash
pip install git+https://github.com/PolicyEngine/policyengine-taxsim.git
```

## Usage

Run the simulation by providing your input CSV file:

```bash
python policyengine_taxsim/cli.py your_input_file.csv
```

The output will be generated as `output.csv` in the same directory.

## Input Variables

The emulator accepts CSV files with the following variables:

### Demographics

| Variable  | Description                     | Notes                                    |
|-----------|--------------------------------|------------------------------------------|
| taxsimid  | Unique identifier              |                                          |
| year      | Tax year                       |                                          |
| state     | State code                     |                                          |
| mstat     | Marital status                 | Only supports: 1 (single), 2 (joint)     |
| page      | Primary taxpayer age           |                                          |
| sage      | Spouse age                     |                                          |
| depx      | Number of dependents           |                                          |
| age1      | First dependent's age          |                                          |
| age2      | Second dependent's age         |                                          |
| ageN      | Nth dependent's age            |                                          |

### Income

| Variable  | Description                     |
|-----------|--------------------------------|
| pwages    | Primary taxpayer wages         |
| swages    | Spouse wages                   |

### Supported output types as like taxsim

Depending on the idtl input value it can generate output types as following

| idtl | Description     |
|------|-----------------|
| 0    | Standard output |
| 2    | Full output     |

### Supported household types

| Supported household types                                   |
|----------------------------------------|
| Single                                 |
| Joint                                  |
| Household with Dependent               |
| Household with Dependent single parent |


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License 
[MIT License](https://github.com/PolicyEngine/policyengine-taxsim?tab=License-1-ov-file#)

## Support

For issues and feature requests, please [open an issue](https://github.com/PolicyEngine/policyengine-taxsim/issues).