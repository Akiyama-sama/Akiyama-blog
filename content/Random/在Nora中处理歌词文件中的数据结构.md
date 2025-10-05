---
tags:
  - '#pernamant'
---

## LRC格式和ID3标签中的歌词数据

LRC文件格式和音频文件的ID3标签是存储和显示歌词的两种主要方式。下面详细介绍这两种格式的结构以及它们在Nora音乐播放器中的应用。

### LRC文件格式

LRC(Lyric)是一种简单的文本格式，用于存储歌词与时间的同步信息。它基于纯文本，使用特定的标记来表示时间戳和元数据。

#### 1. 基本结构

LRC文件由两部分组成：
1. **元数据标签**：包含歌曲信息的标签，以方括号包围
2. **时间戳歌词**：包含时间戳和对应歌词文本的行

#### 2. 元数据标签

LRC文件通常包含以下元数据标签：
```
[ti:标题]          - 歌曲标题
[ar:艺术家]        - 艺术家/演唱者
[al:专辑]          - 专辑名称
[length:时长]      - 歌曲时长，格式为"分:秒"
[lang:语言]        - 歌词语言代码(如"zh"、"en")
[offset:偏移量]    - 歌词整体时间偏移，单位为毫秒
[copyright:版权]   - 版权信息
[ve:版本]          - 创建软件版本
[re:创建者]        - 歌词文件创建者
```

#### 3. 时间戳歌词

时间戳歌词的基本格式为：
```
[分钟:秒.毫秒]歌词文本
```

例如：
```
[00:12.34]这是一行歌词
[00:16.50]这是下一行歌词
```

#### 4. 扩展同步歌词

LRC格式还支持单词级别的同步，称为"扩展同步歌词"：
```
[00:12.34]<00:12.50>第<00:12.70>一<00:13.00>个<00:13.20>词
```

每个`<时间戳>`表示单词开始的时间。

#### 5. 多语言支持

LRC还可以支持同一时间点的多语言歌词：
```
[00:12.34]原文歌词
[00:12.34][lang:en]英文翻译
```

### ID3标签中的歌词数据

ID3是音频文件(主要是MP3)的元数据标准，可以嵌入歌词等信息到音频文件中。

#### 1. ID3标签结构

ID3v2标签中，歌词信息主要以两种方式存储：
1. **USLT（非同步歌词/文本）**：存储无时间戳的纯文本歌词
2. **SYLT（同步歌词/文本）**：存储带时间戳的同步歌词

#### 2. USLT帧格式

非同步歌词在Node-ID3库中的结构：
```typescript
interface UnsynchronisedLyrics {
  language: string;      // 通常为"ENG"或其他语言代码
  text: string;          // 纯文本歌词
}
```

#### 3. SYLT帧格式

同步歌词在Node-ID3库中的结构：
```typescript
interface SynchronisedLyrics {
  contentType: number;          // 内容类型（如：1表示歌词）
  timeStampFormat: number;      // 时间戳格式（通常为毫秒）
  language: string;             // 语言代码
  shortText?: string;           // 简短文本/元数据（可存储为JSON）
  synchronisedText: Array<{
    text: string;               // 歌词文本
    timeStamp: number;          // 时间戳（毫秒）
  }>;
}
```

### Nora播放器中的歌词数据处理

Nora播放器对LRC和ID3标签中的歌词进行了统一处理，将它们转换为内部的`LyricsData`类型。

#### 1. 歌词数据获取流程

1. **LRC文件读取**：从以下位置寻找LRC文件
   ```typescript
   // 查找顺序
   const defaultLrcFilePath = `${songPath}.lrc`;
   const defaultLrcFilePathWithoutExtension = `${songPath.replaceAll(path.extname(songPath), '')}.lrc`;
   const customLrcFilePath = userData.customLrcFilesSaveLocation ? 
     path.join(userData.customLrcFilesSaveLocation, `${path.basename(songPath)}.lrc`) : undefined;
   ```

2. **ID3标签读取**：使用Node-ID3库从音频文件中读取歌词标签
   ```typescript
   const tags = await NodeID3.Promise.read(songPath);
   const lyrics = parseLyricsFromID3Format(tags.synchronisedLyrics, tags.unsynchronisedLyrics);
   ```

3. **在线歌词服务**：如果本地没有歌词，可从在线服务获取
   ```typescript
   // 例如从lrclib获取歌词
   const lrclibLyrics = await fetchLyricsFromLrclib({...});
   ```

