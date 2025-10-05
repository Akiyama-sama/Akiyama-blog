import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"


// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header:[
    Component.Flex({
      components: [
        {
          Component:Component.PageTitle(),
          align:"start",
          grow:true,
        },
        {
          Component: Component.Search(),
          align:"end",
          grow: true,
        },
        { Component: Component.Darkmode(),
          align:"end",
        },
        { Component: Component.ReaderMode(),
          align:"end",
        },
      ],
    }),
  ],
  afterBody: [
    Component.Flex({
      components: [
        {
          Component: Component.Backlinks(),
          align:"end",
        },
      ],
    }),
  ],
  footer: Component.Footer({
    links: {
      GitHub主页: "https://github.com/Akiyama-sama",
      X主页: "https://x.com/lchngy502188733",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.Flex({
      components: [
        {
          Component: Component.MobileOnly(Component.Spacer()),
          align:"center",
        },
        {
          Component: Component.Explorer(),
          align:"center",
        },
      ],
    })
  ],
  right: [
    Component.Flex({
      components: [
        {
          Component: Component.DesktopOnly(Component.TableOfContents()),
          align:"center",
        },
      ],
    }),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.MobileOnly(Component.Spacer()),
    Component.Explorer(),
  ],
  right: [],
}
