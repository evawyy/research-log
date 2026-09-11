# GPU 一阶凸 QCQP 求解器

## 核心问题

理解并参与开发面向凸 QCQP 的 GPU 一阶求解器，包括问题重构、算法推导、收敛判据和 GPU 实现。

## 当前阶段

- 2026-09-10 起，项目重心从单纯阅读论文转为“代码和实验先跑通，论文与理论同步反查”。
- 国庆前（2026-10-01 前）优先进入实验状态：跑通孙德峰老师团队相关代码、自带例子和 QPB 数据，形成可展示结果。
- 同步精读 APDB / 当前项目论文，以及孙德峰老师团队 HAPEN / HPR-QP 相关论文，重点服务于算法对比、代码理解和汇报表达。
- 2026-09-11 已跑通 HRQ 和 Hongpei PDHCG 两个 baseline，并开始整理 HAMS 榜单与 convex QCQP benchmark；后续重点是把自己的 QCQP solver、QCQP 转 SOCP 后的 HRQ、PDHCG 放入同一批实例中比较。

## 近期目标

- 跑通孙德峰老师团队的两个代码项目，记录依赖、入口、最小示例、数据路径和输出指标。
- 使用 QPB 网站数据做初步实验，熟悉该领域常用测试集和评测流程。
- 后续拿到组内代码后，在同一批数据上对比组内算法和孙老师团队代码，说明速度、稳定性和工程优势。
- 准备 20 页以内 PPT，争取 2026-09-19 向师姐汇报；若准备不足，最迟 2026-09-26 汇报。
- 获取并整理 convex QCQP benchmark，优先确认 HAMS 中哪些实例可以直接使用。
- 完成 QCQP 到 SOCP 的统一转换，并统一三套 solver 的 stopping criterion、tolerance、time limit、硬件和线程设置。

## 阅读时必须回答

- 原问题的标准形式和假设是什么？
- 算法每一步如何从最优性条件推导？
- 哪些算子最耗时，哪些适合 GPU？
- 停止准则、残差和数值稳定性如何定义？
- 与 PDHG、PDLP、APD/APDB 的关系是什么？
- 论文 introduction 中对比了哪些经典方法？各方法的收敛 order 是什么？
- 收敛结论针对最后迭代点还是平均迭代点？为什么会有这个区别？
- 原始-对偶步长解耦、momentum 外推、梯度外推、迭代点外推、加权迭代点和加权梯度分别解决什么问题？
- HAPEN / HPR-QP 路线与 PD / PDHG 路线在建模、子问题、残差和 GPU 映射上有什么不同？

## 代码学习时必须回答

- 如何安装依赖并运行最小示例？
- 数据如何加载，QPB 数据如何转成代码需要的格式？
- 核心入口函数、核心算子和测试脚本分别在哪里？
- 算法伪代码与代码文件如何对应？
- 哪些实现技巧可迁移到组内 GPU QCQP 求解器？
- 与组内算法比较时，公平评测口径是什么？

## 当前问题清单

- 法锥为什么可以用来刻画互补松弛条件。
- APDB 与 PDHG / PDHCG 的核心区别。
- EGM / extragradient method 的定义、用途和与 PD 类方法的关系。
- HAPEN 加速和 HPR-QP 的 restricted Wolfe dual、symmetric Gauss-Seidel、range-space update 等机制。
- QPB 数据组织方式和 QCQP 生成数据的建模合理性。
- 李的项目截至 2026-09-10 仍未跑通，需要继续定位运行入口和依赖问题。
- QCQP / functional SOCP / standard SOCP 之间的 formulation 对应关系，以及 KKT 条件如何逐项对应。
- centered gap、error bound、quadratic growth 在局部线性收敛分析中的具体作用。
- Exact-x / APDB 一类算法中的步长选择和 backtracking 机制。

## 近期实验进展

- 2026-09-11：HRQ 和 Hongpei PDHCG 已经作为 baseline 跑通，下一步准备与自己的 QCQP solver 做统一实验。
- 2026-09-11：计划对同一个 convex QCQP 分别测试直接 QCQP solver、转 SOCP 后的 HRQ、PDHCG，并比较求解时间、收敛情况、数值稳定性和不同实例类型上的表现。
- 2026-09-11：Hongpei PDHCG 已补充 CUDA / cuSPARSE 版本兼容处理。CUDA 13.3 / cuSPARSE 12.8.2+ 使用新的 `cusparseSpMVOp_bufferSize`、`cusparseSpMVOp_createDescr` 和 `CUSPARSE_SPMVOP_ALG_DEFAULT`；CUDA 13.2 / cuSPARSE 12.7.x 保留旧版 SpMVOp API；更旧版本 fallback 到标准 `cusparseSpMV`。
- 2026-09-11：已在 CUDA 13.3.73 与 CUDA 13.2.78 环境下分别构建验证，`cmake --build build-cuda133 --parallel 4` 和 `cmake --build build-cuda132 --parallel 4` 均可通过。

## 沟通与展示

- 主动推动和小磊建立实验讨论群，跟进组内代码和新模块测试进展。
- 多向郭晓乐、张成等同学请教 AI 使用、代码运行和工具链经验。
- 组会展示时突出“正在看代码、跑实验、理解求解器”，避免只呈现理论阅读。
- 如需讨论导师归属，私下向葛老师表达想留在当前方向，并说明正在推进代码、论文和项目参与。

## 下一步

- 先用 AI / Codex 拆解孙老师团队代码：目录结构、依赖、运行入口、数据路径、示例脚本、测试指标。
- 跑通自带例子，再接 QPB 数据；每次运行记录命令、环境、数据、结果和失败原因。
- 重读 APDB / 当前项目论文的摘要和 introduction，做“经典方法—order—最后/平均迭代点—与本文差异”表格。
- 阅读 HPR-QP / HAPEN 论文，重点理解其模型、算法伪代码、GPU 实验和与 PDQP、SCS、Gurobi 等求解器的比较。
- 先选择少量 convex QCQP / HAMS 实例跑通完整实验 pipeline。
- 在正式 benchmark 中记录 PDHCG 的运行时间、收敛信息和 CUDA 版本。
