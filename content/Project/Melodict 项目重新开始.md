---
date: 2025-10-29
tags:
  - project
output: false
---

# 前言

之前的这个[[唱歌背单词AI初次开发]]项目就是Melodict的前身文档，但是上篇文档写得太杂太乱，遂新开一个文档

# 正文

我先用svg的图片来代替一下：
https://www.svgrepo.com/svg/476079/music-note
但感觉找不到合适的，先用着原来的，然后再找人吧


---


原项目有着清晰的版本号管理以及变更日志的书写，我得好好阅读他是如何管理这个项目的

[[版本号管理]]

---

构建完毕过后我自己的电脑安装这个应用，确直接运行不起来，必须抛弃沙盒环境才行，

```sh
./Melodict.exe --disable-gpu-sandbox --no-sandbox
```

但运行的时候总是说缺少某些依赖，我估计是构建的时候没打包进去，我需要仔细阅读一下Electron的文档，然后再去解决这件事

---

v4.0.0-alpha 版本发布过后，我就该宣传宣传了，这时候我需要切换角色，从一个程序员，变为一个彻彻底底的销售人员，倾尽全力去宣传、销售我的产品。


---

日语五十音图学习者/需要熟练者的角度：  
就是利用这个软件，在播放日语歌的时候，他会自动语义化分词，并在歌词上面标注平假名，这样在我经常循环歌曲的时候，顺便也能唱出每个词上面的平假名，这下五十音图就能这样熟练起来了

开源软件下载地址：https://github.com/Akiyama-sama/Melodict/releases/tag/v4.0.0-alpha

因为我知道有很多动漫爱好者都想要唱出他们喜欢动漫的op/ed，这样我可以在各大贴吧的特定吧中，去宣传专属这个动漫的op/ed在Melodict上的使用截图。

---

测试下来似乎在mac上有问题，后面安装一下mac的虚拟机，然后在虚拟机中测试，地址：
https://www.kindyear.cn/archives/949/

---

[[Melodict 内存泄露问题回顾]]



## 随心记录

[[Melodict - 异步任务请求状态机]]

立党说过，Agent相比于人类，最适合干的是那种验证复杂度为 1，但实现复杂度为 1000 的任务。因一旦验证标准不明确，整个 Agent loop 循环就会跑偏，导致最终结果的偏差，像是那种有多个集成测试用例的，以及单元测试用例的，红绿灯测试这些。

因此我得自己设计一套验证结果的这个一个标准。首先是结果质量，也就是前端拿到的这个JSON 内容的质量。注意这里并没有说有validate 的东西，validate 的这个工作交给函数，内容质量的判定交给 LLM

内容质量总分 10 分，打分如下：

|维度|分值|看什么|
|---|---|---|
|1. 行级语义准确性|2.0|每行翻译是否符合歌词上下文，不生硬直译，不误解主谓、语气、隐喻、前后承接|
|2. 分词与 token 覆盖|1.5|是否覆盖核心词、助词、短语、外来语；是否漏掉关键教学点；token 切分是否合理|
|3. 语法/词性解释质量|1.5|日语助词、动词形态、接续、固定表达、缩略/外来语解释是否准确且适合学习者|
|4. 读音与语言识别|1.0|日语 kana/romaji、英文 IPA、mixed language 判断是否正确；不要给标点乱造读音|
|5. 教学可用性|1.5|gloss 是否短而清楚；解释是否能帮用户学会这句；不是只给词典义，而是贴合歌词|
|6. 上下文一致性|1.0|chunk 内多行语义是否连贯；重复副歌解释是否稳定；同一个词/表达前后不矛盾|
|7. 幻觉与保守性|1.0|不编不存在的典故、语法、文化解释；不把不确定内容说死；不输出明显过度解释|
|8. 前端呈现友好度|0.5|文案长度适中、字段内容干净、没有模型废话、没有 Markdown/说明文字污染 JSON|

合计 10 分。

我会把通过线设计成：

- **>= 8.0**：通过，可进入前端展示。
- **7.0 - 7.9**：可接受但建议重试一次，取更高分版本。
- **< 7.0**：失败，需要重试生成。
- **任一严重错误直接不通过**：比如整行翻译反了、日语助词大面积错、输出大量臆造内容、明显不符合原歌词。



TS 版本新的结构

