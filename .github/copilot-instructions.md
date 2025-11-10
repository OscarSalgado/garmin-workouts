# Clean Code Code Review Guidelines

When reviewing code, adhere to the following principles derived from Uncle Bob's Clean Code:

## Meaningful Names

- Use descriptive and unambiguous names.
- Avoid abbreviations unless they are widely understood.
- Use pronounceable names and maintain consistent naming conventions.

## Small Functions

- Ensure functions are small and perform a single task.
- Avoid flag arguments and side effects.
- Each function should operate at a single level of abstraction.

## Single Responsibility Principle

- Each class or function should have only one reason to change.
- Separate concerns and encapsulate responsibilities appropriately.

## Clean Formatting

- Use consistent indentation and spacing.
- Separate code blocks with new lines where needed for readability.

## Avoid Comments

- Write self-explanatory code that doesn’t require comments.
- Use comments only to explain complex logic or public APIs.

## Error Handling

- Use exceptions rather than return codes.
- Avoid catching generic exceptions.
- Fail fast and handle exceptions at a high level.

## Avoid Duplication

- Extract common logic into functions or classes.
- DRY – Don’t Repeat Yourself.

## Code Smells to Flag

- Long functions
- Large classes
- Deep nesting
- Primitive obsession
- Long parameter lists
- Magic numbers or strings
- Inconsistent naming

## Review Style

- Maintain a strict but constructive tone.
- Use bullet points to list issues.
- Provide alternatives and improved code suggestions.