---
date: 2025-10-21
tags: 
draft: "true"
---
路径：/etc/nginx/sites-available

```nginx
server {
    listen 2005; 后续改为80
    server_name 47.109.99.107; # 替换成您的域名，如果没有域名，可以用服务器公网IP

    # 根路径代理配置
    location / {
        # **核心代理指令：将请求转发到 GitHub Pages**
        # 注意：如果您的 GitHub Pages 地址是项目页面（如 /repo-name），请在URL末尾添加斜杠 /
        proxy_pass https://akiyama-sama.github.io/Akiyama-blog/; 

        # 关键头部信息设置
        # 设置Host头，通常需要设置为GitHub Pages的原始Host（如 username.github.io）
        # 否则 GitHub Pages 可能会返回 404
        proxy_set_header Host akiyama-sama.github.io; # 替换成您的 username.github.io
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 避免浏览器缓存问题
        #proxy_cache off;
        
        # 确保所有请求都发往 Pages
        proxy_redirect off;
    }

    # 错误日志和访问日志
    error_log  /var/log/nginx/Akiyama-blog-error.log;
    access_log /var/log/nginx/Akiyama-blog-access.log;
}
```

