mkdir -p /root/xtuner0117 && cd /root/xtuner0117
git clone -b v0.1.17  https://github.com/InternLM/xtuner
cd /root/xtuner0117/xtuner
pip install -e '.[all]'

xtuner train qwen_1.8B_qlora_ASCA.py --deepspeed deepspeed_zero2 # Add deepspeed to accelerate training

xtuner convert pth_to_hf qwen_1.8B_qlora_ASCA.py ./work_dirs/qwen_1.8B_qlora_ASCA/iter_1803.pth ./hf

xtuner convert merge ./qwen/Qwen1.5-1.8B ./hf Qwen-1.5-1.8B-ASCA --max-shard-size 2GB
rm -rf ./hf
