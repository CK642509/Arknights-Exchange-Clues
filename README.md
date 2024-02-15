# Arknights-Exchange-Clues
## 簡介
這是一個給明日方舟玩家使用的工具，用於計算玩家之間交換相同線索的最佳解

## 動機
原先是 Yao 開發出第一版 (用 C++ 寫的，再編譯成執行檔)，但後續為了讓大家使用起來更方便，我嘗試整合到 [Discord BOT](https://github.com/CK642509/DiscordBOT-Arknights) 上 (使用 Python 開發)。過程中遇到了諸多問題，儘管最終算是有成功整合，但該作法會導致在部屬 Discord BOT 時，只適合部屬在 Windows 電腦中，很難打包成 Docker image。

因此，希望使用 Python 重構整個工具。
