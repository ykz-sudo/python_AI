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
        model_checkpoint: ModelCheckpoint对象，用于保存模型，默认为None
        tensorboard_callback: TensorBoardCallback对象，用于写入Tensorboard，默认为None
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.eval_step = eval_step
        self.model.to(self.device)

        # 新增: ModelCheckpoint和TensorBoardCallback
        self.model_checkpoint = model_checkpoint
        self.tensorboard_callback = tensorboard_callback

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
            epoch_val_loss = None
            epoch_val_acc = None
            
            for batch in self.train_loader:
                self.model.train()
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
                # 通过torch.argmax获取输出中最大概率的类别索引，作为模型对每个样本的预测标签。
                # 例如，对于分类任务，outputs为(batch_size, num_classes)，
                # argmax(dim=1)会返回每个样本预测的类别（下标）。
                predicted = torch.argmax(outputs, dim=1)
                # 计算当前batch的准确预测数量和总数
                # batch_correct为本batch中预测正确的样本数，batch_total为样本总数
                # batch_acc为当前batch的准确率，等于batch_correct / batch_total
                # 下面代码的作用是计算当前batch中模型预测正确的样本数量。
                # (predicted == targets) 会按元素返回True/False的布尔张量，表示预测值与真实值是否相等。
                # .sum() 会将True计为1，False计为0，得到预测正确样本的总数（是个torch张量）。
                # .item() 把这个数值从单元素张量转换为Python的数字类型，方便后续计算和打印。
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
                    epoch_val_loss = val_loss
                    epoch_val_acc = val_acc
                    self.val_loss_history.append(val_loss)
                    self.val_acc_history.append(val_acc)
                    print(f"[Step {global_step}] Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}")

                    # --- 新增TensorBoard写入 ---
                    if self.tensorboard_callback is not None:
                        # 这里支持记录loss/acc
                        self.tensorboard_callback(
                            global_step,
                            loss=batch_loss,
                            val_loss=val_loss,
                            acc=batch_acc,
                            val_acc=val_acc,
                            # lr参数用于记录当前优化器的学习率（learning rate）。
                            # 这行的作用是：如果优化器有param_groups这个属性（如大多数PyTorch优化器都有），
                            # 就从第一个参数组取出其'lr'值作为学习率；否则返回None。
                            # learning rate决定了每次参数更新的步长，是训练过程中的重要超参数。
                            # 这是Python函数调用的关键字参数语法（keyword arguments）。
                            # 在这里，tensorboard_callback被调用并传入了多个参数，每个参数都是以key=value的形式出现，
                            # 意味着这些值会被作为带名字的参数传递到tensorboard_callback回调函数。
                            # 这种写法的优点是可读性强，不容易搞错位置参数的顺序，也可以只传自己关心的参数名及其值。
                            # 例如：loss=batch_loss 表示把batch_loss这个变量的值赋给名为loss的参数。
                            # 这些参数的含义如下：
                            #   global_step: 全局第几步，用于X轴标尺。
                            #   loss: 当前batch损失。
                            #   val_loss: 当前验证集损失。
                            #   acc: 当前batch准确率。
                            #   val_acc: 当前验证集准确率。
                            #   lr: 当前学习率。其写法意为：
                            #       self.optimizer.param_groups是优化器的参数组列表（PyTorch标准用法），
                            #       [0]['lr']表示取第一个参数组里的'lr'（学习率）参数。
                            #       如果优化器没有param_groups属性，则返回None。
                            lr=self.optimizer.param_groups[0]['lr'] if hasattr(self.optimizer, 'param_groups') else None,
                        )

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


            # 每个epoch结束后保存模型
            if self.model_checkpoint is not None and epoch_val_loss is not None:
                # monitor参数判据: ModelCheckpoint 设置为监控val_loss(val_acc)
                if self.model_checkpoint.monitor == 'val_loss':
                    self.model_checkpoint(epoch_val_loss, self.model, epoch=epoch)
                elif self.model_checkpoint.monitor == 'val_acc':
                    self.model_checkpoint(epoch_val_acc, self.model, epoch=epoch)
                else:  # 默认用val_loss
                    self.model_checkpoint(epoch_val_loss, self.model, epoch=epoch)
            
            if stop_training:
                break

            # 可以在一个epoch末尾也再次eval一次（可选）
            # val_loss, val_acc = self.evaluate_once()
            # self.val_loss_history.append(val_loss)
            # self.val_acc_history.append(val_acc)

            avg_train_loss = train_loss / len(self.train_loader.dataset)
            avg_train_acc = train_correct / train_total if train_total > 0 else 0
            print(f"Epoch [{epoch+1}/{num_epochs}]  Train Loss: {avg_train_loss:.4f}  Train Acc: {avg_train_acc:.4f}")

    def train_regression(self, num_epochs):
        """
        回归训练函数，包含早停和模型保存功能
        """
        import torch
        
        self.model.train()
        global_step = 0
        stop_training = False
        
        for epoch in range(num_epochs):
            train_loss = 0.0
            train_total = 0
            epoch_val_loss = None
            
            for batch_idx, batch in enumerate(self.train_loader):
                inputs, targets = batch
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                
                # 前向传播
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                
                # 反向传播
                loss.backward()
                self.optimizer.step()
                
                batch_loss = loss.item()
                train_loss += batch_loss * inputs.size(0)
                train_total += inputs.size(0)
                
                # 记录训练损失历史
                self.train_loss_history.append(batch_loss)
                
                global_step += 1
                
                # 定期评估
                if self.eval_step is not None and self.eval_step > 0 and global_step % self.eval_step == 0:
                    val_loss = self.evaluate_regression_once()
                    epoch_val_loss = val_loss
                    self.val_loss_history.append(val_loss)
                    print(f"[Step {global_step}] Val Loss: {val_loss:.4f}")
                    
                    # TensorBoard记录
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
                    
                    # 早停检查（基于val_loss）
                    if self.early_stopping is not None:
                        should_stop = self.early_stopping.step(val_loss)
                        if should_stop:
                            print(f"Early stopping triggered at step {global_step}.")
                            stop_training = True
                            break
            
            if stop_training:
                break
            
            # 每个epoch结束后保存模型
            if self.model_checkpoint is not None and epoch_val_loss is not None:
                self.model_checkpoint(epoch_val_loss, self.model, epoch=epoch)
                
            avg_train_loss = train_loss / train_total if train_total > 0 else 0
            print(f"Epoch [{epoch+1}/{num_epochs}]  Train Loss: {avg_train_loss:.4f}")
    
    def evaluate_regression_once(self):
        """评估回归模型的损失"""
        self.model.eval()
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

    def train_binary(self, num_epochs):
        """
        针对二分类任务的训练过程，适用于单神经元（最后一层输出一个logits）+ BCEWithLogitsLoss 作为损失函数。
        每经过eval_step步，会在验证集进行一次评估：输出验证损失和准确率。

        详细说明：
        - Binary Cross Entropy with Logits Loss (BCEWithLogitsLoss) 是二分类场景下常用的损失函数。
        - BCEWithLogitsLoss与普通的二分类交叉熵（BCELoss）不同之处在于，BCEWithLogitsLoss将“sigmoid归一化激活函数”和“二元交叉熵损失”合为一步，直接对神经网络的logits输出计算损失，具有数值稳定性更好、精度更高的优势。
        - 而普通的交叉熵（如nn.CrossEntropyLoss）通常用在多分类问题，输入必须是未归一化的logits，标签为类别索引(0, 1, ..., n_classes-1)。
        - BCELoss常用于二分类，需输入sigmoid归一化后的概率值，标签同样为0或1，而BCEWithLogitsLoss则直接输入logits，自动内部进行sigmoid操作。

        Args:
            num_epochs (int): 训练轮数
        """
        # 全局步数计数器
        global_step = 0
        for epoch in range(num_epochs):
            self.model.train()  # 进入训练模式
            train_loss = 0.0    # 累计训练损失
            train_correct = 0   # 累计训练准确样本数
            train_total = 0     # 累计总训练样本数

            # 遍历整个训练集
            for batch in self.train_loader:
                inputs, targets = batch
                inputs = inputs.to(self.device)
                # BCEWithLogitsLoss 需要float型的targets，并reshape为 (batch_size, 1)
                targets = targets.float().to(self.device).view(-1, 1)

                self.optimizer.zero_grad()  # 梯度归零
                outputs = self.model(inputs)  # 前向传播，获得logits
                
                # 计算BCEWithLogitsLoss损失
                loss = self.criterion(outputs, targets)
                loss.backward()        # 反向传播
                self.optimizer.step()  # 参数更新

                # 累计损失（要乘batch_size）
                train_loss += loss.item() * inputs.size(0)
                # sigmoid后的概率>=0时对应概率>=0.5，所以直接用logits>=0作为分类输出
                preds = outputs >= 0
                # 比较预测与标签获得当前batch准确样本数
                # .cpu() 的原因：确保张量是在CPU上进行比较和sum，否则如果它们在GPU上而没有被移到CPU，某些情况下（比如在需要从GPU转回CPU做进一步处理，或是在某些只有CPU支持的操作时）会报错或导致不可预期行为。
                # 下面的写法可以保留这种安全性
                train_correct += (preds.cpu() == targets.cpu()).sum().item()
                train_total += targets.size(0)

                # 可以记录loss和acc的历史变化（用于画图等分析）
                if hasattr(self, "train_loss_history"):
                    self.train_loss_history.append(loss.item())
                if hasattr(self, "train_acc_history"):
                    acc_this_batch = (preds.cpu() == targets.cpu()).float().mean().item()
                    self.train_acc_history.append(acc_this_batch)

                global_step += 1

                # 每隔eval_step步进行一次验证集评估
                if hasattr(self, 'eval_step') and self.eval_step is not None and self.eval_step > 0:
                    if global_step % self.eval_step == 0:
                        val_loss, val_acc = self.evaluate_binary_once()
                        if hasattr(self, "val_loss_history"):
                            self.val_loss_history.append(val_loss)
                        if hasattr(self, "val_acc_history"):
                            self.val_acc_history.append(val_acc)
                        print(f"[Step {global_step}] Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}")

            # 每个epoch统计平均损失与准确率
            avg_train_loss = train_loss / train_total if train_total > 0 else 0
            train_acc = train_correct / train_total if train_total > 0 else 0
            
            # 每个epoch结束后，如有需要，保存模型
            if self.model_checkpoint is not None and val_loss is not None:
                self.model_checkpoint(val_loss, self.model, epoch=epoch)
        

            print(f"Epoch [{epoch+1}/{num_epochs}] Train Loss: {avg_train_loss:.4f} Acc: {train_acc:.4f} | Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}")

    def evaluate_binary_once(self):
        """二分类评估过程，返回平均损失和准确率"""
        self.model.eval()
        val_loss = 0.0
        val_correct = 0
        total = 0

        with torch.no_grad():
            for batch in self.val_loader:
                inputs, targets = batch
                inputs = inputs.to(self.device)
                targets = targets.float().to(self.device).view(-1, 1)

                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                val_loss += loss.item() * inputs.size(0)
                preds = outputs >= 0
                val_correct += (preds.cpu() == targets.cpu()).sum().item()
                total += targets.size(0)

        avg_val_loss = val_loss / total if total > 0 else 0
        val_acc = val_correct / total if total > 0 else 0
        self.model.train()
        return avg_val_loss, val_acc
        
    def plot_curves(self, sample_step=1000):
        """
        绘制训练过程中损失（loss）和准确率（accuracy）随迭代步数变化的曲线。
        支持训练集/验证集的loss和acc曲线，并进行步长采样。
        如果self.train_acc_history为空，则只画损失曲线。

        Args:
            sample_step (int): 采样间隔步数。每隔多少步取一个点绘图，避免曲线太密集。
        """
        import numpy as np

        # 采样训练集损失曲线，隔sample_step采样一个点
        train_loss_sampled = self.train_loss_history[::sample_step]
        # 构造训练集loss的横坐标步数序列（采样后对应的batch号）
        train_x_steps = np.arange(0, len(self.train_loss_history), sample_step)

        # 验证集采样间隔：每(val_sample_interval)步采样一次
        # 默认每sample_step//eval_step采样一次val_loss，如果eval_step为0或属性不存在，则全部采样
        if hasattr(self, 'eval_step') and self.eval_step and self.eval_step > 0:
            val_sample_interval = max(1, sample_step // self.eval_step)
        else:
            val_sample_interval = 1  # 如果没有eval_step，验证loss全用

        # 验证集损失采样
        val_loss_sampled = self.val_loss_history[::val_sample_interval]
        # 验证集横轴x坐标（注意：val_loss通常每eval_step统计一次）
        # 这里构造val_x_steps: 0, eval_step, 2*eval_step, ...
        val_x_steps = np.arange(0, len(self.val_loss_history)*self.eval_step, self.eval_step)[::val_sample_interval]

        # 检查是否有准确率历史
        has_acc_data = len(self.train_acc_history) > 0

        if has_acc_data:
            # ------------------- 有准确率数据，绘制损失+准确率两个子图 -------------------
            # 训练集准确率采样
            train_acc_sampled = self.train_acc_history[::sample_step]
            # 验证集准确率采样
            val_acc_sampled = self.val_acc_history[::val_sample_interval]
            
            # 创建画布，1行2列，宽高12x4英寸
            plt.figure(figsize=(12, 4))
            
            # =============== 子图1：损失曲线 ===============
            plt.subplot(1, 2, 1)
            plt.plot(train_x_steps, train_loss_sampled, label='Train Loss')
            if len(val_loss_sampled) > 0:
                plt.plot(val_x_steps, val_loss_sampled, label='Validation Loss')
            plt.xlabel('Batch')              # 横轴标签
            plt.ylabel('Loss')               # 纵轴标签
            plt.title('Loss Curves')         # 图标题
            plt.legend()                     # 图例
            plt.grid(True)                   # 网格

            # =============== 子图2：准确率曲线 ===============
            plt.subplot(1, 2, 2)
            plt.plot(train_x_steps, train_acc_sampled, label='Train Acc')
            if len(val_acc_sampled) > 0:
                plt.plot(val_x_steps, val_acc_sampled, label='Validation Acc')
            plt.xlabel('Batch')              # 横轴标签
            plt.ylabel('Accuracy')           # 纵轴标签
            plt.title('Accuracy Curves')     # 图标题
            plt.legend()                     # 图例
            plt.grid(True)                   # 网格

            plt.tight_layout()               # 紧凑布局

        else:
            # ------------------- 没有准确率，单独绘制损失曲线 -------------------
            plt.figure(figsize=(8, 4))       # 画布大小

            # 绘制训练集损失曲线
            plt.plot(train_x_steps, train_loss_sampled, label='Train Loss')
            # 若有验证损失则一起绘制
            if len(val_loss_sampled) > 0:
                plt.plot(val_x_steps, val_loss_sampled, label='Validation Loss')
            plt.xlabel('Batch')              # 横轴标签
            plt.ylabel('Loss')               # 纵轴标签
            plt.title('Loss Curves')         # 图标题
            plt.legend()                     # 图例
            plt.grid(True)                   # 网格

            plt.tight_layout()               # 紧凑布局

        plt.show()                           # 显示图形


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
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.best_score = None #记录最佳指标
        self.counter = 0
        self.early_stop = False

        if self.mode not in ['min', 'max']:
            raise ValueError("mode只能是'min'或'max'")

        if self.mode == 'min':
            self.monitor_op = lambda curr, best: curr < best - self.min_delta #监控指标小于最佳指标,val_loss越小越好
        else:
            self.monitor_op = lambda curr, best: curr > best + self.min_delta #监控指标大于最佳指标,val_acc越大越好

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
        mode (str): 'min' 或 'max'，确定"更好"是数值更小或更大
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
                filepath = os.path.dirname(self.filepath) # 获取文件夹路径
                os.makedirs(filepath, exist_ok=True) # 创建文件夹
                self.best_score = current
                # 保存
                file_name = self.filepath.format(epoch='best')
                self._save_model(model, file_name) # 保存模型
                return True  # 有保存
            return False  # 无保存
        else:
            # 每次都保存
            if epoch is not None:
                filepath = self.filepath.format(epoch=epoch, **{self.monitor: current})
            else:
                filepath = self.filepath.format(**{self.monitor: current})
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
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

from torch.utils.tensorboard import SummaryWriter


class TensorBoardCallback:
    def __init__(self, log_dir, flush_secs=10):
        """
        Args:
            log_dir (str): dir to write log.
            flush_secs (int, optional): write to dsk each flush_secs seconds. Defaults to 10.
        """
        self.writer = SummaryWriter(log_dir=log_dir, flush_secs=flush_secs) # 实例化SummaryWriter, log_dir是log存放路径，flush_secs是每隔多少秒写入磁盘

    def draw_model(self, model, input_shape):#graphs
        self.writer.add_graph(model, input_to_model=torch.randn(input_shape)) # 画模型图
        
    def add_loss_scalars(self, step, loss, val_loss):
        self.writer.add_scalars(
            main_tag="training/loss", 
            tag_scalar_dict={"loss": loss, "val_loss": val_loss},
            global_step=step,
            ) # 画loss曲线, main_tag是主tag，tag_scalar_dict是子tag，global_step是步数
        
    def add_acc_scalars(self, step, acc, val_acc):
        self.writer.add_scalars(
            main_tag="training/accuracy",
            tag_scalar_dict={"accuracy": acc, "val_accuracy": val_acc},
            global_step=step,
        ) # 画acc曲线, main_tag是主tag，tag_scalar_dict是子tag，global_step是步数
        
    def add_lr_scalars(self, step, learning_rate):
        self.writer.add_scalars(
            main_tag="training/learning_rate",
            tag_scalar_dict={"learning_rate": learning_rate},
            global_step=step,
        ) # 画lr曲线, main_tag是主tag，tag_scalar_dict是子tag，global_step是步数
    
    def __call__(self, step, **kwargs):
        # add loss,把loss，val_loss取掉，画loss曲线
        loss = kwargs.pop("loss", None)
        val_loss = kwargs.pop("val_loss", None)
        if loss is not None and val_loss is not None:
            self.add_loss_scalars(step, loss, val_loss) # 画loss曲线
        # add acc
        acc = kwargs.pop("acc", None)
        val_acc = kwargs.pop("val_acc", None)
        if acc is not None and val_acc is not None:
            self.add_acc_scalars(step, acc, val_acc) # 画acc曲线
        # add lr
        learning_rate = kwargs.pop("lr", None)
        if learning_rate is not None:
            self.add_lr_scalars(step, learning_rate) # 画lr曲线
