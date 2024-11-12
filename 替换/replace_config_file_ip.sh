#!/bin/bash
function SED_CONFIG() {
    # 定义需要替换的 IP 地址及其对应的新 IP 地址
	declare -A IP_MAP=(
	["10-101-166"]="10-101-224"
    ["10.101.166"]="10.101.224"
    ["10-101-174"]="10-101-225"
    ["10.101.174"]="10.101.225"
    ["10-101-176"]="10-101-226"
    ["10.101.176"]="10.101.226"
	)
	# 遍历所有需要替换的 IP ,其中${IP_MAP[@]}：表示获取关联数组中所有的值,${!IP_MAP[@]}：表示获取关联数组中所有的键
	for OLD_IP in "${!IP_MAP[@]}";do
		NEW_IP="${IP_MAP[$OLD_IP]}"
		# 使用 grep -l 获取包含目标 IP 的文件列表 -a 将所有文件视为文本文件进行搜索 . 表示当前目录
		for f in $(grep -Rla "$DLD_IP" .);do
		#\< 和 \> 是为了匹配完整的单词边界，即确保替换只发生在完全匹配的单词上，而不是单词的子串上
		#\<：匹配单词的开始。\>：匹配单词的结束。
			sed -i "s/\<$DLD_IP\>/$NEW_IP/g" "$f" 
			
		done
	done
}

# 定义需要处理的目录
DIRECTORIES=(
    "/etc/supervisor.d"
    "/data/server"
    "/data/svr"
    "/home/svr"
)

# 遍历并检查每个目录是否存在，然后调用替换函数
for DIR in "${DIRECTORIES[@]}";do
	if [ -d "$DIR" ];then
		cd "$DIR" || continue
		SED_CONFIG
	fi
done
