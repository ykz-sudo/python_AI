# Step 1: 对原始双语数据执行预处理操作，包括分词与标点符号规范化。
# 参数说明:
# $1: 源-目标语言配对文件所在目录（pair_dir）
# $2: 预处理输出文件目录（dest_dir）
# $3: 源语言（src_lang, 如 en）
# $4: 目标语言（trg_lang, 如 de）
python data_multi30k.py --pair_dir $1 --dest_dir $2 --src_lang $3 --trg_lang $4

# $1、$2、$3、$4 是 shell 脚本中的位置参数，代表你在运行本脚本时传入的四个参数：
# $1  表示第一个参数，通常在本脚本中用于指定原始数据/配对文件的目录（pair_dir）
# $2  表示第二个参数，指定预处理后数据的输出目录（dest_dir）
# $3  表示第三个参数，指定源语言（src_lang），如 en
# $4  表示第四个参数，指定目标语言（trg_lang），如 de
# 例如运行命令：bash data_multi30k.sh data/raw data/preproc en de
# 这时 $1=data/raw, $2=data/preproc, $3=en, $4=de


# Step 2: 创建一个新的文件train_l，将经过分词的源、目标语言训练数据拼接到一起
# 这样做的目的是生成合并后的训练语料，用于后续联合学习BPE子词分词器
touch $1/train_l  # 创建空文件train_l
cat $2/train_src.cut.txt >> $1/train_l  # 源语言训练数据追加到train_l
cat $2/train_trg.cut.txt >> $1/train_l  # 目标语言训练数据追加到train_l

# Step 3: 基于合并的训练数据生成联合BPE模型和词表
# -i: 输入合并后的分词数据文件
# -s: BPE子词数目设置为20000
# -o: 输出BPE编码规则文件
# --write-vocabulary: 输出词表文件
subword-nmt learn-joint-bpe-and-vocab \
    -i $1/train_l \
    -s 20000 \
    -o $1/bpe.20000 \
    --write-vocabulary $1/vocab

# Step 4: 对训练、验证、测试集中的源/目标句子应用上面学到的BPE模型
# 针对train、val、test分别处理源语言和目标语言分词文件
for mode in train val test; do
    # 对源语言切词文本应用BPE编码，输出到指定文件
    subword-nmt apply-bpe -c $1/bpe.20000 -i $2/${mode}_src.cut.txt -o $1/${mode}_src.bpe
    # 对目标语言切词文本应用BPE编码，输出到指定文件
    subword-nmt apply-bpe -c $1/bpe.20000 -i $2/${mode}_trg.cut.txt -o $1/${mode}_trg.bpe
    # 提示当前数据集分词完成
    echo "Finished applying bpe to ${mode} files."
done
