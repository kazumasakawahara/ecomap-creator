# Skill Metadata Capability

## MODIFIED Requirements

### Requirement: SKILL.md YAML Frontmatter
The SKILL.md file SHALL include YAML frontmatter with required Claude Skill metadata.

#### Scenario: Valid YAML frontmatter structure
- **WHEN** SKILL.md is parsed by Claude Desktop
- **THEN** file begins with `---` delimiter
- **AND** file contains valid YAML metadata block
- **AND** file ends YAML block with `---` delimiter
- **AND** YAML block precedes all markdown content

#### Scenario: Required metadata fields
- **WHEN** validating SKILL.md frontmatter
- **THEN** `name` field exists with value "ecomap-creator"
- **AND** name is 64 characters or less
- **AND** `description` field exists with Japanese description
- **AND** description is 200 characters or less
- **AND** description clearly explains skill purpose

#### Scenario: Optional metadata fields
- **WHEN** SKILL.md includes optional fields
- **THEN** `version` field follows semantic versioning (e.g., "1.0.0")
- **AND** `dependencies` field lists required software
- **AND** dependencies include uv, Python version

### Requirement: Skill Description
The SKILL.md SHALL provide clear, comprehensive usage instructions for Claude Desktop users.

#### Scenario: Interactive mode documentation
- **WHEN** user reads SKILL.md
- **THEN** document explains interactive dialog mode
- **AND** document provides example conversation flow
- **AND** document lists types of information collected
- **AND** document explains when to use interactive vs file mode

#### Scenario: File mode documentation
- **WHEN** user reads SKILL.md
- **THEN** document explains Excel template usage
- **AND** document maintains existing usage examples
- **AND** document provides command-line examples
- **AND** backward compatibility is documented

#### Scenario: Installation instructions
- **WHEN** user needs to install skill
- **THEN** SKILL.md includes uv installation steps
- **AND** document explains Claude Desktop upload process
- **AND** document includes troubleshooting section
- **AND** document lists system requirements

## ADDED Requirements

### Requirement: Claude Skill Integration
The skill SHALL be packaged as a valid Claude Skill for Claude Desktop.

#### Scenario: Skill directory structure
- **WHEN** skill is packaged
- **THEN** root directory contains SKILL.md
- **AND** directory contains pyproject.toml
- **AND** directory contains all Python modules
- **AND** directory contains templates and samples
- **AND** directory excludes __pycache__ and .pyc files

#### Scenario: ZIP package creation
- **WHEN** creating distribution package
- **THEN** ZIP file contains skill directory as root
- **AND** ZIP includes all necessary files
- **AND** ZIP excludes development files (.git, .DS_Store, etc.)
- **AND** ZIP file naming follows ecomap-creator-vX.Y.Z.zip pattern

#### Scenario: Upload to Claude Desktop
- **WHEN** user uploads skill ZIP to Claude Desktop
- **THEN** Claude recognizes skill from YAML frontmatter
- **AND** skill appears in skills list
- **AND** skill can be activated/deactivated
- **AND** skill description is displayed correctly

### Requirement: Version Management
The skill SHALL maintain consistent version numbers across all files.

#### Scenario: Version synchronization
- **WHEN** releasing new version
- **THEN** pyproject.toml version matches SKILL.md version
- **AND** CHANGELOG.md includes version entry
- **AND** ZIP filename includes version number
- **AND** all version references are consistent

#### Scenario: Semantic versioning
- **WHEN** incrementing version
- **THEN** major version changes for breaking changes
- **AND** minor version changes for new features
- **AND** patch version changes for bug fixes
- **AND** version follows MAJOR.MINOR.PATCH format

### Requirement: Usage Examples
The SKILL.md SHALL provide practical, region-specific examples.

#### Scenario: Kitakyushu region examples
- **WHEN** documentation provides examples
- **THEN** examples use Kitakyushu-area municipality names
- **AND** examples include realistic Japanese names
- **AND** examples reflect actual support workflows
- **AND** examples cover multiple use cases (young, middle-aged, elderly)

#### Scenario: Interactive mode example
- **WHEN** showing interactive conversation
- **THEN** example demonstrates natural Japanese dialogue
- **AND** example shows complete data collection flow
- **AND** example includes validation and feedback
- **AND** example shows final output generation

#### Scenario: File mode example
- **WHEN** showing Excel file usage
- **THEN** example references sample files
- **AND** example shows command-line invocation
- **AND** example explains expected output
- **AND** example maintains compatibility with existing docs
