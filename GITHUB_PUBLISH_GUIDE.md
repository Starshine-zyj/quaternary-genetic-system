# 📤 GitHub 发布操作指南

## 🎯 目标

将**四进制基因编程演化系统**项目发布到 GitHub，并确保：
- ✅ 使用 `main` 分支（而非 `master`）
- ✅ 包含 Apache 2.0 License
- ✅ 包含完整的 .gitignore
- ✅ 代码结构清晰，文档完善

---

## 📋 准备工作检查清单

### 1. 本地文件确认

```
✅ 已完成的准备工作：
├── .gitignore（已创建，完整的 Python 项目配置）
├── LICENSE（已创建，Apache 2.0）
├── README.md（项目文档）
├── requirements.txt（依赖管理）
└── 所有源代码文件
```

### 2. GitHub 账号准备

```
需要确保：
├── 已注册 GitHub 账号
├── 已配置 Git 用户信息
└── 已配置 GitHub 认证方式
```

---

## 🚀 快速发布（推荐方式）

### 方法一：使用自动化脚本 ⭐

**Windows 用户：**
```bash
# 双击运行
git_push_to_github.bat
```

**Linux/Mac 用户：**
```bash
# 添加执行权限
chmod +x git_push_to_github.sh

# 运行脚本
./git_push_to_github.sh
```

**脚本会自动完成：**
1. ✅ 初始化 Git 仓库
2. ✅ 设置默认分支为 `main`
3. ✅ 添加所有文件
4. ✅ 创建初始提交
5. ✅ 推送到 GitHub

---

## 🔧 手动发布（详细步骤）

### 步骤 1：在 GitHub 创建新仓库

1. 登录 GitHub：https://github.com
2. 点击右上角 `+` → `New repository`
3. 填写仓库信息：
   ```
   Repository name: quaternary-genetic-evolution
   Description: 四进制基因编程演化系统 - 基于四进制编码的遗传算法实验平台
   Visibility: Public（或 Private）
   ⚠️ 不要勾选以下选项：
      □ Add a README file
      □ Add .gitignore
      □ Choose a license
   ```
4. 点击 `Create repository`
5. **复制仓库 URL**（例如：`https://github.com/yingjiezhu/quaternary-genetic-evolution.git`）

---

### 步骤 2：配置 Git 用户信息（首次使用）

```bash
# 设置用户名
git config --global user.name "yingjiezhu"

# 设置邮箱
git config --global user.email "your_email@example.com"

# 查看配置
git config --list
```

---

### 步骤 3：初始化本地 Git 仓库

```bash
# 进入项目目录
cd "d:\工作日志\杂项\胡思乱想\四进制基因编程演化系统"

# 初始化 Git 仓库
git init

# 设置默认分支为 main（重要！）
git branch -M main
```

---

### 步骤 4：添加文件并提交

```bash
# 添加所有文件到暂存区
git add .

# 查看将要提交的文件
git status

# 创建初始提交
git commit -m "Initial commit: 四进制基因编程演化系统 v1.0" \
           -m "- 完整的四进制基因编程演化框架" \
           -m "- 支持 GUI 界面操作" \
           -m "- 包含完整文档和示例" \
           -m "- Apache 2.0 License"
```

---

### 步骤 5：连接到 GitHub 远程仓库

```bash
# 添加远程仓库（替换为你的仓库 URL）
git remote add origin https://github.com/yingjiezhu/quaternary-genetic-evolution.git

# 验证远程仓库
git remote -v
```

---

### 步骤 6：推送到 GitHub

```bash
# 推送到 main 分支
git push -u origin main
```

**可能遇到的问题和解决方法：**

#### 问题 1：需要身份验证

**错误信息：**
```
Username for 'https://github.com': 
Password for 'https://yingjiezhu@github.com':
```

**解决方法 A：使用 Personal Access Token（推荐）**

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. 勾选权限：`repo`（完整仓库访问权限）
4. 生成 Token 并复制
5. 推送时：
   ```
   Username: yingjiezhu
   Password: <粘贴 Token>
   ```

**解决方法 B：使用 SSH Key**

```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥
cat ~/.ssh/id_ed25519.pub

# 添加到 GitHub: Settings → SSH and GPG keys → New SSH key

# 修改远程 URL 为 SSH
git remote set-url origin git@github.com:yingjiezhu/quaternary-genetic-evolution.git

# 推送
git push -u origin main
```

#### 问题 2：远程仓库不为空

**错误信息：**
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/...'
```

**解决方法：**

```bash
# 方法 1：强制推送（会覆盖远程内容，谨慎使用）
git push -u origin main --force

# 方法 2：先拉取再合并
git pull origin main --allow-unrelated-histories
git push -u origin main
```

#### 问题 3：网络问题

**解决方法：**

```bash
# 配置代理（如果使用代理）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 或临时使用 SSH
git remote set-url origin git@github.com:yingjiezhu/quaternary-genetic-evolution.git
```

---

## ✅ 验证发布成功

### 1. 检查 GitHub 仓库

访问：`https://github.com/yingjiezhu/quaternary-genetic-evolution`

应该看到：
- ✅ 所有文件已上传
- ✅ README.md 正确显示
- ✅ LICENSE 显示为 Apache-2.0
- ✅ 分支是 `main`（不是 `master`）

### 2. 检查本地分支

```bash
# 查看当前分支
git branch

# 应该显示：
* main

# 查看远程分支
git branch -r

# 应该显示：
origin/main
```

