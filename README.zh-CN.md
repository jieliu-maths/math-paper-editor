# Math Paper Editor

**先检查论证，保留作者原意，让修订可追踪。**

面向 LaTeX 数学论文的 Codex skill，首先服务分析与 PDE。版本 **0.1.0**。

[English](README.md) · [评测](evals/README.md) ·
[版本记录](CHANGELOG.md) · [贡献指南](CONTRIBUTING.md) · [MIT](LICENSE)

| 模式 | 是否修改论文 | 工作重点 |
| --- | --- | --- |
| review | 不修改 | 核心论证、重要缺口与表达问题 |
| edit | 在指定范围修改 | 必要语言修改，允许零修改 |
| deep-review | 不修改 | 重建承重估计，核对假设、端点和反例 |
| rewrite | 在指定范围修改 | 重组已有证明、简化辅助记号、补清可验证步骤 |

区分已确认错误、缺少论证、未核验引用和表达歧义。普通编辑不得静默改动假设、
指数、收敛方式或结论。重写允许等价推导和获准的记号调整，不自动授权新定理
或未经证明的修补。保留作者风格、宏、标签、引用键和项目约定。

## 安装与升级

工具需要 **Python 3.10+**，仅用标准库；使用技能需要启用技能的 Codex 环境。
CI 覆盖 macOS 与 Linux，Windows 与其他宿主适配尚未单独验证。
不内置模型、API 密钥、TeX 发行版、证明器或真实未发表论文。

~~~sh
git clone https://github.com/jieliu-maths/math-paper-editor.git
cd math-paper-editor
git checkout v0.1.0
python3 tools/check.py
python3 tools/install.py
python3 tools/install.py --apply
~~~

前一个安装命令只预览，--apply 才实际安装。默认目标为
~/.agents/skills/math-paper-editor，可用 --dest 指定已有约定的位置。
保持一个可发现的安装副本。新版本可在下一轮调用，发现未刷新时新开会话。

升级遇到已管理文件的本地修改、删除或未管理文件冲突时停止；保留额外文件，
在技能发现目录之外完整备份旧安装。已有未管理安装需要精确的私有基线。
详见 [安装与维护](docs/installation.md)。

## 在论文目录中调用

输入写在 Codex 对话框，不是终端：

~~~text
$math-paper-editor review main.tex
$math-paper-editor edit introduction
$math-paper-editor deep-review main.tex
$math-paper-editor rewrite main.tex
~~~

例如：“为本领域博士生重写 Lemma 2 的证明，保留假设、结论、宏、标签和参考文献，
解释关键估计，减少没有独立作用的辅助记号，交付实际改稿、源码、快照、完整 diff
与真实编译状态。”

遵守目标论文项目自己的约定和审批边界。指定一节允许读取依赖，只修改该节。
报告随用户语言，论文默认保留原语言。

## 修改记录

保存开始时的真实字节，包括作者已有未提交修改。写入前核对当前版本，
发现未登记变化就拒绝覆盖。

| 记录 | 含义 |
| --- | --- |
| before/ | 原稿快照 |
| editor/ 与 editor.diff | 经工具登记并应用的修改 |
| after/ 与 changes.diff | 最终观察到的源文件与总差异 |
| unattributed.diff | 登记操作无法解释的变化 |
| manifest.json | 哈希、操作与完成/冲突状态 |

记录包含论文副本和绝对运行路径，应保持私有。快照与安装工具不联网；
AI 宿主如何处理文本仍取决于宿主设置与政策。
工具是乐观版本检查，不是排他文件锁、作者认证、LaTeX 语义分析器或证明器。
v0.1 的新增、删除源文件需要另行记录。
详见 [编辑流程](skills/math-paper-editor/references/editing.md)。

## 测试与评测

~~~sh
python3 tools/check.py
python3 -m unittest discover -s tests -v
python3 skills/math-paper-editor/scripts/changes.py self-test
~~~

CI 执行确定性工具测试与发布检查。另有 **10 个自建行为案例**，覆盖正确与错误
证明、局部编辑、零修改、结构重写与无法核验的引用。准备案例不调用模型，
不读取真实论文。[评测方法](evals/README.md) 与
[v0.1.0 评测记录](evals/results/v0.1.0.md) 分别说明工具结果与模型表现。
小规模回归不足以证明普遍数学可靠性、优于其他产品或提高科研生产率。

## 长期维护与科研工作流

真实问题 → 匿名最小案例 → 验收标准 → 小范围改进 → 与旧版对照 → 发布版本。
本仓库是唯一维护源码，本机安装是带版本副本。保留正确证明作为误报对照，
将特定论文机制放入按需加载的参考指南。

可独立使用，也可配合
[AI Research Workflow](https://github.com/jieliu-maths/AI-Research-Workflow)：
后者维护科研证据和获准状态，本技能修订指定稿件。论文改写不能批准科研命题
或提升证据状态。

MIT 许可，版权所有 2026 Jie Liu。许可证涵盖本仓库代码、文档和自建样例，
不改变用户论文的所有权或许可；外部文献和服务保留各自条款。
