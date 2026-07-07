# 1. 创建项目文件夹
mkdir ~/Desktop/stock_analyzer
cd ~/Desktop/stock_analyzer

# 2. 初始化 Git（便于版本管理）
git init

# 3. 创建虚拟环境（隔离依赖）
python3 -m venv venv   # Mac
# Windows 用: python -m venv venv

# 4. 激活虚拟环境
source venv/bin/activate   # Mac
# Windows 用: venv\Scripts\activate

# 5. 安装必要库
pip install customtkinter akshare pandas numpy

# 6. 创建子目录
mkdir data cache gui
以后每次打开项目，都要 cd ~/Desktop/stock_analyzer + source venv/bin/activate（Mac）激活环境。
Git 已经初始化，后续我们会用 git add . 和 git commit -m "消息" 来保存版本。
