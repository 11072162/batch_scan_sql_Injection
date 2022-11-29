<!--
 * @Author: xiaotian
 * @Date: 2022-11-25 20:34:14
 * @LastEditors: xiaotian
 * @LastEditTime: 2022-11-25 21:51:14
 -->
# batch_scan_sql_Injection

[English](./README_EN.md)

批量扫描网站sql注入

那么接下来看看batch_scan_sql_Injection的**特点**吧

# 功能特点

1. 支持批量扫描网站sql注入
2. 支持自定义参数
3. 并发扫描

# 使用方法

## 环境准备

```shell
git clone https://github.com/11072162/batch_scan_sql_Injection.git && cd batch_scan_sql_Injection && python3 -m pip install -r requirement.txt

```

## 快速使用

### 输入目标

单目标，默认为http

```shell
python3 sqlinject.py -u https://github.com
```

### 文件读取

```shell
python3 sqlinject.py -r url.txt
```

### 结果保存

1. 结果将自动保存在result.txt中，一个url一行
2. 结果自动去重复，不用担心产生大量冗余

# 维护工作

1. 若使用过程中出现问题，欢迎发issue

# 联系作者

mail: qq11072162@gmail.com

![donate](doc/donate.jpg)
