---
tags:
  - #project
  - 前端实习挑战
  - 前端
  - React
---
灵感来源：[[通过唱歌背单词]]
   
   为了让AI能理解我的需求，我得先写一个需求文档和编码文档，需求文档编写产品的需求，功能，编码文档确定技术栈，编码步骤
   [[唱歌背单词需求文档]]
   
   我想在开源方案中直接修改，我先找找有哪些优秀的开源方案在其之上进行二次开发
   [[唱歌背单词开源方案调查]]
   
   我决定采用[Nora](https://github.com/Sandakan/Nora)，在此基础之上进行二次开发，此开源项目虽然Star不是太多，但界面简洁，美观大气，我先读读Nora源码，学习一下这个开源项目
   [[Nora]]
   
   我在浏览的过程中，不仅Nora，还有一个网易云套壳的播放器深得我心，[SPlayer](https://github.com/imsyy/SPlayer?tab=readme-ov-file)，里面所用到的[Apple样式的歌词组件库](https://github.com/Steve-xmh/applemusic-like-lyrics)，还有随着封面颜色渲染整个歌词背景页面的颜色背后的[开源项目](https://github.com/material-foundation/material-color-utilities)，给了我很多启发与想象的空间
   
   ==在体验过程中，我认为需要添加一个左右键热键来控制歌曲前进/后退n秒==
   
   当我在Nora之上进行开发时，我就得需要改变一些提示词，让gemini能够理解我，并再其之上提出一些建议
   
   - **产品背景**：在初一英语老师布置唱英语歌的暑假作业的时候，我常常在想，如果有个软件，可以在歌词浏览的时候，点击某个单词，就能跳出这个单词的读法，释义，而且并不是查词典后僵硬的释义或者读法，而是对歌词的上下文针对性给出此单词的释义与读法，可以让我学会唱英语歌的同时，能背这些单词，例如说WestLife中有一首歌的单词：cherish珍惜，这个单词虽然没在书上要求背，但通过这首歌，我记得很牢固。直到现在，在我听日语歌的时候，也在想如果有类似的软件就好了，我经常听ACG，JPop的歌，如果能让我学会唱这些歌的同时，能让我记住这些单词不就一举两得了吗，这就是这个产品的由来。
       
   - **产品目标**：在Nora的基础之上开发一个歌词滚动条结合语言学习的应用，此产品可以解决用户想在学唱外语歌的同时，可以背这些外语单词的痛点
       
   - **目标用户**：外语初学者，初一，初二英语初学者，ACG日语歌爱好者，韩语歌爱好者
       
   - **核心价值**：此产品既可以让英/日/韩语歌爱好者可以学会唱出他们喜欢的外语歌，还可以在学会唱歌的同时，无痛地背出歌词里面当中的单词，让此产品寓教于乐
   
   提示词：请理解本项目的宗旨，我想让在Nora的基础之上实现这个产品，我的改造想法是在这个LyricData变为另一个数据结构r，主要是将原字段中的parsedLyrics.LyricLine.originalText利用AI/comprise.js进行数据处理，如果歌词是日语，数据处理包括含义，在句子中的成分，词性，罗马音，平假名，来分析每个按单词/短语切分好的切片，分析好后最后语法分析整个句子。将切分好的originalText每个切片定义为一个个button，点击每个单词/短语的button可以跳出此单词/短语的所有被AI处理好的信息。我的这个改造想法怎么样，在此工程中有没有更好的实现方法来实现本产品的愿景，你作为一个熟练高级开发工程师，请给我改造建议。
   
   
   在进行LyricLine句子切分的时候遇到了难处：最开始想着用LLM来进行切分句子，但还是有挑战：
   1. 大模型有幻觉，不保证每次切分都能切成一个样子，这样就不能保证用户查词典的时候的准确性
   2. 成本大，耗时长，LLM处理文本需要一定时间，如果只是简单的切分句子并查单词英语很容易，日语也有现成的[库](https://github.com/miseya/kuroshiro/blob/master/README.zh-cn.md)，不过韩语没有，可能得采取混合的方式来进行切分句子，甚至得将韩语拖到后面再做
   
   君のために It's forever
   npm test japaneseTokenizer.test.ts
   
   英语句子切分上我用的是这个库[compromise](https://github.com/spencermountain/compromise?tab=readme-ov-file)
   日语句子切分是@sglkc/kuromoji这个库
   
   至于其他的切分方案我在网络中看到有一个机器学习切分的方案[tokenizers](https://github.com/huggingface/tokenizers/tree/main)
   
   至于词典查询我在网络上没找到好用的API，一般都是一段文本翻译的API，我还是用本地查询的吧，为了查询快一点，得用数据库查询，且不涉及到修改与删除等复杂的任务，用sqlite就可以了，在Node.js环境中Gemini 推荐用[better-sqlite3](https://github.com/WiseLibs/better-sqlite3)这个库
   英语词典来源：[dict](https://github.com/kajweb/dict)
   
   英语词典表结构
   ```
   CREATE TABLE IF NOT EXISTS dictionary (
             word TEXT PRIMARY KEY NOT NULL,      -- 单词 (headWord)
             wordRank INTEGER,                  -- 单词序号
             usphone TEXT,                      -- 美式音标
             ukphone TEXT,                      -- 英式音标
             ukspeech TEXT,                     -- 英式发音链接相关
             usspeech TEXT,                     -- 美式发音链接相关
             translations TEXT,                 -- 核心释义列表 (JSON 字符串化 trans 数组)
             sentences TEXT,                    -- 例句列表 (JSON 字符串化 sentences 数组)
             phrases TEXT,                      -- 短语列表 (JSON 字符串化 phrases 数组)
             synonyms TEXT,                     -- 同近义词 (JSON 字符串化 syno 对象)
             antonyms TEXT,                     -- 反义词 (JSON 字符串化 antos 对象)
             relatedWords TEXT,                 -- 同根词 (JSON 字符串化 relWord 对象)
             collinsStar INTEGER,               -- 柯林斯星级 (从 star 字段获取)
             bookId TEXT                        -- 来源书籍 ID
             -- 可以根据需要添加 wordId 等其他字段
           );
   ```
   
   示例Json字符串
   ```json
   {
      "wordRank": 3, // 单词在该词典或列表中的排序、等级或序号
      "headWord": "abandon", // 核心单词、词头
      "content": { // 包裹单词主要详细内容的对象
        // 注意：这里的 "wordHead" 和 "wordId" 存在于原始 JSON 的 "content.word" 层面下，
        // 而更详细的音标、释义等在 "content.word.content" 下。
        // 在之前的数据库脚本中，我们可能简化了层级，直接从 "entry.content.word.content" 取数据，
        // 并将 "entry.headWord" 作为了数据库中的 "word"。
        // 这里我们按照你提供的 JSON 结构进行注解。
        "wordHead": "abandon", // 单词的拼写（与外层的 headWord 通常一致）
        "wordId": "Level8_2_3", // 该单词在本词典数据中的唯一标识符
        "content": { // 包含单词所有详细语言学信息的对象
          "sentence": { // 关于例句的信息
            "sentences": [ // 例句数组，可能包含多个例句
              {
                "sContent": "He approached life with reckless abandon–I don't think he himself knew what he was going to do next.", // 英文例句内容
                "sCn": "他以不计后果的放纵态度对待生活–我想他自己都不知道他接下来要做什么。" // 例句的中文翻译
              }
            ],
            "desc": "例句" //对此部分的描述，这里是“例句”
          },
          "usphone": "ə'bændən", // 美式音标
          "syno": { // 关于同义词/近义词的信息
            "synos": [ // 同义词/近义词列表，可能按词性分组
              {
                "pos": "n", // 该组同义词的词性 (例如：名词)
                "tran": "狂热；放任", // 该组同义词对应的中文含义或分类
                "hwds": [ // 具体的同义词单词列表
                  {"w": "loose"},
                  {"w": "mania"}
                ]
              },
              {
                "pos": "vt", // 该组同义词的词性 (例如：及物动词)
                "tran": "遗弃；放弃", // 该组同义词对应的中文含义或分类
                "hwds": [
                  {"w": "desert"},
                  {"w": "yield"},
                  {"w": "quit"}
                ]
              }
            ],
            "desc": "同近" // 对此部分的描述，这里是“同近”
          },
          "antos": { // 关于反义词的信息
            "anto": [ // 反义词列表
              {"hwd": "reclaim"} // 具体的反义词
            ],
            "desc": "反义" // 对此部分的描述，这里是“反义”
          },
          "ukphone": "ə'bænd(ə)n", // 英式音标
          "ukspeech": "abandon&type=1", // 英式发音的音频文件名或API参数
          "star": 0, // 单词的星级或重要程度 (例如柯林斯星级，0 可能表示非星级或未评级)
          "phrase": { // 关于常用短语的信息
            "phrases": [ // 短语列表
              {
                "pContent": "with abandon", // 英文短语
                "pCn": "恣意地，放纵地" // 短语的中文释义
              },
              {
                "pContent": "abandon ship",
                "pCn": "弃船"
              }
            ],
            "desc": "短语" // 对此部分的描述，这里是“短语”
          },
          "speech": "abandon", // 单词的朗读形式或基本拼写（可能与 headWord 一致）
          "relWord": { // 关于同根词或派生词的信息
            "rels": [ // 同根词/派生词列表，可能按词性分组
              {
                "pos": "adj", // 该组词的词性 (例如：形容词)
                "words": [ // 具体的同根词/派生词列表
                  {"hwd": "abandoned", "tran": "被抛弃的；无约束的；恣意放荡的；寡廉鲜耻的"} // 词汇及其基本中文释义
                ]
              },
              {
                "pos": "n",
                "words": [
                  {"hwd": "abandonment", "tran": "抛弃；放纵"}
                ]
              },
              {
                "pos": "v", // 注意这里 pos:v 对应的是 abandoned 这个过去式/过去分词形式
                "words": [
                  {"hwd": "abandoned", "tran": "抛弃（abandon的过去式和过去分词）"}
                ]
              }
            ],
            "desc": "同根" // 对此部分的描述，这里是“同根”
          },
          "usspeech": "abandon&type=2", // 美式发音的音频文件名或API参数
          "trans": [ // 单词的主要释义/翻译列表（核心部分）
            {
              "tranCn": "放任；狂热", // 中文释义
              "descOther": "英释", // 描述字段，表明 tranOther 是英文释义
              "descCn": "中释", // 描述字段，表明 tranCn 是中文释义
              "pos": "n", // 该条释义对应的词性 (名词)
              "tranOther": "if someone does something with abandon, they behave in a careless or uncontrolled way, without thinking or caring about what they are doing" // 英文释义/例证
            },
            {
              "tranCn": "遗弃；放弃",
              "descOther": "英释",
              "descCn": "中释",
              "pos": "v", // 该条释义对应的词性 (动词)
              "tranOther": "to leave someone, especially someone you are responsible for"
            }
          ]
        }
      },
      "bookId": "Level8_2" // 词典来源的书籍ID或标识符
    }
   ```
   ```
   ```
   
## 切分方案
   不过有个问题是例如I've been here原样处理为 I am here的话就不能让 I've 这样的缩略词分为一个token了，因此并不能简单的将句子的全部来进行原样解析，而是只是把动词变为原形，系动词之类的不变，这样就既能不影响系动词的分词，又能对动词短语进行精准匹配
   
   因此切分方案为
   1. 先用comprise.nomalize()先将歌词句子标准化，再对句子中的动词进行还原
   2. 根据原样解析的结果，将8000+短语用更高效的算法对句子中存在的短语进行精准匹配并分为一个token
   3. 再用comprise自带的分词功能，处理缩略词等等
   
   不过comprise不知道为什么会在动词后加点，导致有问题  
   ```
    ● normalizeVerbsInSentence › should convert "This was developed by them." to "This was develop by them."   
      
          expect(received).toBe(expected) // Object.is equality
      
          Expected: "This was develop by them."
          Received: "This was develop.by them."
   ```
   ==切分方案重来==
   - 第一遍，使用 `compromise` 初步解析歌词行，得到每个 `term` 对象。
   - 创建一个与原始 `term` 序列平行的“**候选匹配词序列**”。
       - 对于每个原始 `term`：
           - 如果是动词（非助动词、非系动词、非情态动词），候选词是其**词元（lemma/不定式）**。
           - 如果是缩写词，候选词是其**展开后的各个词**（这会让候选匹配词序列的长度可能大于原始 `term` 序列的长度，需要特别处理）。
           - 如果是名词，候选词是其**单数形式**。
           - 其他词保持原样（或者也取其 `normal()` 形式）。
   - 让这个“候选匹配词序列”与你的短语库（短语库中的短语也应该是“标准形态”）进行匹配。
   
   终于弄好了，我用gemini帮我总结一下切分策略：[[英语歌词切分策略]]
   
## 日语模块
   我用的是 kuromoji.js这个模块来进行切分的，在切分的时候碰到了渲染的小问题，当我更新歌词数据的时候，就算最顶层的对象引用更新了，但其中某些对象你要是不更新引用的话，渲染进程还是认为没有改变，这里就能体现不可变数据或者是新建引用的重要性了。
   
   装上这个模块并在前端进行渲染的时候我发现了一个很严重的性能问题：内存泄露，有很多组件渲染了但没有销毁，导致我拍堆快照的时候，CSSTransition和keyframeEffect越来越多
   
   
## 字典匹配
   Gemini说到了[[Aho-Corasick]]算法，先让我学习一下
   
## 其他
   js基础太薄弱了，对数组的操作都不能手到擒来，后面得多练习多背背方法。
   
   碰到tailwind一个坑了，opecity和color这两个本来不相关的两个属性，tailwind非要绑定在一起，子盒子一旦层叠了父盒子的color样式，其opecity竟然不能继承下来！！
   
   
## 产品思考
   
   我在思考如何将分析后的数据在前端页面展示，设计组件的时候，我突然意识到自己并不是自己的用户，自己并没有去学唱日语歌，自己并没有成为自己的用户，因此我得自己学唱日语歌才行，像是b站上面那些教唱日语歌的视频，其实就是同一类产品，解决的都是同一类需求：==不仅仅要求会唱，在会唱的同时能学习单词，语法==。因此我利用他们的视频学习唱日语歌其实就是对自己产品审视的过程
   
   我在这个过程中发现了一个很重要的三点：
   4. 如果只是将分析后的数据嵌入到歌词中，想让用户悬浮在单词上面查询有一个问题：歌曲的节奏太快了，你不能让用户悬浮在一个token上面，然后又移动到下一个token，这样上一个token消失了，因为定位的用户为初学者，可以说是完全不了解语法或者单词的。因此展示只能是只能以一句歌词为单位来展示一句歌词的token[]，对于单个token的信息显示，==只能作为辅助的显示作用==。想要一句歌词为显示单位，可以参考[Don't say lazy](https://b23.tv/oJ9MZet) 这个教学中对信息的布局展示。
   5. 第二个问题，就是一句歌词我没唱熟练，得手动切换到那句歌词的开始部分，这个是一个很反直觉的东西，我可以设置一个快捷键，例如[[Nora]]中快进/后退的快捷键是shift+<>左右键，这样就能直接跳转到上一句的开头，或者上一句的前几秒用户可以自己设置
   6. 根据 凯西「用户思维」这本书的理论，用户喜欢一个产品，不是因为这个产品很好，而是因为产品使用这个产品，让他自己变得更好而感觉更好了，「让用户感觉良好」，聚焦在用户身上，是产品的重点。在此产品中我的其中一个切入点是：针对那些已经循环播放了无数次某首日语歌的人，他们可能有的会唱，有的不会唱。但他们只需要使用了这个产品，不仅让他们学会唱自己喜爱的歌曲，顺便能够“学习”，顺便能够“背单词”，让他们感觉自己在朝着更好的方向发展。
   
   ## 产品名字
   1.0 简单歌词 EasyLyrics
   备选：
   * 乐词汇
   * 乐词通
   * 旋律词典
   * 乐记单词
   * 跟着音乐背单词
   
   
   ## 产品slogan
   1.0 仅需循环播放您喜爱的歌曲，就可以轻松学习外语
   
   ## 产品logo
   1.0 
   ![file-20250603221657747](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20250603221657747.png)