---
tags:
  - '#pernamant'
---

好的，我们以你提供的这个 LRC 文件为例，一步步模拟 `parseLyrics` 函数 的执行过程，看看它是如何将这个文件的信息转换成 `LyricsData` 对象的。

**示例 LRC 文件内容 (节选关键部分):**

```lrc
[offset:0]
[offset:0]
[offset:0]
[00:00.00][ti:アスノヨゾラ哨戒班。明日的夜空哨戒班]
[00:00.00][ar:Akie秋绘/夏璃夜]
[00:00.00][al:春雫。2017]
[00:00.00][by:]
[00:00.00][kana:11111111...]
[00:00.00]アスノヨゾラ哨戒班。明日的夜空哨戒班 - Akie秋绘/夏璃夜
[00:00.00]//
[00:01.36]词：Orangestar
[00:01.36]//
[00:02.73]曲：Orangestar
[00:02.73]//
[00:04.09]//
[00:04.10]编曲：Orangestar/鈴木秋則
[00:05.46]気分次第です僕は
[00:05.46]随心而定的我
[00:07.95]敵を選んで戦う少年
[00:07.95]是个择敌而战的少年
[00:11.42]叶えたい未来も無くて
[00:11.42]没有想要实现的未来
[00:14.95]夢に描かれるのを待ってた
[00:14.95]只是等待着梦想自己降临
[00:18.92]そのくせ未来が怖くて
[00:18.92]故而我恐惧未来 
[00:21.86]明日を嫌って過去に願って
[00:21.86]讨厌明天 渴望回到过去
[00:25.65]もう如何しようも無くなって
[00:25.65]但也已经束手无策
[00:28.47]叫ぶんだ
[00:28.47]只能无奈喊叫
[00:29.48]明日よ明日よ
[00:29.48]明天啊 明天啊
[00:31.11]もう来ないでよって
[00:31.11]求你不要来啊
[00:33.23]そんな僕を置いて
[00:33.23]明月西沉 旭日东升
[00:37.14]月は沈み陽は昇る
[00:37.14]将那样的我置之不理
[00:40.16]けどその夜は違ったんだ
[00:40.26]然而那个夜晚已经变了
[00:43.74]君は僕の手を
[00:43.74]你抓紧我的手
[00:48.95]
[00:48.95]
... (省略中间部分) ...
[03:20.17]今日の日をいつか思い出せ
[03:20.17]在某一天 回想起今天吧
[03:22.43]未来の僕ら
[03:22.43]未来的我们
```

**`parseLyrics` 执行过程模拟:**

1.  **初始化:**
    * `output: LyricsData` 对象被创建。
    * `output.isSynced = isLyricsSynced(lrcString)`: 函数检测到 `[mm:ss.xx]` 格式的时间戳，所以 `output.isSynced` 设置为 `true`。
    * `output.unparsedLyrics`: 存储完整的 LRC 文件内容字符串。
    * `output.isTranslated`, `output.isRomanized`, `output.parsedLyrics`, `output.originalLanguage`, `output.translatedLanguages`, `output.copyright` 等字段被初始化（例如 `false`, `[]`, `undefined` 等）。

2.  **提取元数据标签:**
    * `getOffsetFromLyricsString`: 找到多个 `[offset:0]`，最后一个生效。函数返回 `0 / 1000 = 0`。所以 `output.offset = 0`。
    * `getCopyrightInfoFromLyricsString`: 在 LRC 文件中未找到 `[copyright:]` 标签。`output.copyright` 保持 `undefined`。
    * `getLanguageFromLyricsString`: 未找到全局的 `[lang:]` 标签。`output.originalLanguage` 保持 `undefined`。
    * 其他元数据如 `ti`, `ar`, `al` 会被 `get...FromLyricsString` 函数识别，但这些信息不直接存储在 `LyricsData` 对象中。

