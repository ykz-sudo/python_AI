import torch
import matplotlib.pyplot as plt

class Trainer:
    def __init__(self, model, train_loader, val_loader, criterion, optimizer, device, eval_step=100):
        """
        初始化 Trainer 类，用于训练和评估神经网络模型
        参数说明:
            model: 神经网络模型
            train_loader: 训练集的DataLoader
            val_loader: 验证集的DataLoader
            criterion: 损失函数（如CrossEntropyLoss）
            optimizer: 优化器（如Adam等）
            device: 设备 (如 "cpu" 或 "cuda")
            eval_step: 训练过程中多少个batch后做一次验证
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.eval_step = eval_step

        # 这行代码的作用是将神经网络模型移动到指定的设备（如CPU或GPU），从而加速计算或利用GPU，提高训练和推理效率
        self.model.to(self.device)

        # 以下用于保存每个batch的损失和准确率历史，用于后续绘图分析
        self.train_loss_history = []  # 训练集损失，每个batch一个
        self.val_loss_history = []    # 验证集损失，每eval_step记录一次
        self.train_acc_history = []   # 训练集准确率，每个batch一个
        self.val_acc_history = []     # 验证集准确率，每eval_step记录一次

    def train(self, num_epochs):
        """
        主训练循环，训练指定轮数(num_epochs)
        """
        global_step = 0  # 全局步数计数（以batch为单位）
        for epoch in range(num_epochs):
            # 进入训练模式用 self.model.train()，进入评估（验证/测试）模式用 self.model.eval()。
            # 训练时（即训练集循环）要调用 self.model.train()，这样像Dropout、BatchNorm等层会采用训练时的行为。
            # 验证或推理（eval/inference）时要调用 self.model.eval()，这样这些层会切换到推理行为（如Dropout失效，BatchNorm用全局均值/方差）。
            # 一般流程：训练epoch开始前调用 self.model.train()，评估前（如在验证集跑一遍）调用 self.model.eval()。
            self.model.train()
            
            train_loss = 0.0    # 当前epoch累积损失
            train_correct = 0   # 当前epoch累积正确预测数
            train_total = 0     # 当前epoch样本总数

            # 这里的用法是使用enumerate遍历DataLoader（self.train_loader），
            # enumerate会返回每个batch的下标（batch_idx）以及数据（batch）。
            # 这样可以在训练循环中既获得当前是第几个batch，也获得数据本身。
            for batch_idx, batch in enumerate(self.train_loader):
                # 解包batch数据，获取输入和目标
                inputs, targets = batch
                # 数据移动到指定device
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)

                # 梯度清零
                self.optimizer.zero_grad()

                # 前向传播，outputs 通常是模型输出的“分数”（logits），不是 softmax 后的概率。
                # 绝大多数 PyTorch 分类模型，最后一层不会自动加 softmax，因为常用的损失函数如 CrossEntropyLoss 要求输入 logits。
                outputs = self.model(inputs)
                
                # 计算损失
                loss = self.criterion(outputs, targets)
                # 反向传播
                loss.backward()
                # 更新参数
                self.optimizer.step()
                
                # 计算当前batch的损失值，其中loss是一个标量张量（即只有一个元素），调用item()方法将其从张量类型转换为Python的float类型
                # 这一步的作用是为了便于后续进行数值计算、累加或存入列表，因为直接用张量类型可能会带来不便
                batch_loss = loss.item()

                # 获取预测类别：
                # outputs 是神经网络的输出，通常形状为 (batch_size, num_classes)，
                # 其中每一行包含该样本属于每个类别的“分数”（如 logits 或概率）。
                # torch.argmax(outputs, dim=1) 的作用是
                #   沿着第1维（即类别维）找出每个样本分数最大的下标（类别编号），
                #   结果是一个长度为 batch_size 的整型张量，每个元素都是对应样本的预测类别编号。
                predicted = torch.argmax(outputs, dim=1)
                # 当前batch预测正确的数量
                batch_correct = (predicted == targets).sum().item()

                # 当前batch总样本数:
                # 这里我们计算本次迭代(batch)中的样本数量。
                # 在PyTorch的DataLoader中，targets（标签）通常是一个一维张量，其长度等于本batch的样本个数。
                # 例如，如果本batch有32个样本，则targets.size(0)的值就是32。
                # 这样可以方便后续进行累计样本数、分母用于计算准确率等。
                batch_total = targets.size(0)
                
                # 当前batch准确率
                batch_acc = batch_correct / batch_total if batch_total > 0 else 0

                # 记录本batch的损失和准确率到历史列表
                self.train_loss_history.append(batch_loss)
                self.train_acc_history.append(batch_acc)

                # 对epoch的损失与准确率做累加
                train_loss += batch_loss * batch_total  # 需乘以样本数得到总损失
                train_correct += batch_correct
                train_total += batch_total

                global_step += 1  # 全局步数+1

                # 每到eval_step的整数倍，做一次验证集评估
                if self.eval_step is not None and self.eval_step > 0 and global_step % self.eval_step == 0:
                    val_loss, val_acc = self.evaluate_once()
                    self.val_loss_history.append(val_loss)
                    self.val_acc_history.append(val_acc)
                    print(f"[Step {global_step}] Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}")

            # 可选：在每个epoch结束时再做一次验证（已注释）
            # val_loss, val_acc = self.evaluate_once()
            # self.val_loss_history.append(val_loss)
            # self.val_acc_history.append(val_acc)
            
            # 本段代码用于在每个epoch(训练轮)结束后，计算当前epoch的平均训练损失（loss）和准确率（accuracy）。
            # 这里的train_loss、train_correct和train_total都是在前面的循环中按batch累加得到的。

            # 计算平均训练损失:
            # - train_loss 变量在整个epoch中累加了每个batch的损失（注意：每个batch的loss已乘以该batch的样本数，即为当前batch所有样本的总损失）。
            # - len(self.train_loader.dataset) 表示整个训练集的总样本数。
            #   -> 所以，train_loss / len(self.train_loader.dataset) 便得到了该epoch下，所有样本对应的平均损失值。
            avg_train_loss = train_loss / len(self.train_loader.dataset)

            # 计算平均训练准确率:
            # - train_correct 变量在整个epoch中累加了每个batch预测正确的样本数，总数即为本epoch所有被正确分类的样本数。
            # - train_total 记录了当前epoch参与训练的总样本数（通常等于len(self.train_loader.dataset)，但为稳妥及兼容，实际采用该变量）。
            #   -> train_correct / train_total 即为本epoch整体的准确率。如果总样本数为0（极端情况，如数据集为空），则准确率返回0以避免除零错误。
            avg_train_acc = train_correct / train_total if train_total > 0 else 0

            # 输出当前训练轮(epoch)的详细信息，包括训练损失和准确率
            # - epoch+1: 表示当前是第几个epoch（从1计数，便于理解）
            # - num_epochs: 总共训练多少个epoch
            # - avg_train_loss: 当前epoch的平均训练损失，保留4位小数
            # - avg_train_acc: 当前epoch的平均训练准确率，保留4位小数
            # 这样可以直观地看到训练过程中损失和准确率的变化，有助于监控模型收敛情况
            print(
                f"Epoch [{epoch+1}/{num_epochs}] "
                f"Train Loss: {avg_train_loss:.4f} "
                f"Train Acc: {avg_train_acc:.4f}"
            )

    def evaluate_once(self):
        """
        在整个验证集(val_loader)上评估模型的损失和准确率
        返回: (平均损失, 平均准确率)
        """
        self.model.eval()  # 设置为评估模式
        val_loss = 0.0     # 验证集损失总和
        correct = 0        # 正确预测总数
        total = 0          # 验证数据总条数

        # 使用 torch.no_grad() 让PyTorch在该代码块里不追踪张量的计算图，避免自动求导，占用更少显存并加速推理阶段。
        # 这是验证/推理（即不需要反向传播和梯度的情况）常用的写法。
        with torch.no_grad():
            # 遍历整个验证集的 DataLoader。每次取一批(batch)数据进行模型评估。
            for batch in self.val_loader:
                # 解包 batch，获得输入（inputs）和标签（targets）
                # DataLoader 的每个batch通常是元组 (data, labels)
                inputs, targets = batch

                # 将输入和标签迁移到模型所在的device上（如GPU或CPU）。
                # 这样模型和数据在同一设备上才能正常计算。
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)

                # 前向传播（推理）：将输入传入模型，获得输出结果（未经过softmax的logits）
                outputs = self.model(inputs)

                # 使用损失函数（如交叉熵）计算当前batch的损失，loss是（标量张量）
                loss = self.criterion(outputs, targets)

                # 由于loss是当前batch的平均损失（每个样本1个损失，默认对batch取均值），
                # 但整个验证集损失需要加总所有样本的损失（再求总均值），
                # 所以要乘以当前batch的样本数inputs.size(0)
                val_loss += loss.item() * inputs.size(0)

                # 根据模型输出的logits取最大值的类别作为模型预测结果（按列argmax，适用于分类场景）
                predicted = torch.argmax(outputs, dim=1)

                # 统计该batch中预测正确的样本数
                # (predicted == targets) 得到布尔张量，sum()总计True的个数
                correct += (predicted == targets).sum().item()

                # 累加本batch的总样本数
                total += targets.size(0)

        avg_val_loss = val_loss / len(self.val_loader.dataset)  # 平均损失
        val_acc = correct / total if total > 0 else 0           # 平均准确率
        return avg_val_loss, val_acc

    def plot_curves(self):
        """
        绘制训练和验证过程中的损失与准确率变化曲线
        - 每1000步采样一次训练集损失和准确率
        - 验证集按sample_step/eval_step采样
        """
        import numpy as np

        sample_step = 1000  # 控制采样间隔，减少点数，画面更清晰

        # --- 采样训练集损失与准确率曲线 ---
        # 语法解释:
        # self.train_loss_history[::sample_step] 这是Python切片(slice)操作，形式为 list[start:stop:step]
        # - start: 起始索引（这里省略，默认为0，从头开始）
        # - stop: 终止索引（这里省略，默认为结尾，直到最后一个元素）
        # - step: 步长（这里为sample_step），表示每隔sample_step取一个元素
        # 作用：等价于 [self.train_loss_history[i] for i in range(0, len(self.train_loss_history), sample_step)]
        # 即把每sample_step间隔的损失值采样出来，生成一个新的列表train_loss_sampled
        train_loss_sampled = self.train_loss_history[::sample_step]        # 每sample_step采一个点
        train_acc_sampled = self.train_acc_history[::sample_step]
        # 生成一个等间隔的横坐标数组，表示采样出来的每个训练集点对应的step（步数/批次数）
        train_x_steps = np.arange(0, len(self.train_loss_history), sample_step)

        # --- 采样验证集损失与准确率曲线（按sample_step/eval_step间隔采样）---
        if hasattr(self, 'eval_step') and self.eval_step and self.eval_step > 0:
            val_sample_interval = max(1, sample_step // self.eval_step)
        else:
            val_sample_interval = 1  # eval_step无效时，每一个都采

        val_loss_sampled = self.val_loss_history[::val_sample_interval]
        val_acc_sampled = self.val_acc_history[::val_sample_interval]
        # 验证集X轴坐标对应的全局step
        # np.arange(start, stop, step)：生成一个从start到stop（不包括stop），步长为step的等差数组
        # - 这里start为0，stop为len(self.val_loss_history)*self.eval_step，step为self.eval_step
        #   生成的数组形如 [0, self.eval_step, 2*self.eval_step, ..., (n-1)*self.eval_step]，n为len(self.val_loss_history)
        # - [::val_sample_interval]：再次切片，每隔val_sample_interval取一个值，实现和val_loss_sampled一样的采样步长
        val_x_steps = np.arange(0, len(self.val_loss_history)*self.eval_step, self.eval_step)[::val_sample_interval]

        plt.figure(figsize=(12, 4))  # 画布大小

        # ------------------- 损失曲线 -------------------
        plt.subplot(1, 2, 1)
        plt.plot(train_x_steps, train_loss_sampled, label='Train Loss', marker='o')  # 训练损失
        if len(val_loss_sampled) > 0:
            plt.plot(val_x_steps, val_loss_sampled, label='Validation Loss', marker='x')  # 验证损失
        plt.xlabel('Batch')   # 横坐标为batch
        plt.ylabel('Loss')    # 纵坐标为损失
        plt.title('Loss Curves')  # 图标题
        plt.legend()
        plt.grid(True)        # 显示网格

        # ------------------- 准确率曲线 -------------------
        plt.subplot(1, 2, 2)
        plt.plot(train_x_steps, train_acc_sampled, label='Train Acc', marker='o')  # 训练准确率
        if len(val_acc_sampled) > 0:
            plt.plot(val_x_steps, val_acc_sampled, label='Validation Acc', marker='x')  # 验证准确率
        plt.xlabel('Batch')
        plt.ylabel('Accuracy')
        plt.title('Accuracy Curves')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()      # 自动调整子图间距
        plt.show()             # 展示图像
