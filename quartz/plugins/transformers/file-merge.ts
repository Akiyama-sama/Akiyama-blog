import { QuartzTransformerPlugin } from "../types"
import fs from "fs"
import path from "path"
import matter from "gray-matter"
import { Root, BlockContent, DefinitionContent } from "mdast"
import { VFile } from "vfile"
import { unified } from "unified"
import remarkParse from "remark-parse"

export interface FileMergeRule {
  // 主文件路径（相对于 content 目录，如 "index.md"）
  mainFile: string

  // 要合并的文件列表（相对于 content 目录，按顺序追加到主文件末尾）
  mergeFiles: string[]

  // 合并时的分隔符（默认为两个换行符）
  separator?: string

  // 是否剥离被合并文件的 frontmatter（默认 true）
  stripFrontmatter?: boolean
}

export interface Options {
  // 合并规则数组
  rules: FileMergeRule[]
}

const defaultOptions: Options = {
  rules: [],
}

/**
 * 标准化路径用于比较
 * 支持输入格式：
 * - "index.md"
 * - "./index.md"
 * - "content/index.md"
 * 统一输出为相对于 content 目录的路径，如 "index.md"
 */
function normalizePath(filePath: string): string {
  return filePath
    .replace(/^\.\//, "") // 移除开头的 ./
    .replace(/^content\//, "") // 移除开头的 content/
    .replace(/\\/g, "/") // 统一使用正斜杠（Windows 兼容）
}

/**
 * FileMerge Plugin
 *
 * 在构建时将多个 Markdown 文件合并为一个，而不修改原始文件。
 *
 * @example
 * ```typescript
 * Plugin.FileMerge({
 *   rules: [
 *     {
 *       mainFile: "index.md",
 *       mergeFiles: ["Thought.md"],
 *       separator: "\n\n---\n\n"
 *     }
 *   ]
 * })
 * ```
 */
export const FileMerge: QuartzTransformerPlugin<Partial<Options>> = (userOpts) => {
  const opts = { ...defaultOptions, ...userOpts }

  // 构建查找 Map 用于 O(1查找
  const rulesMap = new Map<string, FileMergeRule>()
  opts.rules.forEach((rule) => {
    const normalizedMainFile = normalizePath(rule.mainFile)
    rulesMap.set(normalizedMainFile, rule)
  })

  return {
    name: "FileMerge",
    markdownPlugins(ctx) {
      const { argv } = ctx

      return [
        () => {
          // 返回 transformer 函数
          return (tree: Root, file: VFile) => {
            // file.path 由 read() 设置，计算相对路径
            if (!file.path) return tree

            const currentRelativePath = path.posix.relative(argv.directory, file.path as string)
            const normalizedPath = normalizePath(currentRelativePath)
            const rule = rulesMap.get(normalizedPath)

            if (!rule) return tree // 不需要合并

            // 读取需要合并的文件并解析为 AST
            const mergeContents: string[] = []

            for (const mergeFile of rule.mergeFiles) {
              const normalizedMergeFile = normalizePath(mergeFile)
              const filePath = path.join(argv.directory, normalizedMergeFile)

              if (fs.existsSync(filePath)) {
                let content = fs.readFileSync(filePath, "utf-8").trim()

                // 如果需要剥离 frontmatter（默认剥离）
                if (rule.stripFrontmatter !== false) {
                  const parsed = matter(content)
                  content = parsed.content.trim()
                }

                if (content) {
                  mergeContents.push(content)
                }
              } else {
                console.warn(
                  `[FileMerge] File not found for merging into "${rule.mainFile}": ${filePath}`,
                )
              }
            }

            // 如果有内容需要合并
            if (mergeContents.length > 0) {
              const separator = rule.separator ?? "\n\n"

              // 将每个合并文件解析为 AST 节点
              const parser = unified().use(remarkParse)

              for (const content of mergeContents) {
                const separatorTree = parser.parse(separator) as Root
                const contentTree = parser.parse(content) as Root

                // 将分隔符和内容添加到主文件的 AST 中
                tree.children.push(
                  ...(separatorTree.children as (BlockContent | DefinitionContent)[]),
                )
                tree.children.push(
                  ...(contentTree.children as (BlockContent | DefinitionContent)[]),
                )
              }
            }

            return tree
          }
        },
      ]
    },
  }
}
