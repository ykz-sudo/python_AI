import torch
import matplotlib.pyplot as plt

class Trainer:
    def __init__(
        self,
        model,
        train_loader,
        val_loader,
        criterion,
        optimizer,
        device,
        eval_step=100,
        early_stopping=None,
        early_stopping_kwargs=None,
    ):
        """
        model: 神经网络模型
        train_loader: 训练集的DataLoader
        val_loader: 验证集的DataLoader
        criterion: 损失函数
        optimizer: 优化器
        device: 设备 (如 "cpu" 或 "cuda")
        eval_step: 训练过程中多少个batch后验证一次
        early_stopping: EarlyStopping对象 或 None 禁用早停
        early_stopping_kwargs: 如果不传early_stopping对象，可以传此参数作为EarlyStopping的参数(dict)
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.eval_step = eval_step

        self.model.to(self.device)

        # 用于绘图的损失和准确率历史记录（按batch记）
        self.train_loss_history = []
        self.val_loss_history = []
        self.train_acc_history = []
        self.val_acc_history = []

        # early stopping
        if early_stopping is not None:
            self.early_stopping = early_stopping
        elif early_stopping_kwargs is not None:
            self.early_stopping = EarlyStopping(**early_stopping_kwargs)
        else:
            self.early_stopping = None

    def train(self, num_epochs):
        global_step = 0
        stop_training = False
        for epoch in range(num_epochs):
            if stop_training:
                print(f"Early stopping triggered. Stopping at epoch {epoch}.")
                break
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            for batch_idx, batch in enumerate(self.train_loader):
                inputs, targets = batch
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                loss.backward()
                self.optimizer.step()

                # 当前batch损失和准确率
                batch_loss = loss.item()
                predicted = torch.argmax(outputs, dim=1)
                batch_correct = (predicted == targets).sum().item()
                batch_total = targets.size(0)
                batch_acc = batch_correct / batch_total if batch_total > 0 else 0

                # 记录本batch的损失和准确率
                self.train_loss_history.append(batch_loss)
                self.train_acc_history.append(batch_acc)

                train_loss += batch_loss * batch_total
                train_correct += batch_correct
                train_total += batch_total

                global_step += 1

                # eval_step的整数倍时进行一次验证集计算
                if self.eval_step is not None and self.eval_step > 0 and global_step % self.eval_step == 0:
                    val_loss, val_acc = self.evaluate_once()
                    self.val_loss_history.append(val_loss)
                    self.val_acc_history.append(val_acc)
                    print(f"[Step {global_step}] Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}")

                    # early stopping 检查，默认监控val_loss
                    if self.early_stopping is not None:
                        if self.early_stopping.mode == 'min':
                            should_stop = self.early_stopping.step(val_loss)
                        else:
                            should_stop = self.early_stopping.step(val_acc)
                        if should_stop:
                            print(f"Early stopping triggered at step {global_step}.")
                            stop_training = True
                            break

            if stop_training:
                break
            # 可以在一个epoch末尾也再次eval一次（可选）
            # val_loss, val_acc = self.evaluate_once()
            # self.val_loss_history.append(val_loss)
            # self.val_acc_history.append(val_acc)

            avg_train_loss = train_loss / len(self.train_loader.dataset)
            avg_train_acc = train_correct / train_total if train_total > 0 else 0
            print(f"Epoch [{epoch+1}/{num_epochs}]  Train Loss: {avg_train_loss:.4f}  Train Acc: {avg_train_acc:.4f}")


    def evaluate_once(self):
        """评估整个val_loader的损失和准确率"""
        self.model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in self.val_loader:
                inputs, targets = batch
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)

                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                val_loss += loss.item() * inputs.size(0)
                predicted = torch.argmax(outputs, dim=1)
                correct += (predicted == targets).sum().item()
                total += targets.size(0)
        avg_val_loss = val_loss / len(self.val_loader.dataset)
        val_acc = correct / total if total > 0 else 0
        return avg_val_loss, val_acc

    def plot_curves(self):
        """
        每1000步采样一次训练集loss/acc进行绘图，验证集采用每sample_step/eval_step采样绘图。
        """
        import numpy as np

        sample_step = 1000  # 采样间隔

        # 采样训练曲线
        train_loss_sampled = self.train_loss_history[::sample_step]
        train_acc_sampled = self.train_acc_history[::sample_step]
        train_x_steps = np.arange(0, len(self.train_loss_history), sample_step)

        # 采样验证曲线（每sample_step/eval_step拿一个点）
        if hasattr(self, 'eval_step') and self.eval_step and self.eval_step > 0:
            val_sample_interval = max(1, sample_step // self.eval_step)
        else:
            val_sample_interval = 1  # fallback

        val_loss_sampled = self.val_loss_history[::val_sample_interval]
        val_acc_sampled = self.val_acc_history[::val_sample_interval]
        # 验证集点的x坐标（每eval_step加一个，采样后同样间隔拉伸）
        val_x_steps = np.arange(0, len(self.val_loss_history)*self.eval_step, self.eval_step)[::val_sample_interval]

        plt.figure(figsize=(12, 4))  # 画布

        # ------------------- 损失曲线 -------------------
        plt.subplot(1, 2, 1)
        plt.plot(train_x_steps, train_loss_sampled, label='Train Loss', marker='o')
        if len(val_loss_sampled) > 0:
            plt.plot(val_x_steps, val_loss_sampled, label='Validation Loss', marker='x')
        plt.xlabel('Batch')
        plt.ylabel('Loss')
        plt.title('Loss Curves')
        plt.legend()
        plt.grid(True)

        # ------------------- 准确率曲线 -------------------
        plt.subplot(1, 2, 2)
        plt.plot(train_x_steps, train_acc_sampled, label='Train Acc', marker='o')
        if len(val_acc_sampled) > 0:
            plt.plot(val_x_steps, val_acc_sampled, label='Validation Acc', marker='x')
        plt.xlabel('Batch')
        plt.ylabel('Accuracy')
        plt.title('Accuracy Curves')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()


# INSERT_YOUR_CODE
class EarlyStopping:
    """
    提前停止训练（Early Stopping）：
    在验证集损失在设定patience轮内没有提升，则提前终止训练。
    """

    def __init__(self, patience=5, min_delta=0.01, mode='min'):
        """
        参数:
        patience (int): 容忍的epoch数，如果在patience个epoch内指标未提升，则停止训练
        min_delta (float): 指标提升的最小变化量，只有大于这个才认为有提升
        mode (str): 'min' 表示希望监控指标越小越好（如loss），'max' 表示指标越大越好（如accuracy）
        """
        self.patience = patience           # 容忍多少个epoch未提升指标才停止（耐心值）
        self.min_delta = min_delta         # 指标提升的判定阈值，提升要大于该值才认为有效
        self.mode = mode                   # 选择监控指标是希望最小化('min')还是最大化('max')
        self.best_score = None             # 用于记录监控指标的最佳历史值
        self.counter = 0                   # 连续多少次没有指标提升
        self.early_stop = False            # 是否满足提前停止的条件（True: 训练应该停止）

        if self.mode not in ['min', 'max']:
            raise ValueError("mode只能是'min'或'max'")

        # 根据mode参数决定监控目标是希望越小越好（'min'，如loss）还是越大越好（'max'，如accuracy）
        if self.mode == 'min':
            # 如果mode是'min'，则定义一个用于比较的函数monitor_op。
            # 该函数接收当前指标curr和历史最佳指标best。
            # 只有当当前指标curr相比历史最佳指标best下降了超过min_delta阈值时，才认为指标有实质提升
            # 换句话说：只有curr < best - min_delta时，才判定有“提升”。
            # 适用于如val_loss这种越低越好的情况，只有明显变小才算进步。
            
            # monitor_op是一个匿名函数(lambda)，用于判断指标是否显著提升
            # 语法: lambda curr, best: curr < best - self.min_delta
            # - curr: 当前epoch的监控指标值(如最新的val_loss)
            # - best: 历史最佳指标值
            # 返回值: 如果curr比best小，且小于self.min_delta（即“显著提升”），返回True，否则返回False
            # 例：best=0.8, min_delta=0.01，只有curr < 0.79时才认定有提升
            self.monitor_op = lambda curr, best: curr < best - self.min_delta
        else:
            # 如果mode是'max'，则定义monitor_op为
            # 当前指标curr相比历史最佳指标best提升了超过min_delta阈值时，才算有提升。
            # 即只有curr > best + min_delta时，才确定指标提升
            # 适用于如val_acc这种越高越好，且提升必须超过指定幅度才算有效的场景
            self.monitor_op = lambda curr, best: curr > best + self.min_delta

    def step(self, current):
        """
        应在每次验证后调用step()方法，传入当前的验证集监控指标（如val_loss或者val_acc）。
        返回True，如果训练应提前停止；否则返回False。
        """
        if self.best_score is None:
            self.best_score = current #记录最佳指标
            self.counter = 0 #重置计数器
            self.early_stop = False
            return False

        if self.monitor_op(current, self.best_score): #监控指标小于最佳指标,val_loss越小越好
            self.best_score = current #记录最佳指标
            self.counter = 0 #重置计数器
            self.early_stop = False
        else:
            self.counter += 1 #计数器加1
            if self.counter >= self.patience:
                self.early_stop = True #训练应提前停止  
        return self.early_stop

    def reset(self):
        """重置early stopping状态"""
        self.best_score = None
        self.counter = 0
        self.early_stop = False

     
class ModelCheckpoint:
    def __init__(self, filepath, monitor='val_loss', save_best_only=True, mode='min', min_delta=0.01):
        """
        参数:
        filepath (str): 保存模型的文件路径，可以包含格式化字符串，如 'model_epoch{epoch}_val_loss{val_loss:.4f}.pt'
        monitor (str): 监控的指标名称，仅用于信息记录
        save_best_only (bool): 是否只保存性能最优的模型
        mode (str): 'min' 或 'max'，确定“更好”是数值更小或更大
        min_delta (float): 指标提升的最小变化量
        """
        self.filepath = filepath
        self.monitor = monitor
        self.save_best_only = save_best_only
        self.mode = mode
        self.min_delta = min_delta
        self.best_score = None

        if mode not in ['min', 'max']:
            raise ValueError("mode只能是'min'或者'max'")

        if self.mode == 'min':
            self.monitor_op = lambda curr, best: curr < best - self.min_delta
            self.best_score = float('inf')
        else:
            self.monitor_op = lambda curr, best: curr > best + self.min_delta
            self.best_score = -float('inf')

    # __call__的作用是让实例可以像函数一样被调用，用于执行模型保存的判断与保存逻辑。
    # 用法说明：
    # 1. checkpoint = ModelCheckpoint(...)     # 实例化一个保存器
    # 2. checkpoint(val_loss, model, epoch=i)  # 在训练中像函数一样调用，根据指标自动决定是否/如何保存模型
    # 3. 也可以只传必需值，如：checkpoint(val_acc, model)
    
    # __call__的常见场景和用途举例：
    # 1. PyTorch模块，如神经网络层(如nn.Module)。调用layer(x)，实际上执行了layer.__call__(x)，用于前向传播。
    # 2. 回调/Hook类，例如EarlyStopping、ModelCheckpoint等训练过程中的回调。像函数一样用对象，便于记录状态和传参。
    # 3. sklearn中的transformer、estimator对象，可以直接obj(x)处理数据。
    # 4. 函数对象（functor/functor pattern）：用来封装可带状态的函数，例如用于自定义排序、分组、过滤等。
    # 5. TensorFlow/Keras自定义层、损失函数或调度器（如学习率调度器）。
    # 6. 装饰器实现：某些简单装饰器直接用__call__实现包装，@装饰时返回一个__call__对象。
    # 7. Python一些标准库对象（如re.compile(pattern).match），正则对象就是可调用的。
    # 8. 用于配置型对象，如参数化的采样、生成器、闭包等，高阶自定义控制逻辑时
    def __call__(self, current, model, epoch=None):
        """
        current: 当前验证集监控指标（如val_loss或val_acc）
        model: 要保存的模型（必须有.state_dict()方法）
        epoch: 当前epoch编号（可选，用于文件命名）
        """
        import os
        # 保存模型
        if self.save_best_only:
            if self.monitor_op(current, self.best_score):
                self.best_score = current
                # 保存
                self._save_model(model, 'best.ckpt')
                return True  # 有保存
            return False  # 无保存
        else:
            # 每次都保存
            # 判断是否提供了epoch参数。如果有，就将epoch作为格式化字符串参数传入filepath，否则只传val_loss/val_acc或其他monitor键。
            # 格式化字符串语法: 
            #  - self.filepath.format(epoch=epoch, **{self.monitor: current}) 
            #    意思是将文件路径中的{epoch}和如{val_loss:.4f}等字段用实际值替换。
            #    **{self.monitor: current} 是构建一个字典，比如 monitor='val_loss'，current=0.1234, 则为{'val_loss': 0.1234}。
            if epoch is not None:
                # epoch不为None时，将epoch和监控指标(如val_loss)同时带入路径格式化。
                filepath = self.filepath.format(epoch=epoch, **{self.monitor: current})
            else:
                # 只提供监控指标做格式化参数，比如filepath="ckpt_{val_loss:.4f}.pt"。
                filepath = self.filepath.format(**{self.monitor: current})
            # os.makedirs(os.path.dirname(filepath), exist_ok=True) 作用是确保保存目录存在，不存在就自动创建。
            # os.path.dirname(filepath)返回文件路径的目录部分，exist_ok=True让已存在也不会报错。
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            # 调用保存函数
            self._save_model(model, filepath)
            return True

    def _save_model(self, model, filepath):
        """保存模型，假设是PyTorch模型"""
        # 只实现通用保存接口，具体框架层可根据需求调整
        try:
            import torch
            torch.save(model.state_dict(), filepath)
        except ImportError:
            raise RuntimeError("需要torch库用于保存模型")
