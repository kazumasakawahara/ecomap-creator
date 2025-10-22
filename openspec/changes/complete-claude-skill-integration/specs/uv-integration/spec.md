# UV Integration Capability

## ADDED Requirements

### Requirement: UV Package Management
The system SHALL use uv for Python package management following PEP 621 standards.

#### Scenario: Project configuration with pyproject.toml
- **WHEN** project is initialized
- **THEN** pyproject.toml file exists in project root
- **AND** file contains valid PEP 621 metadata
- **AND** file specifies Python version requirement >=3.9
- **AND** file lists all required dependencies

#### Scenario: Install dependencies with uv
- **WHEN** user runs `uv sync`
- **THEN** uv installs all dependencies from pyproject.toml
- **AND** uv creates uv.lock file for reproducible installs
- **AND** installation completes without errors

#### Scenario: Run ecomap-creator with uv
- **WHEN** user runs `uv run ecomap-creator`
- **THEN** uv executes the main script
- **AND** script has access to all dependencies
- **AND** command works without prior `uv sync`

### Requirement: Project Metadata
The system SHALL define comprehensive project metadata in pyproject.toml.

#### Scenario: Basic metadata fields
- **WHEN** reading pyproject.toml
- **THEN** file contains name = "ecomap-creator"
- **AND** file contains version number
- **AND** file contains description in Japanese
- **AND** file contains author information
- **AND** file contains license information

#### Scenario: Python version specification
- **WHEN** checking Python requirements
- **THEN** pyproject.toml specifies requires-python = ">=3.9"
- **AND** uv enforces this requirement during installation

### Requirement: Dependency Specification
The system SHALL declare all runtime dependencies in pyproject.toml.

#### Scenario: Core dependencies
- **WHEN** listing dependencies
- **THEN** pyproject.toml includes openpyxl>=3.1.5
- **AND** version constraints are specified
- **AND** dependencies are minimal (no unnecessary packages)

#### Scenario: Optional dependencies
- **WHEN** future features require additional packages
- **THEN** optional dependencies can be defined in [project.optional-dependencies]
- **AND** users can install them with `uv sync --extra <group>`

### Requirement: Script Entry Points
The system SHALL define command-line entry points using PEP 517.

#### Scenario: Main entry point
- **WHEN** pyproject.toml defines [project.scripts]
- **THEN** ecomap-creator command is mapped to ecomap_creator:main
- **AND** `uv run ecomap-creator` executes the main function
- **AND** command is available after installation

#### Scenario: Entry point with arguments
- **WHEN** user runs `uv run ecomap-creator sample.xlsx`
- **THEN** command passes arguments to main function
- **AND** file mode is activated
- **AND** ecomap is generated from Excel file

### Requirement: Lock File Management
The system SHALL use uv.lock for reproducible dependency resolution.

#### Scenario: Generate lock file
- **WHEN** developer runs `uv lock`
- **THEN** uv.lock file is created
- **AND** file contains exact versions of all dependencies
- **AND** file includes transitive dependencies

#### Scenario: Install from lock file
- **WHEN** user runs `uv sync`
- **THEN** uv installs exact versions from uv.lock
- **AND** installation is reproducible across environments
- **AND** no dependency resolution conflicts occur

### Requirement: Build System Configuration
The system SHALL configure modern Python build system.

#### Scenario: Hatchling build backend
- **WHEN** pyproject.toml defines [build-system]
- **THEN** build-backend = "hatchling.build"
- **AND** requires = ["hatchling"]
- **AND** package can be built with `uv build`

#### Scenario: Package distribution
- **WHEN** building distribution
- **THEN** `uv build` creates wheel and sdist
- **AND** packages include all necessary files
- **AND** packages exclude __pycache__ and .pyc files

### Requirement: Backwards Compatibility
The system SHALL maintain compatibility with traditional pip workflows.

#### Scenario: requirements.txt preservation
- **WHEN** requirements.txt exists
- **THEN** file lists same dependencies as pyproject.toml
- **AND** users can still use `pip install -r requirements.txt`
- **AND** file is kept in sync with pyproject.toml

#### Scenario: Migration path
- **WHEN** users migrate from pip to uv
- **THEN** existing workflows continue to work
- **AND** documentation explains both installation methods
- **AND** no breaking changes to existing installations
