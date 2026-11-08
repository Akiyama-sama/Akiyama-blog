# AGENTS

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke: Bash("openskills read <skill-name>")
- The skill content will load with detailed instructions on how to complete the task
- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
- Each skill invocation is stateless
</usage>

<available_skills>

<skill>
<name>json-canvas</name>
<description>Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.</description>
<location>project</location>
</skill>

<skill>
<name>obsidian-bases</name>
<description>Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian.</description>
<location>project</location>
</skill>

<skill>
<name>obsidian-cli</name>
<description>Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.</description>
<location>project</location>
</skill>

<skill>
<name>obsidian-markdown</name>
<description>Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds, or Obsidian notes.</description>
<location>project</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>

## 笔记库组织方式

本目录同时是 Obsidian vault 和 Quartz 的 `content/`（站点内容源）。

### 目录约定

| 位置 | 放什么 |
|---|---|
| `index.md` | 博客首页，总入口（链接各 INDEX 与进行中项目） |
| `Thought.md` | 闪念流水：一行一条想法，行尾标日期（`YYYY-MM-DD`）；写不下一整段时才单独开 md 放 `Random/` |
| `Random/` | 杂项笔记默认归档地：技术点、八股、调研、PRD、文档等（约 1200+ 篇） |
| `Knowlege/` | 主题知识库：`计算机大类/`（网络、组成原理、操作系统、算法、软件工程、软件测试、人工智能、收集类）和 `生活杂类/`（读书、金融、政治、工具收集） |
| `Project/` | 项目 / 实习 / 比赛 / 简历类笔记 |
| `Private/` | 私人内容（意图不发布，见下方发布规则） |
| `Attachment/` | 粘贴的图片附件 |
| `Excalidraw/` | Excalidraw 画布（`*.excalidraw.md`） |
| `templates/` | Templater 模板 |
| `scripts/` | 预留脚本目录（当前为空） |

### INDEX 索引笔记

- 每个主题 / 分类配一篇 `XX - INDEX.md`：frontmatter 用 `tags: index`，正文按 `## 小节` 分组，只列 `[[wikilink]]`，不写正文。
- 面经汇总在 `Random/面试经历 - INDEX.md`；知识总索引在 `Knowlege/计算机大类/计算机大类 - INDEX.md`。

### 模板使用（Templater，新建文件时自动套用）

配置见 `.obsidian/plugins/templater-obsidian/data.json`：

| 模板 | 触发条件 | frontmatter |
|---|---|---|
| `templates/Random - Template.md` | 在 `Random/`、`Knowlege/` 下新建文件 | `date`（自动当天）、`tags`、`aliases` |
| `templates/Project - template.md` | 在 `Project/` 下新建文件 | `date`、`tags: project`、`output: false` |
| `templates/Index - template.md` | 手动（新建 INDEX 笔记时） | `date`、`tags: "#index"`、`aliases` |
| `templates/date_command.md` | 快捷键插入当前日期 | — |

常用标签写法（沿用现状）：`index`、`#pernamant`（permanent，拼写即如此）、`#literature`、`project`，以及主题词（前端、八股、CSS 等）；带 `#` 的标签直接写在 `tags:` 列表项里。

### 发布（Quartz）规则

- `quartz.config.ts` 的 `ignorePatterns: ["Private", "templates", ".obsidian", "Excalidraw"]` + filters：frontmatter 带 `draft: true` 或 `private: true` 的笔记不发布（注意 `ignorePatterns` 区分大小写，须与目录名大小写一致）。
- 单篇笔记不想发布时，直接加 `private: true` frontmatter。
- `output: false`（Project 模板里）当前 Quartz 不读取，仅作约定标记，不影响发布。

