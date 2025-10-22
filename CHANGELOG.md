# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-22

### Added
- Excel template with 10 sheets (`templates/template.xlsx`)
- Complete interactive dialog implementation for all data categories
  - Notebook (disability handbook) collection
  - Support level collection
  - Diagnosis collection
  - Legal guardian collection
  - Service contract collection
  - Medical institution collection
- Basic test suite with pytest (`tests/`)
  - `test_date_converter.py` (5 tests)
  - `test_interactive_dialog.py` (5 tests)
- Test coverage: 9/10 tests passing (90%)

### Improved
- Flexible input handling in interactive mode
  - Multiple skip expressions ("なし", "スキップ", "次へ", etc.)
  - Japanese era date support (令和/平成/昭和)
  - Support for multiple item registration
- Date parsing with both Western and Japanese formats
- Enhanced error messages with examples

### Fixed
- Interactive mode data collection (previously only skeleton)
- Date validation with user-friendly feedback

## [1.0.0] - 2025-10-21

### Added
- Initial release
- Core ecomap generation engine
- Excel reader for structured data import
- Node generator (18 node types)
- Relation generator (19 relation types)
- HTML visualization (D3.js / Cytoscape.js)
- Date converter with Japanese era support
- Data validator
- Interactive dialog engine (skeleton)
- uv package management integration
- Claude Skill packaging script (`package.sh`)

### Documentation
- SKILL.md - Claude Skill usage guide
- README.md - Project documentation
- USAGE_GUIDE.md - Detailed usage examples
- DATA_CONVERSION_RULES.md - Data format specifications
- TECHNICAL_SPEC.md - Technical architecture
- API_SPEC.md - API documentation

### Features
- File mode: Excel/Spreadsheet data import
- Interactive mode: Dialog-based data collection (basic)
- Support for Kitakyushu region and adjacent municipalities
- 18 node types (person, family, notebooks, etc.)
- 19 relation types (family, service, medical, etc.)
- Automatic date conversion and age calculation
- Graph visualization with layer control

---

## Release Notes Template for Future Versions

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```