```ts
export const LanguageCodeValues = {
  JA: 'ja',
  EN: 'en',
  ZH: 'zh',
  KO: 'ko',
  MIXED: 'mixed',
  UNKNOWN: 'unknown',
} as const;

export type LanguageCode =
  (typeof LanguageCodeValues)[keyof typeof LanguageCodeValues];

export const TokenTypeValues = {
  WORD: 'word',
  PHRASE: 'phrase',
  PARTICLE: 'particle',
  PUNCTUATION: 'punctuation',
  SYMBOL: 'symbol',
  UNKNOWN: 'unknown',
} as const;

export type TokenType =
  (typeof TokenTypeValues)[keyof typeof TokenTypeValues];

export const AnalysisStateValues = {
  COMPLETED: 'completed',
  PARTIAL: 'partial',
  FAILED: 'failed',
} as const;

export type AnalysisState =
  (typeof AnalysisStateValues)[keyof typeof AnalysisStateValues];

export const DifficultyLevelValues = {
  BEGINNER: 'beginner',
  INTERMEDIATE: 'intermediate',
  ADVANCED: 'advanced',
} as const;

export type DifficultyLevel =
  (typeof DifficultyLevelValues)[keyof typeof DifficultyLevelValues];

export const SourceTypeValues = {
  MANUAL: 'manual',
  LRC: 'lrc',
  REMOTE: 'remote',
} as const;

export type SourceType =
  (typeof SourceTypeValues)[keyof typeof SourceTypeValues];

export interface SongAnalysisSummary {
  schemaVersion: '1.0';

  songId?: string;
  title?: string;
  artists?: string[];
  album?: string;

  targetLanguage: LanguageCode;
  sourceLyricsText: string;

  lines: LyricLineAnalysis[];
  metadata?: SongAnalysisMetadata;
}


export interface SongAnalysisMetadata {
  generator: 'llm';
  model?: string;
  generatedAt?: string;
  sourceType?: SourceType;
}

export interface LyricLineAnalysis {
  id: string;

  index: number;
  startTimeMs?: number;
  endTimeMs?: number;

  source: LyricLineSource;

  language: LyricLineLanguageInfo;

  analysis: {
    tokens: Token[];
  };

  translation: {
    lineTranslation: string;
    alternatives?: string[];
  };

  status: {
    state: AnalysisState;
    warnings?: string[];
    errorMessage?: string;
  };

  extensions?: LineExtensions;
}

export interface LyricLineSource {
  text: string;
  normalizedText?: string;
  textHash?: string;
}

export interface LyricLineLanguageInfo {
  code: LanguageCode;
  confidence?: number;
}

export interface Token {
  id: string;

  position: TokenPosition;

  surface: TokenSurface;

  language: {
    code: LanguageCode;
  };

  type: TokenType;

  reading?: TokenReading;

  grammar: TokenGrammar;

  meaning: TokenMeaning;

  translation?: TokenTranslation;

  extensions?: TokenExtensions;
}

export interface TokenPosition {
  index: number;
  startChar: number;
  endChar: number;
}

export interface TokenSurface {
  text: string;
  normalizedText?: string;
}

export interface TokenReading {
  kana?: string;
  romaji?: string;
  ipa?: string;
}

export interface TokenGrammar {
  partOfSpeech: string;
  subcategory?: string;
}

export interface TokenMeaning {
  gloss: string;
  notes?: string[];
}

export interface TokenTranslation {
  literal?: string;
}

export interface LineExtensions {
  ja?: JapaneseLineExtension;
  en?: EnglishLineExtension;
  [key: string]: unknown;
}

export interface TokenExtensions {
  ja?: JapaneseTokenExtension;
  en?: EnglishTokenExtension;
  [key: string]: unknown;
}

export interface JapaneseLineExtension {
  kanaText?: string;
  romajiText?: string;
}

export interface JapaneseTokenExtension {
  dictionaryForm?: string;
}

export interface EnglishLineExtension {}

export interface EnglishTokenExtension {}
```

2026-10-21

主题色

|Swatch|RGB|HEX|
|---|---|---|
|LightVibrant(主底色来源)|`rgb(217, 236, 227)`|`#D9ECE3`|
|Vibrant(logo 身体色)|`rgb(82, 173, 129)`|`#52AD81`|
|DarkVibrant(高亮/进度条)|`rgb(41, 91, 67)`|`#295B43`|
|DarkMuted|`rgb(49, 103, 78)`|`#31674E`|
|LightMuted|`rgb(196, 195, 188)`|`#C4C3BC`|
|Muted|`rgb(183, 177, 170)`|`#B7B1AA`|


2026-10-21

改名为“知音”，英文名：Knote