---

## 🔄 master 到 main 的迁移说明

### 为什么使用 main 而不是 master？

```
历史原因：
├── Git 默认分支曾是 master
├── 2020 年起，GitHub 改用 main 作为默认分支
└── 原因：避免奴隶制相关术语（master/slave）

现状：
├── GitHub 新仓库默认使用 main
├── 大多数开源项目已迁移到 main
└── 推荐所有新项目使用 main
```

### 如果已经使用了 master 分支

**情况 1：本地仓库已有 master 分支**

```bash
# 重命名 master 为 main
git branch -m master main

# 推送到远程
git push -u origin main

# 删除远程 master（可选）
git push origin --delete master
```

**情况 2：远程仓库是 master，想改为 main**

```bash
# 在 GitHub 仓库页面：
# Settings → Branches → Default branch → 改为 main → Update

# 本地更新
git branch -m master main
git fetch origin
git branch -u origin/main main
git remote set-head origin -a
```

---

## 📝 后续维护

### 日常更新流程

```bash
# 1. 修改代码后，查看状态
git status

# 2. 添加修改的文件
git add .

# 3. 提交修改
git commit -m "描述你的修改"

# 4. 推送到 GitHub
git push
```

### 创建新版本标签

```bash
# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

### 查看提交历史

```bash
# 查看提交历史
git log --oneline

# 查看图形化历史
git log --graph --oneline --all
```

---

## 🎨 完善 GitHub 仓库

### 1. 添加仓库描述

在仓库页面点击 `About` 右侧的 ⚙️ 设置：

```
Description: 
四进制基因编程演化系统 - 基于四进制编码的遗传算法实验平台

Website: 
（可选）你的项目主页或文档网站

Topics (标签):
genetic-algorithm
evolutionary-computation
quaternary-encoding
python
artificial-intelligence
machine-learning
```

### 2. 添加封面图片

将 `A_DNA_double_helix_icon_in_vib_2026-03-12T06-57-01.png` 上传为 Social Preview：

```
Settings → Options → Social preview → Upload an image
```

### 3. 设置 GitHub Pages（可选）

如果想发布文档网站：

```
Settings → Pages → Source → main branch → /docs folder → Save
```

### 4. 添加 Shields 徽章

在 README.md 顶部添加：

```markdown
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
```

---

## 🆘 常见问题 FAQ

### Q1: 推送时需要输入用户名密码，很麻烦？

**A:** 配置凭据存储：

```bash
# Windows
git config --global credential.helper wincred

# Linux
git config --global credential.helper store

# macOS
git config --global credential.helper osxkeychain
```

### Q2: 如何撤销最后一次提交？

```bash
# 撤销提交但保留修改
git reset --soft HEAD~1

# 撤销提交并丢弃修改（危险！）
git reset --hard HEAD~1
```

### Q3: 如何忽略已经被跟踪的文件？

```bash
# 从 Git 中移除但保留本地文件
git rm --cached <file>

# 然后添加到 .gitignore
echo "<file>" >> .gitignore

# 提交更改
git commit -m "Stop tracking <file>"
```

### Q4: 如何查看某个文件的修改历史？

```bash
# 查看文件提交历史
git log -- <file>

# 查看文件每行的修改记录
git blame <file>
```

### Q5: 如何删除远程仓库的文件？

```bash
# 删除远程文件（本地保留）
git rm --cached <file>
git commit -m "Remove <file> from repository"
git push

# 删除远程文件（本地也删除）
git rm <file>
git commit -m "Delete <file>"
git push
```

---

## 📚 学习资源

### Git 基础教程
- **Git 官方文档**：https://git-scm.com/doc
- **GitHub 指南**：https://guides.github.com/
- **Pro Git 书籍**：https://git-scm.com/book/zh/v2
- **交互式学习**：https://learngitbranching.js.org/

### GitHub 功能
- **Actions（CI/CD）**：https://github.com/features/actions
- **Issues（问题跟踪）**：https://guides.github.com/features/issues/
- **Wiki（文档）**：https://guides.github.com/features/wikis/
- **Projects（项目管理）**：https://docs.github.com/en/issues/planning-and-tracking-with-projects

---

## ✨ 总结

### 完整操作流程回顾

```bash
# 1. 在 GitHub 创建空仓库
# 2. 配置 Git 用户信息
git config --global user.name "yingjiezhu"
git config --global user.email "your_email@example.com"

# 3. 初始化并推送
cd "项目目录"
git init
git branch -M main
git add .
git commit -m "Initial commit"
git remote add origin <仓库URL>
git push -u origin main

# 完成！🎉
```

### 关键要点

| 项目 | 说明 |
|------|------|
| **默认分支** | 使用 `main`（不是 `master`） |
| **License** | Apache 2.0（已配置） |
| **`.gitignore`** | Python 完整配置（已创建） |
| **认证方式** | Personal Access Token 或 SSH Key |
| **提交信息** | 清晰描述每次修改 |

---

## 🎉 恭喜！

如果你看到这里，说明你已经掌握了如何将项目发布到 GitHub。

**下一步建议：**
1. ✅ 完善 README.md 文档
2. ✅ 添加使用示例和截图
3. ✅ 邀请协作者参与开发
4. ✅ 设置 GitHub Actions 自动化测试
5. ✅ 发布第一个 Release 版本

---

**祝你的开源项目成功！** 🚀
