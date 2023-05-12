<div align="center">
  <a href="https://github.com/sanmaomashi/FileParse">
    <img src="https://raw.githubusercontent.com/sanmaomashi/FileParse/main/img/1.jpg" height="400">
  </a>
  <h1>File Parse Service</h1>
  <img src="https://img.shields.io/github/repo-size/sanmaomashi/FileParse.svg?label=Repo%20size&style=flat-square" height="20">
  <img src="https://img.shields.io/badge/License-Apache%202.0-purple" data-origin="https://img.shields.io/badge/License-Apache%202.0-blue" alt="">
</div>




## 简介

基于fastapi构建文件解析项目 支持txt文件、docx文件、doc文件、excel文件、csv文件、ppt文件、json文件、扫描pdf、非扫描pdf、图片、音频转文字



## 免责声明

本仓库为非盈利仓库，对任何法律问题及风险不承担任何责任。

本仓库没有任何商业目的，如果认为侵犯了您的版权，请来信告知。

本仓库不能完全保证内容的正确性。通过使用本仓库内容带来的风险与本人无关。



## 本地部署

1. 克隆项目

```bash
git clone https://github.com/sanmaomashi/FileParse.git
```

2. 安装依赖

```bash
pip install -r requirements -i https://mirror.baidu.com/pypi/simple
```

3. 执行项目

```bash
cd /项目目录/bin
bash start_project.sh
```

4. 访问swagger ui

```http
http://{{ip}}:1701/docs
```

![](https://raw.githubusercontent.com/sanmaomashi/FileParse/main/img/2.png)

## docker部署

构建镜像

```bash
docker build -t nlp:file_parse .
```

启动容器

```bash
docker run -d --name fileparse -p 1701:1701 --restart=always nlp:file_parse
```

访问swagger ui

```http
http://{{ip}}:1701/docs
```

![](https://raw.githubusercontent.com/sanmaomashi/FileParse/main/img/3.png)



## License

Licensed under the [Apache-2.0](http://choosealicense.com/licenses/apache/) © FileParse

