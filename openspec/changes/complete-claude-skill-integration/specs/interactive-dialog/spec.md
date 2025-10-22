# Interactive Dialog Capability

## ADDED Requirements

### Requirement: Interactive Dialog Engine
The system SHALL provide an interactive dialog engine that collects ecomap data through a conversational interface with Claude Desktop users.

#### Scenario: Start new ecomap creation session
- **WHEN** user requests "田中一郎さんのエコマップを作成してください" in Claude Desktop
- **THEN** system initiates interactive dialog session
- **AND** system responds with initial greeting and overview
- **AND** system begins collecting person information

#### Scenario: Collect person information
- **WHEN** system is in COLLECT_PERSON state
- **THEN** system asks for name, birth date, gender
- **AND** system validates each input before proceeding
- **AND** system provides helpful examples for date formats

#### Scenario: Collect family information
- **WHEN** person information is complete
- **THEN** system transitions to COLLECT_FAMILY state
- **AND** system asks "ご家族の情報を教えてください"
- **AND** system collects name, relation, living together status for each family member
- **AND** system allows adding multiple family members

#### Scenario: Collect notebook information
- **WHEN** family information collection is complete or skipped
- **THEN** system transitions to COLLECT_NOTEBOOK state
- **AND** system asks for disability certificate information
- **AND** system supports 療育手帳, 精神保健福祉手帳, 身体障害者手帳
- **AND** system validates certificate number format

#### Scenario: Input validation with feedback
- **WHEN** user provides invalid date format
- **THEN** system responds with clear error message
- **AND** system provides examples of valid formats
- **AND** system asks for the input again

#### Scenario: Skip optional sections
- **WHEN** user responds "なし" or "スキップ" for optional sections
- **THEN** system acknowledges and moves to next section
- **AND** system continues without requiring that information

### Requirement: State Management
The system SHALL maintain conversation state throughout the data collection process.

#### Scenario: Track collection progress
- **WHEN** collecting data through multiple conversation turns
- **THEN** system maintains state of which sections are complete
- **AND** system can display progress (e.g., "3/7ステップ完了")
- **AND** system prevents duplicate data collection

#### Scenario: Resume after interruption
- **WHEN** conversation is interrupted and resumed
- **THEN** system recalls previously collected data
- **AND** system continues from last incomplete section
- **AND** system allows user to review and modify previous inputs

### Requirement: Data Validation
The system SHALL validate all user inputs according to ecomap data requirements.

#### Scenario: Validate required fields
- **WHEN** required field is empty
- **THEN** system responds with specific error message
- **AND** system re-prompts for the required information
- **AND** system does not proceed until valid input received

#### Scenario: Validate date formats
- **WHEN** user provides date in various formats
- **THEN** system accepts "2025-10-21", "2025/10/21", "令和7年10月21日"
- **AND** system normalizes to YYYY-MM-DD format internally
- **AND** system rejects invalid dates with clear feedback

#### Scenario: Validate enum values
- **WHEN** user provides gender information
- **THEN** system accepts "男", "女", "その他"
- **AND** system rejects invalid values
- **AND** system suggests valid options

### Requirement: User Feedback
The system SHALL provide clear, helpful feedback throughout the conversation.

#### Scenario: Provide input examples
- **WHEN** asking for date input
- **THEN** system includes example: "例: 2025-10-21 または 令和7年10月21日"
- **AND** examples are relevant to Japanese context

#### Scenario: Confirm collected data
- **WHEN** section is complete
- **THEN** system summarizes collected data
- **AND** system asks for confirmation
- **AND** system allows corrections before proceeding

#### Scenario: Display progress indicators
- **WHEN** multi-step collection is in progress
- **THEN** system displays current step (e.g., "ステップ2/7: 家族情報")
- **AND** system shows which sections remain

### Requirement: Generate Ecomap from Dialog
The system SHALL convert collected dialog data into ecomap JSON and HTML outputs.

#### Scenario: Complete data collection and generate
- **WHEN** all required sections are collected
- **THEN** system converts dialog data to internal format
- **AND** system generates JSON file
- **AND** system generates HTML visualization
- **AND** system provides download links or file paths

#### Scenario: Handle partial data
- **WHEN** user skips optional sections
- **THEN** system generates ecomap with available data
- **AND** system includes only non-empty sections in output
- **AND** generated visualization reflects actual data provided
