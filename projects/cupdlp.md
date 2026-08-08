# cuPDLP.jl 学习

## 目标

能够运行 cuPDLP.jl、解释主要代码调用链，并理解 LP 一阶方法如何映射到 NVIDIA GPU。

## 当前入口

- JuMP 接口：`cuPDLP.Optimizer`
- 推荐脚本：`scripts/solve.jl`

## 学习检查点

- [ ] 跑通一个最小 LP 实例。
- [ ] 画出读取实例到输出结果的调用链。
- [ ] 定位预处理、缩放和迭代主体。
- [ ] 找到稀疏矩阵乘和 CUDA kernel 的实现位置。
- [ ] 对照 FirstOrderLp.jl 理清继承与修改部分。

## 下一步

从 `scripts/solve.jl` 出发，用调用关系追踪到求解器迭代循环。

