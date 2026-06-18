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

  summary?: SongAnalysisMetaSummary;
  metadata?: SongAnalysisMetadata;
}

export interface SongAnalysisMetaSummary {
  overallTranslation?: string;
  keywords?: string[];
  difficulty?: DifficultyLevel;
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