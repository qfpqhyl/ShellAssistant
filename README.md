# ShellAssistant

ShellAssistant 是一个命令行工具，可以帮助 Windows 用户和Linux用户（TODO）提供适合的 shell 命令推荐和修复失败的 shell 命令建议。

## 安装

1. 克隆仓库：

    ```sh
    git clone https://github.com/qfpqhyl/ShellAssistant.git
    ```

2. 进入项目目录：

    ```sh
    cd ShellAssistant
    ```

4. 安装所需的 Python 包：

    ```sh
    pip install -r requirements.txt
    ```

5. 将`bat` 文件所在 `Windows` 目录添加到系统的 PATH 环境变量中，以便可以从任何命令行位置使用 `ask` 和 `fix` 命令。

## 使用

| ask.bat                           | fix.bat                           |
| --------------------------------- | --------------------------------- |
| 根据用户查询获取 shell 命令推荐。 | 诊断和建议修复失败的 shell 命令。 |

## API 配置

在 `ask.py` 和 `shell_fix.py` 文件中设置 `base_url` 和 `sessionid`。参考 [doubao-free-api](https://github.com/LLM-Red-Team/doubao-free-api) 获取详细信息。

```python
base_url = "your_base_url"
sessionid = "your_session_id"
```

## 效果截图

### ask 命令的示例使用

![ask 命令截图](https://im.gurl.eu.org/file/AgACAgEAAxkDAAIPwWdxQJ-vPOqBU3Q4PJJhiQVgEE2gAAL0rzEbfCuJR6DluyA7-LCZAQADAgADeQADNgQ.png)

### fix 命令的示例使用

![fix 命令截图](https://im.gurl.eu.org/file/AgACAgEAAxkDAAIPwmdxQLsY5h0axNlb_CrE99oFjSm4AAL1rzEbfCuJRwd-AS-EnUKXAQADAgADeQADNgQ.png)

## 贡献

欢迎提交 issue 或 pull request 以改进项目。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
