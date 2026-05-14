---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - React
---
[项目地址](https://github.com/Sandakan/Nora)
## 前言
此项目是我想开发[[唱歌背单词AI初次开发]]的时候找到的项目，我想学习一下这个开源项目，并在此基础之上进行二次开发。

## 点击歌词按钮数据状态流

歌词按钮组件如下：
```ts
<Button
          className={`lyrics-btn !m-0 !rounded-none !border-0 bg-transparent !p-0 outline-1 outline-offset-1 after:absolute after:h-1 after:w-1 after:translate-y-4 after:rounded-full after:bg-font-color-highlight after:opacity-0 after:transition-opacity hover:bg-transparent focus-visible:!outline dark:bg-transparent dark:after:bg-dark-font-color-highlight dark:hover:bg-transparent ${
            currentlyActivePage.pageTitle === 'Lyrics' && 'active after:opacity-100'
          }`}
          tooltipLabel={t('player.lyrics')}
          iconName="notes"
          iconClassName={`material-icons-round !text-2xl opacity-60 transition-opacity hover:opacity-80 ${
            currentlyActivePage.pageTitle === 'Lyrics' &&
            '!text-font-color-highlight dark:!text-dark-font-color-highlight !opacity-100'
          }`}
          clickHandler={() =>
            currentlyActivePage.pageTitle === 'Lyrics'
              ? changeCurrentActivePage('Home')  //重点方法
              : changeCurrentActivePage('Lyrics')
          }
        />
```

changeCurrentActivePage是由Context传过来的
`changeCurrentActivePage: (pageTitle: PageTitles, data?: PageData) => void;`
但也只是AppUpdateContextType中的一个方法类型，那么问题来了，这个方法的实例在哪里，具体是如何触发的

在App.tsx中的最后由
<AppUpdateContext.Provider value={appUpdateContextValues}>所包裹的应用中
appUpdateContextValues包含了changeCurrentActivePage函数的实例

我把这个函数的实例贴上来
```ts
const changeCurrentActivePage = useCallback(
    (pageClass: PageTitles, data?: PageData) => {
          // 1. 获取当前导航历史状态
      const navigationHistory = { ...store.state.navigationHistory };
      const { pageTitle, onPageChange } =
        navigationHistory.history[navigationHistory.pageHistoryIndex];

      const currentPageData = navigationHistory.history[navigationHistory.pageHistoryIndex].data;
       
      // 2. 检查是否需要切换页面
      if (
        pageTitle !== pageClass ||
        (currentPageData && data && isDataChanged(currentPageData, data))
      ) {
         // 3. 调用页面切换回调(如果存在)
        if (onPageChange) onPageChange(pageClass, data);
        // 4. 创建新的页面数据对象
        const pageData = {
          pageTitle: pageClass,
          data
        };
        // 5. 截断历史记录并添加新页面
        navigationHistory.history = navigationHistory.history.slice(
          0,
          navigationHistory.pageHistoryIndex + 1
        );
        navigationHistory.history.push(pageData);
        navigationHistory.pageHistoryIndex += 1;
        // 6. 清除多选状态
        toggleMultipleSelections(false);
        log(`User navigated to '${pageClass}'`);
         // 7. 关键步骤：通过dispatch更新状态
        dispatch({
          type: 'UPDATE_NAVIGATION_HISTORY',
          data: navigationHistory
        });
      } else
        addNewNotifications([
          {
            content: t('notifications.alreadyInPage'),
            iconName: 'info',
            iconClassName: 'material-icons-round-outlined',
            id: 'alreadyInCurrentPage',
            duration: 2500
          }
        ]);
    },
    [addNewNotifications, t, toggleMultipleSelections]
  );
```
 // 7. 关键步骤：通过dispatch更新状态
        dispatch({
          type: 'UPDATE_NAVIGATION_HISTORY',
          data: navigationHistory
        });
在找找用户更新导航历史后的逻辑
在store.ts当中
```ts
export const dispatch = (options: AppReducerStateActions) => {
  store.setState((state) => {
    return appReducer(state, options);
  });
};
```
appReducer返回更新后的store实例，那么就在这里找相关逻辑
```ts
case 'UPDATE_NAVIGATION_HISTORY': {
      const navigationHistory = { ...action.data };//这里的data为dispatch穿过来的  data: navigationHistory导航历史对象
      return {
        ...state,
        bodyBackgroundImage: undefined,
        navigationHistory,
        currentlyActivePage: navigationHistory.history[navigationHistory.pageHistoryIndex]
      };
    }
```

找到了，他更改了一下store中currentlyActivePage这个变量，但为什么改变navigationHistory和currentlyActivePage中的navigationHistory.history就能改变当前页面的状态，我们还得研究一下

回到函数的类型
`changeCurrentActivePage: (pageTitle: PageTitles, data?: PageData) => void;`
和调用的函数来看
changeCurrentActivePage('Lyrics')，其中Lyrics就是page.titile

看看PageTitles
```ts
  type PageTitles =
    | DefaultPages
    | 'Settings'
    | 'Lyrics' //这里
    | 'SongInfo'
    | 'ArtistInfo'
    | 'AlbumInfo'
    | 'PlaylistInfo'
    | 'GenreInfo'
    | 'MusicFolderInfo'
    | 'CurrentQueue'
    | 'SongTagsEditor'
    | 'LyricsEditor'
    | 'AllSearchResults';
```
可以清晰的看到这些类型已经定义好的页面类型

在实例函数中
```ts
 // 5. 截断历史记录并添加新页面
        navigationHistory.history = navigationHistory.history.slice(
          0,
          navigationHistory.pageHistoryIndex + 1
        );
        navigationHistory.history.push(pageData);
        navigationHistory.pageHistoryIndex += 1;
```
通过添加pageData
```ts
const pageData = {
          pageTitle: pageClass,//传入过来的Lyrics字符串
          data
        };
```
来更改导航的历史记录，我们再深入了解这个navigationHistory类型定义navigationHistory: NavigationHistoryData;
```ts
  interface NavigationHistoryData {
    pageHistoryIndex: number;
    history: NavigationHistory[];
  }

	interface NavigationHistory {
	    pageTitle: PageTitles;
	    data?: PageData;
	    onPageChange?: (changedPageTitle: PageTitles, changedPageData?: PageData)          => void;
	}
```
具体分析可以看看下面：
[[Nora页面导航]]

## 添加后退监听事件

由于本项目没有鼠标后侧键的监听事件，因此我为他添加了一个鼠标侧键后退的监听事件

```ts
  const handleMouseBackButton = useCallback((e: MouseEvent) => {
    if (e.button === 3) {
      e.preventDefault();
      updatePageHistoryIndex('decrement');
    }
  }, [updatePageHistoryIndex]);

  useEffect(() => {
    window.addEventListener('mouseup', handleMouseBackButton);
    return () => {
      window.removeEventListener('mouseup', handleMouseBackButton);
    };
  }, [handleMouseBackButton]);
```

## 歌词部分

[[在Nora中处理歌词文件中的数据结构]]
以一个lrc文件为例，展示了parseLrycis这个函数是如何运作的
[[lrc文件例子转化为LrycisData的解析过程]]
无论他是从哪里得到的lrc文件，只要我们搞清楚LyricsData的结构就行了
```ts
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

## 利用Jest库来进行测试

没用过Jest
[[Jest]]

## 其他
* type.ts这个文件当中有个注释：https://quicktype.io/，说是用这个网站，把用例Json格式的数据转为type，[quicktype](https://quicktype.io/)
* 在歌词当中，我发现他用的一个歌词开源方案[Lcrlib](https://lrclib.net/)

这个项目用到了[[useMemo]]和[[useCallback]]这两个Hook，我没用过，记录一下
还用到了[[Tanstack Store]]，没接触过，学习一下

发现了一个问题，就是点击一个歌曲的时候会有缓存时间，导致会过好几秒才能加载出音频，我还以为没点到，我就多点了几次，就卡住了，会同时播放两种不同的歌曲，算是一个bug吧，后面熟悉项目整体后再修修这个问题

## 碰到的Issue
* 添加歌单，或者将一首歌加入歌单后，点叉叉退出退出不了，且逻辑应该是添加完毕过后直接退出（这个Issue是我自己的那个修改的版本）
* 有时候就算在同一文件下，相同文件名的音频文件，歌词文件，歌曲封面图片都识别不出来是一同一首歌的，不知道是不是音乐标签没识别完全[music-tag-web](https://github.com/xhongc/music-tag-web)这个项目粗略看了一下有获取歌词API还有处理音乐标签的模块，后面再看看，不过大部分的标签和封面都能识别的


# reference
