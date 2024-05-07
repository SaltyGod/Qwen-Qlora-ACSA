## **Multidimensional sentiment analysis tasks**

Our task is to determine the emotional tendency of each restaurant review text in 18 dimensions. These 18 dimensions are:
- Location#Transportation
- Location#Downtown
- Location#Easy_to_find
- Service#Queue
- Service#Hospitality
- Service#Parking
- Service#Timely
- Price#Level
- Price#Cost_effective
- Price#Discount
- Ambience#Decoration
- Ambience#Noise
- Ambience#Space
- Ambience#Sanitary
- Food#Portion
- Food#Taste
- Food#Appearance

If you want to know more about the dataset and metrics, see https://github.com/Meituan-Dianping/asap

## **Environment setup & qlora fine-tuning**

My device：Linux，pytorch2.0.1+cu118, A100

1. Before starting, please install the [xtuner](https://github.com/InternLM/tutorial/blob/main/xtuner/README.md) library first：
```cd ~
mkdir -p /root/xtuner0117 && cd /root/xtuner0117

# Pull the source code of version 0.1.17
git clone -b v0.1.17  https://github.com/InternLM/xtuner

# Users who cannot access github please pull from gitee:
# git clone -b v0.1.15 https://gitee.com/Internlm/xtuner

# Enter the source code directory
cd /root/xtuner0117/xtuner

# Install XTuner from source
pip install -e '.[all]'
```
2. With the support of the xtuner library, execute the following fine-tuning instructions to merge the qlora and qwen model configuration files：
```
xtuner train qwen_1.8B_qlora_ASCA.py --deepspeed deepspeed_zero2 # Add deepspeed to accelerate training

xtuner convert pth_to_hf qwen_1.8B_qlora_ASCA.py
./work_dirs/qwen_1.8B_qlora_ASCA/iter_1803.pth ./hf

# Merge qlora files to generate fine-tuned qwen model
xtuner convert merge ./qwen/Qwen1.5-1.8B ./hf Qwen-1.5-1.8B-ASCA --max-shard-size 2GB

# Remove intermediate products
rm -rf ./hf
```

## **Inference**

You can view related files and execute main.py to complete LLM inference tasks.
The average accuracy of all test sets in 18 dimensions reached 86.1%.
