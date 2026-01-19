# GitHub添加SSH密钥详细步骤

## 📋 你的SSH公钥

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKgvph7TEbXAj1a75DUvFoy4e67kAY4orJcx40JdyUoj github
```

## 🔑 添加步骤（图文说明）

### 方法1：通过网页添加（推荐）

1. **打开GitHub网站**
   - 访问：https://github.com
   - 登录你的账号

2. **进入设置页面**
   - 点击右上角头像
   - 选择 **Settings**（设置）

3. **进入SSH密钥页面**
   - 在左侧菜单中找到 **SSH and GPG keys**
   - 点击进入

4. **添加新密钥**
   - 点击绿色的 **New SSH key** 按钮
   - 或者点击 **Add SSH key** 按钮

5. **填写密钥信息**
   - **Title**（标题）：填写一个描述性名称
     - 例如：`Windows PC`、`我的电脑`、`工作电脑` 等
   - **Key type**（密钥类型）：选择 `Authentication Key`
   - **Key**（密钥内容）：粘贴上面的公钥
     ```
     ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKgvph7TEbXAj1a75DUvFoy4e67kAY4orJcx40JdyUoj github
     ```

6. **保存**
   - 点击 **Add SSH key** 按钮
   - 可能需要输入GitHub密码确认

### 方法2：直接访问链接

直接访问以下链接（需要登录）：
```
https://github.com/settings/keys
```

然后点击 **New SSH key** 按钮，按照上面的步骤5-6操作。

## ✅ 验证是否添加成功

添加完成后，在终端执行：

```bash
ssh -T git@github.com
```

如果看到类似以下消息，说明添加成功：
```
Hi MRYGP! You've successfully authenticated, but GitHub does not provide shell access.
```

## 📝 快速复制公钥

如果需要在其他地方复制公钥，可以运行：

**PowerShell:**
```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

**Git Bash:**
```bash
cat ~/.ssh/id_ed25519.pub
```

## 🎯 添加完成后的操作

添加成功后，告诉我，我会：
1. 测试SSH连接
2. 切换到SSH方式
3. 使用22端口推送修复后的提交

## ⚠️ 注意事项

1. **只添加公钥**：只需要添加 `.pub` 文件的内容，不要添加私钥
2. **公钥可以分享**：公钥是公开的，可以安全地添加到GitHub
3. **私钥要保密**：私钥（`id_ed25519`）绝对不能分享或上传

## 🔗 相关链接

- GitHub SSH密钥设置：https://github.com/settings/keys
- GitHub SSH文档：https://docs.github.com/en/authentication/connecting-to-github-with-ssh

---

**你的SSH公钥位置**：`C:\Users\Administrator\.ssh\id_ed25519.pub`