3.  **分割与过滤行:**
    * LRC 字符串按 `\n` 分割成行数组。
    * 过滤掉：
        * 空行。
        * 标准元数据标签行：`[offset:0]`, `[00:00.00][ti:...]`, `[00:00.00][ar:...]`, `[00:00.00][al:...]`, `[00:00.00][by:]`, `[00:00.00][kana:...]` (因为 `[kana:]` 也符合 `^\[\w+:.{1,}\]$` 模式)。
    * 保留下：
        * 定时歌词行，如 `[00:05.46]気分次第です僕は`, `[00:05.46]随心而定的我`, `[00:48.95]` 等。
        * 非标准元数据行（没有时间戳且不符合 `^\[\w+:.{1,}\]$` 模式），如 `アスノヨゾラ哨戒班。明日的夜空哨戒班 - Akie秋绘/夏璃夜`, `//`, `词：Orangestar`, `曲：Orangestar`, `编曲：Orangestar/鈴木秋則`。

4.  **分组原文与译文 (`groupOriginalAndTranslatedLyricLines`):**
    * 这个函数会进一步处理上一步保留下来的行。它使用 `partiallyParseLrcLyricLine` 尝试从每行提取 `timestamp`, `lang`, `lyric`。
    * 那些没有时间戳的非标准元数据行（如 `词：Orangestar`, `//` 等）无法匹配 `LYRICS_LINE_REGEX`，因此会被**过滤掉**。
    * 只剩下带时间戳的行会被处理。
    * 因为 `output.isSynced` 为 `true`，行会根据**时间戳（换算成秒）**进行分组。
    * **示例分组:**
        * **时间 5.46 秒:**
            * `original`: `{ input: '[00:05.46]気分次第です僕は', timestamp: '[00:05.46]', lang: undefined, lyric: '気分次第です僕は' }`
            * `translated`: `[{ input: '[00:05.46]随心而定的我', timestamp: '[00:05.46]', lang: undefined, lyric: '随心而定的我' }]`
        * **时间 7.95 秒:**
            * `original`: `{ input: '[00:07.95]敵を選んで戦う少年', ... }`
            * `translated`: `[{ input: '[00:07.95]是个择敌而战的少年', ... }]`
        * **时间 48.95 秒:**
            * `original`: `{ input: '[00:48.95]', timestamp: '[00:48.95]', lang: undefined, lyric: '' }` (歌词文本为空)
            * `translated`: `[]` (第二行 `[00:48.95]` 也会被解析，但因为歌词为空，可能在后续处理中被忽略或合并，这里简化假设它只有一个空行)
        * ... 其他时间点类似分组 ...

5.  **推断原始语言:**
    * 提取所有 `original` 分组中的 `lyric` 文本（'気分次第です僕は', '敵を選んで戦う少年', '叶えたい未来も無くて', ...）。
    * 将这些文本连接起来，计算日文、中文、韩文的字符占比。
    * 在这个例子中，日文字符占比会很高，因此 `output.originalLanguage` 被设置为 `'ja'`。

