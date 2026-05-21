# API 接口文档

## 概述

本文档详细描述了新闻系统的API接口，包括用户管理、新闻浏览、收藏和历史记录等功能模块。

## 接口实现流程

1. 模块化路由 → API 接口规范文档
2. 定义模型类 → 数据库表(数据设计文档)
3. 在 CRUD 文件夹里面创建文件，封装操作数据库的方法
4. 在路由处理函数里面调用 CRUD 封装好的方法，响应结果

## 响应格式

所有接口返回JSON格式数据，通用响应结构如下：

```json
{
	"code": 200,
	"message": "success",
	"data": {}
}
```

## 接口详情

### 新闻模块

#### 1. 获取新闻分类列表

- **接口地址**: `GET /api/news/categories`
- **请求参数**:

| 参数名 | 类型    | 必填 | 说明                        |
| ------ | ------- | ---- | --------------------------- |
| skip   | integer | 否   | 跳过的记录数，默认为0       |
| limit  | integer | 否   | 返回的记录数限制，默认为100 |

- **请求示例**:

```
GET /api/news/categories
GET /api/news/categories?skip=0&limit=10
```

- **响应示例**:

```json
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"id": 1,
			"created_at": "2023-01-01T00:00:00",
			"updated_at": "2023-01-01T00:00:00",
			"name": "科技",
			"sort_order": 0
		}
	]
}
```

#### 2. 获取新闻列表

- **接口地址**: `GET /api/news/list`
- **请求参数**:

| 参数名     | 类型    | 必填 | 说明                                      |
| ---------- | ------- | ---- | ----------------------------------------- |
| categoryId | integer | 是   | 分类ID                                    |
| page       | integer | 否   | 页码，默认为1                             |
| pageSize   | integer | 否   | 每页显示的新闻数量，最大值为100，默认为10 |

- **请求示例**:

```
GET /api/news/list?categoryId=1
GET /api/news/list?categoryId=1&page=2&pageSize=20
```

- **响应示例**:

```json
{
	"code": 200,
	"message": "success",
	"data": {
		"list": [
			{
				"id": 1,
				"publish_time": "2023-01-01T00:00:00",
				"created_at": "2023-01-01T00:00:00",
				"updated_at": "2023-01-01T00:00:00",
				"category": null,
				"title": "新闻标题",
				"description": "新闻简介",
				"content": "新闻内容",
				"image": null,
				"author": null,
				"category_id": 1,
				"views": 0
			}
		],
		"total": 100,
		"hasMore": true
	}
}
```

#### 3. 获取新闻详情

- **接口地址**: `GET /api/news/detail`
- **请求参数**:

| 参数名 | 类型    | 必填 | 说明   |
| ------ | ------- | ---- | ------ |
| id     | integer | 是   | 新闻ID |

- **请求示例**:

```
GET /api/news/detail?id=1
```

- **响应示例**:

```json
{
	"code": 200,
	"message": "success",
	"data": {
		"id": 1,
		"title": "新闻标题",
		"content": "新闻内容",
		"image": null,
		"author": null,
		"publishTime": "2023-01-01T00:00:00",
		"categoryId": 1,
		"views": 1,
		"relatedNews": []
	}
}
```