#### 2. 歌词解析过程

无论是LRC文件还是ID3标签中的歌词，最终都会通过`parseLyrics`函数解析成统一的格式：

```typescript
const parseLyrics = (lrcString: string): LyricsData => {
  const output: LyricsData = {
    isSynced: isLyricsSynced(lrcString),        // 是否为同步歌词
    isTranslated: false,                         // 是否包含翻译
    isRomanized: false,                          // 是否包含罗马音
    isReset: false,
    parsedLyrics: [],                            // 解析后的歌词行
    unparsedLyrics: lrcString,                   // 原始歌词文本
    copyright: getCopyrightInfoFromLyricsString(lrcString),
    originalLanguage: getLanguageFromLyricsString(lrcString),
    translatedLanguages: [],
    offset: getOffsetFromLyricsString(lrcString) // 时间偏移量
  };
  
  // 解析歌词行
  const lines = lrcString
    .split('\n')
    .filter((line) => line.trim() !== '' && isNotALyricsMetadataLine(line));

  const groupedLines = groupOriginalAndTranslatedLyricLines(lines, output.isSynced);
  // ...处理歌词内容...
  
  return output;
};
```

#### 3. 内部数据结构与文件格式的映射

Nora播放器将LRC和ID3格式的歌词映射到内部`LyricsData`数据结构：

| LRC/ID3格式元素 | Nora内部数据字段 | 说明 |
|---------------|-----------------|------|
| `[ti:标题]` | `title` | 歌曲标题 |
| `[ar:艺术家]` | `artist` | 艺术家名称 |
| `[al:专辑]` | `album` | 专辑名称 |
| `[lang:语言]` | `originalLanguage` | 歌词原始语言 |
| `[offset:偏移量]` | `offset` | 时间偏移量(秒) |
| `[copyright:版权]` | `copyright` | 版权信息 |
| 时间戳`[00:12.34]` | `start`/`end` | 开始/结束时间(秒) |
| 歌词文本 | `originalText` | 原始歌词文本 |
| 带语言标记的翻译行 | `translatedTexts` | 翻译歌词数组 |

#### 4. 歌词保存过程

当用户编辑或获取新歌词时，Nora可以将歌词保存回LRC文件或ID3标签：

4. **保存到LRC文件**：
   ```typescript
   // 将内部数据转换回LRC格式
   const convertLyricsToLrcFormat = (songLyrics: SongLyrics) => {
     const lyricsArr: string[] = [];
     
     // 添加元数据标签
     lyricsArr.push(`[re:Nora (https://github.com/Sandakan/Nora)]`);
     lyricsArr.push(`[ve:${version}]`);
     lyricsArr.push(`[ti:${title}]`);
     // ...其他元数据标签...
     
     // 添加歌词行
     lyricsArr.push(...getLrcLyricLinesFromParsedLyrics(parsedLyrics));
     
     return lyricsArr.join('\n');
   };
   ```

5. **保存到ID3标签**：
   ```typescript
   // 将内部数据转换为ID3格式
   const convertParsedLyricsToNodeID3Format = (parsedLyrics?: LyricsData): SynchronisedLyrics => {
     // 转换同步歌词结构
     const synchronisedText = syncedLyrics.map((line) => ({
       text: typeof line.originalText === 'string' ? line.originalText : line.originalText.map(x => x.text).join(' '),
       timeStamp: Math.round(line.start * 1000) // 转换为毫秒
     }));
     
     return [{
       contentType: TagConstants.SynchronisedLyrics.ContentType.LYRICS,
       timeStampFormat: TagConstants.TimeStampFormat.MILLISECONDS,
       language: 'ENG',
       shortText: copyright ? JSON.stringify({ copyright }) : undefined,
       synchronisedText
     }];
   };
   ```

### 总结

Nora音乐播放器通过精心设计的解析和转换机制，实现了LRC文件和ID3标签两种歌词格式的无缝集成。内部统一的`LyricsData`数据结构使得应用能够一致地处理、显示和编辑来自不同来源的歌词，同时支持多语言歌词、时间偏移调整、单词级同步等高级功能。

无论歌词来自哪种格式，Nora都能将其转换为统一的内部表示，经过处理后再渲染到用户界面，提供流畅的歌词显示和交互体验。同时，当用户编辑歌词后，Nora能够将修改后的歌词保存回原始格式，保持数据的完整性和兼容性。

---




# reference
