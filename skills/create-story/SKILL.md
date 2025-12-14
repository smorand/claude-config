---
name: create-ticket
description: Creates structured technical development tickets when users request ticket creation, need to write tickets, ask to generate task specifications, or mention creating development work items. Transforms oral descriptions into well-formatted tickets with technical requirements, specifications, and impact analysis for project management systems used by L'Oréal development teams.
---

# Technical Ticket Creation

When the user asks you to create a ticket, they will provide an oral description. Your role is to transform their description into a well-structured technical ticket following the template below.

## Instructions

1. Listen to the user's description and extract information for each section
2. Write the ticket in a clear, technical style appropriate for development teams
3. **Remove the "Technical Spec" section entirely if the user does not provide technical specifications**
4. The ticket will be used in project management software for a development team

## Template Structure

**Title**: [Clear, concise title describing what needs to be done]

**Technical Requirements**:
[Describe the technical context and requirements. Include:
- What needs to be implemented or changed
- Any technical constraints or dependencies
- Relevant system components or modules affected
- Prerequisites or conditions that must be met]

**Technical Spec**: *(Include this section ONLY if the user provides technical specifications)*
[Detailed technical specifications such as:
- Architecture or design details
- API contracts or interfaces
- Data models or schemas
- Implementation approach
- Code patterns or standards to follow
- Performance requirements]

**Impact**:
[Describe the expected impact of this ticket:
- Which systems, services, or components will be affected
- Potential risks or breaking changes
- Benefits or improvements delivered
- Dependencies on other teams or tickets]

## Key Guidelines

- **Be precise**: Use technical language that developers can understand and act upon
- **Focus on clarity**: Ensure requirements are unambiguous and actionable
- **Conditional sections**: Only include "Technical Spec" if the user provides that information
- **Completeness**: Ensure all provided information is captured in the appropriate section
- **Ask when needed**: If critical technical details are missing, ask the user for clarification

## Notes

- This ticket format is designed for technical implementation tasks
- Ensure the title is actionable (e.g., "Implement X", "Add Y", "Fix Z")
- The ticket should provide enough detail for a developer to start work with minimal ambiguity
