---
tags:
  - '#pernamant'
---
url:http:/47.93.57.11:10086
原里型地址：https:js.design/fvZ1Gd9?mode=design&p=J_BcY0gELq


1、获取手机验证码
请求request:
path:/admin/VerCode
data:{
phone_num 12345,
∥手机号
op_type 1
∥操作类型1：注册，2：登录
}
返回response:
data:{
errCode =1
∥错误码

3、管理员账号登录
请求request:
path:/admin/AdminLogin
data:{
phone num=123456,/∥手机号
ver code=123456
∥验证码
返▣response:
data:{
errCode =1,
∥错误码
phone num=123456,/∥手机号
token 123456
/token
}


10、查找产品
请求request:
path:/admin/SearchProduct
data:{
phone_num=123456,∥手机号
token=123456,
/token
search text =1
∥查找文本

返回response:
data:{
errCode 1  ∥错误码

请求体：

```json
{
   "productId": 1,
   "productStatus": "ON_SHELF", 
   // 状态枚举值。建议映射关系：
   // "ON_SHELF": "上架", "OFF_SHELF": "下架", "DELETED": "删除", "PENDING_REVIEW": "审核"
 
   "coverUrl": "https://example.com/display_image1.jpg",
   "displayUrls": [
     "https://example.com/display_image1.jpg",
     "https://example.com/display_image2.jpg"
   ],
   "categoryId": "SUB_101", 
 
   "title": "您的产品标题",
   "subTitle": "您的产品副标题", 
   "productDesc": "您的产品详细描述",
   "productHighlights": [ 
     "专业导游讲解，深入了解故宫历史",
     "亲子互动环节，增强家庭感情",
     "专属儿童讲解器，适合孩子理解",
     "故宫文创纪念品赠送",
     "专业摄影师跟拍服务"
   ],
   "tags": [
     "文化古迹",
     "春季赏花"
   ],
   "priceType": "BASE_PRICE", 
   // 价格类型枚举值。建议映射关系：
   // "BASE_PRICE": "基础价", "MEMBER_PRICE": "会员价", "PROMOTION_PRICE": "促销价"
 
   "priceCalendar": [
     {
       "date": "2025-06-12",
       "price": 398, 
       "amount": 10 
     },
     {
       "date": "2025-06-19",
       "price": 298,
       "amount": 10
     },
     {
       "date": "2025-06-20",
       "price": 178,
       "amount": 13
     },
     {
       "date": "2025-06-26",
       "price": 398,
       "amount": 10
     }
   ],
 
   "activityStartTime": "2025-07-01T09:00:00Z", 
   "activityEndTime": "2025-07-10T18:00:00Z",
   "participantLimit": 50, 
   "meetingAddress": "集合地点详细地址",
   "disbandAddress": "解散地点详细地址",
   "ageRange": {
     "min": 18,
     "max": 65
   },
   "zones": [
     "北京"
   ],
   "destinations": [ // 原字段为 dests，全称 destinations 更清晰
     "北京"
   ]
 }
```



# reference
