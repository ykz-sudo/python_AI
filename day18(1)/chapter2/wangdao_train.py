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
        model_checkpoint=None,  # 新增参数：ModelCheckpoint对象
        tensorboard_callback=None,  # 新增参数：TensorBoardCallback对象
    # 你问到 __init__ 括号后面用“:”的作用，实际上这是python类或者函数定义语法的一部分：
    # 
    # def __init__(self, ...):  # <-- 注意这个冒号
    #     ...
    # 
    # 这个冒号是Python语法规定的（和for/if/while/class等也是同样道理），不是参数初始化的符号，只是说明定义体（代码块）开始。和C/C++/Java的大括号的作用类似。
    # 
    # 真正的“初始化”是依靠这个__init__方法内部对self.xxx赋值来实现的。
    # 
    ):
        """
        初始化Trainer类

        参数说明:
            model: 神经网络模型（需继承自torch.nn.Module）
            train_loader: 训练集DataLoader
            val_loader: 验证集DataLoader
            criterion: 损失函数
            optimizer: 优化器（如SGD/Adam等）
            device: 使用的设备（如 "cpu" 或 "cuda"）
            eval_step: 每训练多少个batch进行一次验证
            early_stopping: EarlyStopping对象，若为None则不使用早停
            early_stopping_kwargs: 早停参数的字典，若未传入early_stopping，可用此参数初始化
            model_checkpoint: ModelCheckpoint对象，控制模型保存策略
            tensorboard_callback: TensorBoardCallback对象，控制tensorboard日志记录
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.eval_step = eval_step

        self.model.to(self.device)  # 将模型放置在指定设备

        # 可选的回调功能
        # INSERT_YOUR_CODE
        # 回调功能（callback）指的是：在训练过程中，在程序的某些特定时刻（如每个batch、每次验证、每个epoch结束等）自动执行的用户自定义函数/对象或操作，用于在不修改主训练循环逻辑的前提下，实现如：
        # - 早停（EarlyStopping）：监控验证集表现，如果多轮未提升则自动终止训练。
        # - 模型保存（ModelCheckpoint）：自动保存性能最优或定期保存的模型权重文件。
        # - 日志记录（如TensorBoardCallback）：记录损失、准确率等曲线，用于可视化。
        # 
        # 回调的优势是能让训练过程更加灵活、可扩展，提升自动化与便利性，不需要频繁修改训练主代码结构。
        self.model_checkpoint = model_checkpoint  # 保存模型的回调
        self.tensorboard_callback = tensorboard_callback  # tensorboard日志回调

        # 历史记录，用于绘图和分析
        self.train_loss_history = []  # 训练损失（每batch）
        self.val_loss_history = []    # 验证损失（每eval_step）
        self.train_acc_history = []   # 训练准确率（每batch）
        self.val_acc_history = []     # 验证准确率（每eval_step）

        # 初始化早停机制
        if early_stopping is not None:
            self.early_stopping = early_stopping
        elif early_stopping_kwargs is not None:
            self.early_stopping = EarlyStopping(**early_stopping_kwargs)
        else:
            self.early_stopping = None

    def train(self, num_epochs):
        """
        标准分类训练过程

        参数:
            num_epochs (int): 训练的epoch数量
        """
        global_step = 0  # 全局步计数器，按batch累加
        stop_training = False  # 终止训练的标志

        for epoch in range(num_epochs):
            if stop_training:
                print(f"Early stopping triggered. Stopping at epoch {epoch}.")
                break  # 如果早停被触发，停止训练
            self.model.train()  # 训练模式
            train_loss = 0.0  # 本轮loss总和
            train_correct = 0  # 正确预测数量
            train_total = 0  # 总样本数
            
            for batch_idx, batch in enumerate(self.train_loader):
                # 获取数据
                # 假设batch为元组 (inputs, targets)
                # inputs: torch.Tensor, targets: torch.Tensor
                inputs, targets = batch
                inputs = inputs.to(self.device)  # 放到GPU/CPU
                targets = targets.to(self.device)

                # 梯度清零
                self.optimizer.zero_grad()
                # 前向传播
                # inputs: torch.Tensor, float32; targets: torch.Tensor, long
                outputs = self.model(inputs)  # outputs: torch.Tensor, float32
                # 计算损失
                loss = self.criterion(outputs, targets)  # loss: torch.Tensor, float32 (scalar)
                # 反向传播
                loss.backward()
                # 更新模型参数
                self.optimizer.step()

                # 当前batch损失和准确率
                # loss: torch.Tensor, float32 (scalar)
                batch_loss = loss.item()  # float
                # outputs: torch.Tensor (batch_size, num_classes), float32
                predicted = torch.argmax(outputs, dim=1)  # torch.Tensor, long, (batch_size,)
                # targets: torch.Tensor, long, (batch_size,)
                batch_correct = (predicted == targets).sum().item()  # int
                batch_total = targets.size(0)  # int
                batch_acc = batch_correct / batch_total if batch_total > 0 else 0  # float

                # 记录本batch的损失和准确率
                self.train_loss_history.append(batch_loss)
                self.train_acc_history.append(batch_acc)

                # 累计loss和acc统计
                train_loss += batch_loss * batch_total
                train_correct += batch_correct
                train_total += batch_total

                global_step += 1  # 全局步+1

                # 到达验证步时进行一次评估
                if self.eval_step is not None and self.eval_step > 0 and global_step % self.eval_step == 0:
                    val_loss, val_acc = self.evaluate_once()  # 验证集评估loss与准确率
                    self.val_loss_history.append(val_loss)
                    self.val_acc_history.append(val_acc)
                    print(f"[Step {global_step}] Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}")

                    # 模型保存判据
                    if self.model_checkpoint is not None:
                        # 根据monitor字段判断保存方式
                        if self.model_checkpoint.monitor == 'val_loss':
                            self.model_checkpoint(val_loss, self.model, epoch=epoch)
                        elif self.model_checkpoint.monitor == 'val_acc':
                            self.model_checkpoint(val_acc, self.model, epoch=epoch)
                        else:
                            self.model_checkpoint(val_loss, self.model, epoch=epoch)

                    # TensorBoard日志写入 (支持loss/acc/lr)
                    if self.tensorboard_callback is not None:
                        self.tensorboard_callback(
                            global_step,
                            loss=batch_loss,
                            val_loss=val_loss,
                            acc=batch_acc,
                            val_acc=val_acc,
                            lr=self.optimizer.param_groups[0]['lr'] if hasattr(self.optimizer, 'param_groups') else None,
                        )

                    # 早停判断（根据EarlyStopping的mode自动选择监控指标）
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
            # # 可选：epoch结束额外评估一次
            # val_loss, val_acc = self.evaluate_once()
            # self.val_loss_history.append(val_loss)
            # self.val_acc_history.append(val_acc)

            avg_train_loss = train_loss / len(self.train_loader.dataset)
            avg_train_acc = train_correct / train_total if train_total > 0 else 0
            print(f"Epoch [{epoch+1}/{num_epochs}]  Train Loss: {avg_train_loss:.4f}  Train Acc: {avg_train_acc:.4f}")

    def train_regression(self, num_epochs):
        """
        回归任务的训练过程（支持早停与模型保存），不涉及准确率

        参数:
            num_epochs (int): 训练轮数
        """
        import torch
        
        self.model.train()  # 设置为训练模式
        global_step = 0
        stop_training = False
        
        for epoch in range(num_epochs):
            train_loss = 0.0  # 累计本epoch的loss
            train_total = 0  # 累计样本总数
            
            for batch_idx, batch in enumerate(self.train_loader):
                inputs, targets = batch
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                
                # 前向与反向传播
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                loss.backward()
                self.optimizer.step()
                
                batch_loss = loss.item()
                train_loss += batch_loss * inputs.size(0)  # 归一化乘batch大小
                train_total += inputs.size(0)
                
                # 记录训练损失历史
                self.train_loss_history.append(batch_loss)
                
                global_step += 1
                
                # 到达验证步时评估
                if self.eval_step is not None and self.eval_step > 0 and global_step % self.eval_step == 0:
                    val_loss = self.evaluate_regression_once()
                    self.val_loss_history.append(val_loss)
                    print(f"[Step {global_step}] Val Loss: {val_loss:.4f}")
                    
                    # 模型保存（回归仅支持loss监控）
                    if self.model_checkpoint is not None:
                        self.model_checkpoint(val_loss, self.model, epoch=epoch)
                    
                    # TensorBoard记录loss和lr
                    if self.tensorboard_callback is not None:
                        self.tensorboard_callback.add_loss_scalars(
                            global_step, 
                            loss=batch_loss, 
                            val_loss=val_loss
                        )
                        if hasattr(self.optimizer, 'param_groups'):
                            self.tensorboard_callback.add_lr_scalars(
                                global_step, 
                                learning_rate=self.optimizer.param_groups[0]['lr']
                            )
                    
                    # 早停检测（始终基于val_loss）
                    if self.early_stopping is not None:
                        should_stop = self.early_stopping.step(val_loss)
                        if should_stop:
                            print(f"Early stopping triggered at step {global_step}.")
                            stop_training = True
                            break
            
            if stop_training:
                break
                
            avg_train_loss = train_loss / train_total if train_total > 0 else 0
            print(f"Epoch [{epoch+1}/{num_epochs}]  Train Loss: {avg_train_loss:.4f}")
    
    def evaluate_regression_once(self):
        """
        在整个验证集上评估当前回归模型的平均损失

        返回:
            avg_val_loss (float): 验证集平均损失
        """
        self.model.eval()  # 评估模式
        val_loss = 0.0
        total_samples = 0
        
        with torch.no_grad():
            for batch in self.val_loader:
                inputs, targets = batch
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                val_loss += loss.item() * inputs.size(0)
                total_samples += inputs.size(0)
        
        avg_val_loss = val_loss / total_samples if total_samples > 0 else 0
        return avg_val_loss

    def evaluate_once(self):
        """
        在整个验证集上评估损失和准确率（适用于分类）

        返回:
            avg_val_loss (float): 验证集平均损失
            val_acc (float): 验证集准确率
        """
        self.model.eval()  # 评估模式
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
                predicted = torch.argmax(outputs, dim=1)  # 分类预测
                correct += (predicted == targets).sum().item()  # 预测正确数
                total += targets.size(0)
        avg_val_loss = val_loss / len(self.val_loader.dataset)
        val_acc = correct / total if total > 0 else 0
        return avg_val_loss, val_acc

    def plot_curves(self, sample_step=1000):
        """
        绘制训练过程中的损失和准确率曲线。

        参数:
            sample_step (int): 每sample_step间隔采样一次曲线，用于平滑和减少点数

        说明:
            - 若包含准确率数据，将绘制损失和准确率两个子图
            - 若只有损失（如回归），仅绘制loss曲线
        """
        import numpy as np

        # --- 采样训练曲线 ---
        train_loss_sampled = self.train_loss_history[::sample_step]
        train_x_steps = np.arange(0, len(self.train_loss_history), sample_step)

        # --- 采样验证曲线 ---
        # 判断self是否包含eval_step属性，并且eval_step为正数
        # eval_step代表验证集（validation）采样的步长，用于确定验证曲线在x轴（batch）上的对齐关系
        if hasattr(self, 'eval_step') and self.eval_step and self.eval_step > 0:
            val_sample_interval = max(1, sample_step // self.eval_step)
        else:
            val_sample_interval = 1  # 如果eval_step不可用，备用为1

        val_loss_sampled = self.val_loss_history[::val_sample_interval]
        # 验证曲线x轴（乘上eval_step对齐batch坐标）
        # 详细解释：
        # val_x_steps用于绘制验证集的曲线，它决定了横坐标（x轴）的取值。
        # 由于val_loss_history的每一个数据点，都是在训练时隔self.eval_step个batch评估一次添加进去的，
        # 所以第i个验证点其实是（i*self.eval_step）个batch后得到的。
        # 因此，这里用np.arange(0, len(self.val_loss_history)*self.eval_step, self.eval_step)，
        # 生成从0到最后一个验证点的所有横坐标（按eval_step间隔），
        # 然后再根据val_sample_interval进行采样（下标步进）。
        val_x_steps = np.arange(
            0,
            len(self.val_loss_history) * self.eval_step,
            self.eval_step
        )[::val_sample_interval]

        # 检查是否有准确率信息
        has_acc_data = len(self.train_acc_history) > 0

        if has_acc_data:
            # 有准确率时绘制两个子图
            train_acc_sampled = self.train_acc_history[::sample_step]
            val_acc_sampled = self.val_acc_history[::val_sample_interval]
            
            plt.figure(figsize=(12, 4))  # 画布大小

            # ----- 损失子图 -----
            plt.subplot(1, 2, 1)
            plt.plot(train_x_steps, train_loss_sampled, label='Train Loss', marker='o')
            if len(val_loss_sampled) > 0:
                plt.plot(val_x_steps, val_loss_sampled, label='Validation Loss', marker='x')
            plt.xlabel('Batch')  # 横坐标
            plt.ylabel('Loss')   # 纵坐标
            plt.title('Loss Curves')
            plt.legend()
            plt.grid(True)

            # ----- 准确率子图 -----
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
        else:
            # 仅有损失信息时
            plt.figure(figsize=(8, 4))  # 画布

            plt.plot(train_x_steps, train_loss_sampled, label='Train Loss', marker='o')
            if len(val_loss_sampled) > 0:
                plt.plot(val_x_steps, val_loss_sampled, label='Validation Loss', marker='x')
            plt.xlabel('Batch')
            plt.ylabel('Loss')
            plt.title('Loss Curves')
            plt.legend()
            plt.grid(True)

            plt.tight_layout()

        plt.show()


# INSERT_YOUR_CODE
class EarlyStopping:
    """
    提前停止训练（Early Stopping）机制类:
    在验证集的指标（如loss/acc）在若干patience轮内未提升则中止训练。
    """

    def __init__(self, patience=5, min_delta=0.01, mode='min'):
        """
        初始化EarlyStopping。

        参数:
            patience (int): 容忍的epoch数，若超出且监控指标仍未提升则停止训练
            min_delta (float): 最小提升量，只有提升超过该值才视为改进
            mode (str): 'min' 监控指标越小越好，如loss；'max'越大越好，如acc
        """
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.best_score = None     # 最优监控指标（初始化为空）
        self.counter = 0           # 未提升轮数计数器
        self.early_stop = False    # 是否应提前停止

        if self.mode not in ['min', 'max']:
            raise ValueError("mode只能是'min'或'max'")

        if self.mode == 'min':
            self.monitor_op = lambda curr, best: curr < best - self.min_delta  # 越小越好
        else:
            self.monitor_op = lambda curr, best: curr > best + self.min_delta  # 越大越好

    def step(self, current):
        """
        检查是否应提前停止。

        参数:
            current (float): 当前epoch的监控指标（如val_loss或val_acc）

        返回:
            bool: 是否应提前停止（True为应终止）
        """
        if self.best_score is None:
            # 初始化阶段，记录首个指标
            self.best_score = current
            self.counter = 0
            self.early_stop = False
            return False

        if self.monitor_op(current, self.best_score):
            # 指标有提升，更新最优
            self.best_score = current
            self.counter = 0
            self.early_stop = False
        else:
            # 未提升，计数累加
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True  # 触发早停
        return self.early_stop

    def reset(self):
        """
        重置early stopping状态
        """
        self.best_score = None
        self.counter = 0
        self.early_stop = False

     
class ModelCheckpoint:
    """
    模型权重保存回调类, 可自动判断并保存性能最优的模型
    """
    def __init__(self, filepath, monitor='val_loss', save_best_only=True, mode='min', min_delta=0.01):
        """
        初始化ModelCheckpoint

        参数:
            filepath (str): 保存模型的文件路径，支持占位符，如'model_epoch{epoch}_val_loss{val_loss:.4f}.pt'
            monitor (str): 监控的指标名称，仅用于信息记录
            save_best_only (bool): 是否只存性能最佳的模型
            mode (str): 'min'表示指标越小越好（如loss），'max'反之
            min_delta (float): 指标提升的最小变化幅度
        """
        self.filepath = filepath
        self.monitor = monitor
        self.save_best_only = save_best_only
        self.mode = mode
        self.min_delta = min_delta
        self.best_score = None

        if mode not in ['min', 'max']:
            raise ValueError("mode只能是'min'或者'max'")

        # 详细解释:
        # 下面根据mode决定监控指标的提升判据和最优值初始值。
        # - 若mode为'min'（如监控val_loss），我们希望数值越小越好，因此：
        #   - monitor_op定义为：当前值curr小于best减去min_delta时视为提升（即显著更好）。
        #   - best_score初始设为正无穷，保证第一次能保存（任何数都会更小）。
        # - 若mode为'max'（如监控val_acc），数值越大越好，因此：
        #   - monitor_op定义为：当前值curr大于best加上min_delta时视为提升。
        #   - best_score初始设为负无穷，保证第一次能保存（任何数都会更大）。
        if self.mode == 'min':
            self.monitor_op = lambda curr, best: curr < best - self.min_delta
            self.best_score = float('inf')  # 监控最小值，初始极大
        else:
            self.monitor_op = lambda curr, best: curr > best + self.min_delta
            self.best_score = -float('inf')  # 监控最大值，初始极小

    def __call__(self, current, model, epoch=None):
        """
        执行模型保存

        参数:
            current (float): 当前监控指标
            model: 需保存的模型（需有.state_dict()）
            epoch: 当前epoch（可用于命名）
        返回:
            bool: 若执行了保存返回True，否则返回False
        """
        import os
        if self.save_best_only:
            # 只存性能最佳的
            # 详细解释：
            # 1. 首先判断当前的监控指标current，是否相较于best_score有“显著提升”（即满足monitor_op函数）。这根据mode的不同，可能是比最优值降低了min_delta（如loss），或增长了min_delta（如accuracy）。
            # 2. 如果有提升，则需要保存当前模型：
            #    - 先取出目标文件夹路径，如果文件夹不存在自动创建，避免因路径不存在报错。
            #    - 更新best_score为当前更优的监控值。
            #    - 使用filepath的format方法生成保存文件名（epoch此处默认为'best'，也可根据需要自定义）。
            #    - 调用内部_save_model方法将模型保存到指定位置。
            #    - 返回True，表示本次执行确实发生了模型保存。
            # 3. 如果没有达到最优，则不保存，直接返回False。
            if self.monitor_op(current, self.best_score):
                # 取得目标文件夹路径（如./model_dir/）
                filepath_dir = os.path.dirname(self.filepath)
                os.makedirs(filepath_dir, exist_ok=True)

                # 更新为当前最佳监控值
                self.best_score = current

                # 文件名格式化。此处epoch='best'可用于标识当前最优（当然也可以传入real epoch号）
                file_name = self.filepath.format(epoch='best')

                # 执行模型保存
                self._save_model(model, file_name)

                return True  # 明确发生了保存
            return False      # 未保存
        else:
            # 每次都保存，每次根据指标/epoch重命名
            if epoch is not None:
                filepath = self.filepath.format(epoch=epoch, **{self.monitor: current})
            else:
                filepath = self.filepath.format(**{self.monitor: current})
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            self._save_model(model, filepath)
            return True

    def _save_model(self, model, filepath):
        """
        保存torch模型到指定路径

        参数:
            model: nn.Module
            filepath (str): 存储路径
        """
        try:
            import torch
            torch.save(model.state_dict(), filepath)
        except ImportError:
            raise RuntimeError("需要torch库用于保存模型")

from torch.utils.tensorboard import SummaryWriter


class TensorBoardCallback:
    """
    TensorBoard工具回调类
    实现loss、accuracy、learning_rate等标量自动写入
    """
    def __init__(self, log_dir, flush_secs=10):
        """
        初始化

        参数:
            log_dir (str): tensorboard日志根目录
            flush_secs (int): 写磁盘的时间间隔（秒）
        """
        self.writer = SummaryWriter(log_dir=log_dir, flush_secs=flush_secs)

    def draw_model(self, model, input_shape):
        """
        写入模型图到tensorboard

        参数:
            model: torch模型
            input_shape: 随机输入张量shape
        """
        self.writer.add_graph(model, input_to_model=torch.randn(input_shape))
        
    def add_loss_scalars(self, step, loss, val_loss):
        """
        向tensorboard写入loss曲线

        参数:
            step: 步数
            loss: 训练损失
            val_loss: 验证损失
        """
        self.writer.add_scalars(
            main_tag="training/loss", 
            tag_scalar_dict={"loss": loss, "val_loss": val_loss},
            global_step=step,
        )
        
    def add_acc_scalars(self, step, acc, val_acc):
        """
        向tensorboard写入accuracy曲线

        参数:
            step: 步数
            acc: 训练准确率
            val_acc: 验证准确率
        """
        self.writer.add_scalars(
            main_tag="training/accuracy",
            tag_scalar_dict={"accuracy": acc, "val_accuracy": val_acc},
            global_step=step,
        )
        
    def add_lr_scalars(self, step, learning_rate):
        """
        向tensorboard写入学习率曲线

        参数:
            step: 步数
            learning_rate: 当前学习率
        """
        self.writer.add_scalars(
            main_tag="training/learning_rate",
            tag_scalar_dict={"learning_rate": learning_rate},
            global_step=step,
        )
    
    def __call__(self, step, **kwargs):
        """
        支持一次性自动写入loss/acc/lr
        收到的kwargs支持：loss/val_loss, acc/val_acc, lr(learning_rate)
        """
        # 若有loss/val_loss
        loss = kwargs.pop("loss", None)
        val_loss = kwargs.pop("val_loss", None)
        if loss is not None and val_loss is not None:
            self.add_loss_scalars(step, loss, val_loss)
        # 若有acc/val_acc
        acc = kwargs.pop("acc", None)
        val_acc = kwargs.pop("val_acc", None)
        if acc is not None and val_acc is not None:
            self.add_acc_scalars(step, acc, val_acc)
        # 若有学习率
        learning_rate = kwargs.pop("lr", None)
        if learning_rate is not None:
            self.add_lr_scalars(step, learning_rate)
