import { QuartzFilterPlugin } from "../types"

export const RemovePrivates: QuartzFilterPlugin<{}> = () => ({
  name: "RemovePrivates",
  shouldPublish(_ctx, [_tree, vfile]) {
    const privateFlag: boolean =
      vfile.data?.frontmatter?.private === true || vfile.data?.frontmatter?.private === "true"
    return !privateFlag
  },
})
