# 步骤1：调用 data_multi30k.py 脚本，对原始配对的双语数据进行预处理，包括分词、标点符号归一化。
# 参数说明:
#   $1: 原始双语配对文件目录(pair_dir)
#   $2: 预处理输出目录(dest_dir)
#   $3: 源语言代码(src_lang)，如"de"
#   $4: 目标语言代码(trg_lang)，如"en"
python data_multi30k.py --pair_dir $1 --dest_dir $2 --src_lang $3 --trg_lang $4

# 步骤2：在原始数据目录($1)下创建新文件 train_l，将分词后的训练集（源语言和目标语言）拼接到一起
# 这样做是为了联合训练BPE模型，让BPE子词共享于源/目标语言
touch $1/train_l
# 将分词后的训练集源语言追加到 train_l
cat $2/train_src.cut.txt >> $1/train_l
# 将分词后的训练集目标语言追加到 train_l
cat $2/train_trg.cut.txt >> $1/train_l

# 步骤3：使用 subword-nmt 对合并后的训练数据 train_l 学习联合BPE编码（Byte Pair Encoding）
# 主要参数说明：
#   -i: 输入文件（train_l，已分词合并文件）
#   -s: BPE合并操作次数，此处设为20000，约会生成2万个子词单元
#   -o: 输出BPE规则文件
#   --write-vocabulary: 输出合并词表文件
# 说明：实际词表大小小于20000（见下方补充说明）

# subword-nmt 工具说明：可学习BPE规则(learn-bpe/learn-joint-bpe-and-vocab)并应用(model/apply-bpe)。
# 常用命令示例：
#   1) 联合学习BPE规则（共享子词表）：
#      subword-nmt learn-joint-bpe-and-vocab -i train_l -s 20000 -o bpe.20000 --write-vocabulary vocab
#   2) 应用BPE规则到切分文本：
#      subword-nmt apply-bpe -c bpe.20000 -i infile -o outfile

# vocab 说明：只保留出现频率大于1的子词（极低频次子词不会写入），所以 vocab 的子词个数通常小于20000。这属于正常预期。

subword-nmt learn-joint-bpe-and-vocab \
    -i $1/train_l \
    -s 20000 \
    -o $1/bpe.20000 \
    --write-vocabulary $1/vocab

# 步骤4：将训练好的BPE模型应用到train/val/test的分词文件，生成BPE子词序列
# 结果输出到原数据目录($1)，后缀为 _src.bpe / _trg.bpe
for mode in train val test; do
    # 源语言应用BPE编码
    subword-nmt apply-bpe -c $1/bpe.20000 -i $2/${mode}_src.cut.txt -o $1/${mode}_src.bpe
    # 目标语言应用BPE编码
    subword-nmt apply-bpe -c $1/bpe.20000 -i $2/${mode}_trg.cut.txt -o $1/${mode}_trg.bpe
    # 输出进度提示
    echo "Finished applying bpe to ${mode} files."
done
