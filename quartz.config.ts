import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Akiyama's blog",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "zh-CN",
    baseUrl: "akiyama-blog.pages.dev",
    ignorePatterns: ["Private", "templates", ".obsidian", "Excalidraw"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "LXGW WenKai TC",
        body: "LXGW WenKai TC",
        code: "Fira Code",
      },
      colors: {
        lightMode: {
          light: "#f4faf7",
          lightgray: "#d9ece3",
          gray: "#b7b1aa",
          darkgray: "#4e4e4e",
          dark: "#2b2b2b",
          secondary: "#295b43",
          tertiary: "#52ad81",
          highlight: "rgba(82, 173, 129, 0.15)",
          textHighlight: "#52ad8159",
        },
        darkMode: {
          light: "#0e1411",
          lightgray: "#2b3a32",
          gray: "#66796e",
          darkgray: "#c4c3bc",
          dark: "#d9ece3",
          secondary: "#52ad81",
          tertiary: "#8fd4b1",
          highlight: "rgba(82, 173, 129, 0.18)",
          textHighlight: "#52ad8166",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.FileMerge({
        rules: [
          {
            mainFile: "index.md",
            mergeFiles: ["Thought.md"],
            separator: "\n\n---\n\n",
          },
        ],
      }),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts(), Plugin.RemovePrivates()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Disabled: 1293 OG images added ~38MB to the bundle and made the build very slow (OOM on CI)
      // Plugin.CustomOgImages(),
    ],
  },
}

export default config
