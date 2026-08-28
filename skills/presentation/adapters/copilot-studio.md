# Microsoft Copilot Studio adapter

Use Copilot/Teams as the interaction layer, SharePoint for versioned knowledge/assets, Dataverse for task/run state, and Power Automate for deterministic gates and actions. A small approved Azure Function or container may render PPTX when the tenant permits it.

## Mapping

| Portable contract | Microsoft-native implementation |
| --- | --- |
| Skill package and brand assets | SharePoint versioned library |
| Task/run state and approvals | Dataverse |
| Deterministic workflow and gates | Power Automate |
| Semantic decisions | Copilot Studio agent |
| PPTX rendering | Approved Function/container or certified Office template flow |
| Human review | Teams/Approvals and Dataverse record |

Copilot must emit the same Slide Specification schema. Power Automate validates it before rendering. Monday.com, when present, remains process UI/trigger/status and must not become the memory or rendering runtime.

If the tenant has only a declarative M365 Copilot agent and no deterministic workflow/runtime, label the result `assistive-draft`; do not claim certified reproducibility.
