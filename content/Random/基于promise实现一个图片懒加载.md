---
date: 2026-05-10
tags:
aliases:
---
```js
// 1. 封装加载函数：将图片加载转为 Promise
const loadImage = (img) => {
  return new Promise((resolve, reject) => {
    img.src = img.dataset.src; // 替换真实路径
    img.onload = () => resolve(img);
    img.onerror = reject;
  });
};

// 2. 核心逻辑：监听并触发加载
const lazyLoad = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        
        loadImage(img)
          .then(() => console.log('Loaded:', img.src))
          .catch(err => console.error(err))
          .finally(() => observer.unobserve(img)); // 无论成功失败，停止观察
      }
    });
  });

  // 3. 获取所有带 data-src 的图片并开始观察
  document.querySelectorAll('img[data-src]').forEach(img => {
    observer.observe(img);
  });
};

// 执行
lazyLoad();
```