6.  **遍历分组后的行 & 构建 `LyricLine[]`:**
    * **处理 5.46 秒的分组:**
        * `start = 5.46` (从 `[00:05.46]` 计算)。
        * `end = 7.95` (下一个 `original` 行 `[00:07.95]` 的开始时间)。
        * `originalText = parseLyricsText('[00:05.46]気分次第です僕は', 7.95)` 返回字符串 `'気分次第です僕は'`。
        * `isEnhancedSynced = false` (因为文本不包含 `<>` 标记)。
        * `translatedTexts = parseTranslatedLyricsText(['[00:05.46]随心而定的我'])`:
            * 内部解析 `'[00:05.46]随心而定的我'`。
            * `getLanguageFromLyricsString` 找不到 `[lang:]` 标签，默认语言为 `'en'`。
            * `parseLyricsText` 返回文本 `'随心而定的我'`。
            * 返回 `[{ lang: 'en', text: '随心而定的我' }]`。
        * 因为 `translatedTexts` 不为空，设置 `output.isTranslated = true`。将 `'en'` 加入 `output.translatedLanguages`。
        * **创建 `LyricLine` 对象 1:** `{ originalText: '気分次第です僕は', translatedTexts: [{ lang: 'en', text: '随心而定的我' }], start: 5.46, end: 7.95, isEnhancedSynced: false, convertedLyrics: '' }`。
    * **处理 7.95 秒的分组:**
        * `start = 7.95`。
        * `end = 11.42` (来自 `[00:11.42]`)。
        * `originalText = '敵を選んで戦う少年'`。
        * `isEnhancedSynced = false`。
        * `translatedTexts = [{ lang: 'en', text: '是个择敌而战的少年' }]`。
        * **创建 `LyricLine` 对象 2:** `{ originalText: '敵を選んで戦う少年', translatedTexts: [{ lang: 'en', text: '是个择敌而战的少年' }], start: 7.95, end: 11.42, isEnhancedSynced: false, convertedLyrics: '' }`。
    * **处理 48.95 秒的分组:**
        * `start = 48.95`。
        * `end = 50.39` (来自下一个有效时间戳 `[00:50.39]`)。
        * `originalText = parseLyricsText('[00:48.95]', 50.39)` 因为文本为空，返回 `INSTRUMENTAL_LYRIC_IDENTIFIER` ('♪')。
        * `isEnhancedSynced = false`。
        * `translatedTexts = []`。
        * **创建 `LyricLine` 对象 (对应空行):** `{ originalText: '♪', translatedTexts: [], start: 48.95, end: 50.39, isEnhancedSynced: false, convertedLyrics: '' }`。
    * ... 对所有分组重复此过程 ...

7.  **存储解析结果:**
    * 将所有创建的 `LyricLine` 对象组成的数组赋值给 `output.parsedLyrics`。

8.  **返回 `output`:**
    * 返回最终的 `LyricsData` 对象。

**最终生成的 `LyricsData` 对象结构 (示意):**

```typescript
{
  isSynced: true,
  isTranslated: true,
  isRomanized: false,
  isReset: false,
  parsedLyrics: [
    { originalText: '気分次第です僕は', translatedTexts: [{ lang: 'en', text: '随心而定的我' }], start: 5.46, end: 7.95, isEnhancedSynced: false, convertedLyrics: '' },
    { originalText: '敵を選んで戦う少年', translatedTexts: [{ lang: 'en', text: '是个择敌而战的少年' }], start: 7.95, end: 11.42, isEnhancedSynced: false, convertedLyrics: '' },
    { originalText: '叶えたい未来も無くて', translatedTexts: [{ lang: 'en', text: '没有想要实现的未来' }], start: 11.42, end: 14.95, isEnhancedSynced: false, convertedLyrics: '' },
    { originalText: '夢に描かれるのを待ってた', translatedTexts: [{ lang: 'en', text: '只是等待着梦想自己降临' }], start: 14.95, end: 18.92, isEnhancedSynced: false, convertedLyrics: '' },
    // ... 其他歌词行 ...
    { originalText: '♪', translatedTexts: [], start: 48.95, end: 50.39, isEnhancedSynced: false, convertedLyrics: '' }, // 空行
    // ... 更多歌词行 ...
    { originalText: '今日の日をいつか思い出せ', translatedTexts: [{ lang: 'en', text: '在某一天 回想起今天吧' }], start: 3*60 + 20.17, end: 3*60 + 22.43, isEnhancedSynced: false, convertedLyrics: '' },
    { originalText: '未来の僕ら', translatedTexts: [{ lang: 'en', text: '未来的我们' }], start: 3*60 + 22.43, end: Infinity, isEnhancedSynced: false, convertedLyrics: '' }
  ],
  unparsedLyrics: "[offset:0]...", // 完整的原始LRC字符串
  offset: 0,
  originalLanguage: 'ja',
  translatedLanguages: ['en'], // 注意：这里假设所有中文都被识别为 'en' (基于代码默认行为)
  copyright: undefined
}
```

这个过程展示了 `parseLyrics` 如何处理包含时间戳、元数据以及混合语言（原文+译文）的 LRC 文件，并将其结构化为 `LyricsData`，特别是将时间和文本分离到 `LyricLine` 对象中，并处理了翻译对。


# reference
