# Quartz Project Guidelines

This repository is based on [Quartz](https://quartz.jzhao.xyz/), a static site generator. It uses TypeScript, Preact, and Node.js.

## 1. Build, Lint, and Test Commands

*   **Development Server / Build:**
    ```bash
    npx quartz build --serve
    ```
    To build into a specific directory (e.g., `docs`):
    ```bash
    npx quartz build --serve -d docs
    ```

*   **Linting & Type Checking:**
    ```bash
    npm run check
    ```
    This runs `tsc --noEmit` (for type safety) and `prettier . --check` (for formatting).

*   **Formatting:**
    ```bash
    npm run format
    ```
    This runs `prettier . --write` to fix formatting issues.

*   **Testing:**
    *   **Run all tests:**
        ```bash
        npm test
        ```
    *   **Run a single test:**
        ```bash
        npx tsx --test path/to/file.test.ts
        ```
        Example: `npx tsx --test quartz/util/path.test.ts`

## 2. Code Style & Conventions

### General
*   **Language:** TypeScript (Strict mode enabled).
*   **Formatter:** Prettier. Always run `npm run format` before committing.
*   **Imports:** Use explicit relative imports. Avoid wildcards.

### Components (Preact)
*   **Location:** `quartz/components/`
*   **Framework:** Preact (use `class` instead of `className`).
*   **Type Definition:** Components should be typed as `QuartzComponent`.
*   **Props:** Use `QuartzComponentProps` for component props.
*   **Export Pattern:** Use the factory pattern with `satisfies`:
    ```typescript
    export default (() => MyComponent) satisfies QuartzComponentConstructor
    ```
*   **Styling:** Attach CSS directly to the component if needed:
    ```typescript
    MyComponent.css = `
    .my-class {
      color: red;
    }
    `
    ```
*   **Conditional Rendering:** Use standard JavaScript conditionals (`if`, ternary).

### Plugins
*   **Location:** `quartz/plugins/`
*   **Types:** Implement `QuartzTransformerPlugin` or `QuartzEmitterPlugin`.
*   **Options Pattern:**
    ```typescript
    interface Options { ... }
    const defaultOptions: Options = { ... }
    export const MyPlugin: QuartzTransformerPlugin<Partial<Options>> = (userOpts) => {
      const opts = { ...defaultOptions, ...userOpts }
      return {
        name: "MyPlugin",
        // ... implementation
      }
    }
    ```

### Testing
*   **Runner:** `node:test` (via `tsx`).
*   **File Naming:** `*.test.ts`.
*   **Location:** Co-located with the code (e.g., `quartz/util/path.ts` -> `quartz/util/path.test.ts`).

## 3. Project Structure
*   `quartz/`: Core application logic.
    *   `components/`: UI components (Preact).
    *   `plugins/`: Build-time plugins (transformers, emitters).
    *   `util/`: Utility functions.
*   `content/`: Markdown content for the site.
*   `quartz.config.ts`: Main configuration file.
*   `quartz.layout.ts`: Layout configuration.

## 4. Cursor/Copilot Rules
*   No specific `.cursorrules` or `.github/copilot-instructions.md` found.
*   Follow the conventions strictly, especially the `satisfies QuartzComponentConstructor` export pattern for components, as this is critical for Quartz's dependency injection system.
