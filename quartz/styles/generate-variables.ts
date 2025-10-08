import { variables } from "./variables"
import fs from "fs"
import path from "path"
import { fileURLToPath } from "url"

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

/**
 * Generates and writes the SCSS variables file to disk
 * @throws Error if file writing fails
 */
export function generateScss(): void {
  try {
    const outputPath = path.join(__dirname, "variables.scss")
    const scss = generateScssContent()
    fs.writeFileSync(outputPath, scss)
  } catch (error) {
    console.error("Error generating SCSS variables:", error)
    throw error
  }
}

const generateScssContent = (): string => {
  let scss = "// This file is auto-generated. Do not edit directly.\n\n"

  const mapping = generateScssRecord()
  for (const [key, value] of Object.entries(mapping)) {
    scss += `$${key}: ${value};\n`
  }

  return scss
}

/**
 * Generates a record of SCSS variables from the variables object
 * @returns Record mapping kebab-case variable names to their string values
 */
export function generateScssRecord(): Record<string, string> {
  return Object.fromEntries(
    Object.entries(variables).map(([key, value]) => {
      const kebabKey = toKebabCase(key)
      const valString =
        typeof value === "number" && !unitlessKeys.has(kebabKey) ? `${value}px` : String(value)
      return [kebabKey, valString]
    }),
  )
}
// Convert camelCase to kebab-case
const toKebabCase = (str: string): string => {
  return str.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase()
}

const unitlessKeys = new Set([
  "bold-weight",
  "semi-bold-weight",
  "normal-weight",
  "font-scale-factor",
])