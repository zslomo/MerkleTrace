## 重新部署本地链
```
# 删除数据
rm -rf eth_data/*
# 初始化
geth --datadir './eth_data' init genesis.json
# 启动
geth \
--networkid 1024 --identity "trace" --rpc --rpcaddr "0.0.0.0" --rpcport "8545" \
--datadir './eth_data' --port "30303" --rpcapi "db,eth,net,web3,personal,miner,admin,txpool,gasprice,shh,version" \
--rpccorsdomain "*"
```
## 动态加入节点相关命令
A节点
```
admin.nodeInfo
```
用以下命令添加admin.nodeInfo的输出信息，注意更改IP
```
admin.addPeer
```

## 创始区块
```
genesis.json
{
    "alloc": {},
    "coinbase": "0x0000000000000000000000000000000000000000",
    "config": {
    "homesteadBlock": 0,
    "chainId": 1,
    "eip155Block": null,
    "eip158Block": null,
    "isQuorum": true
    },
    "difficulty": "0x0",
    "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "gasLimit": "0xE0000000",
    "mixhash": "0x00000000000000000000000000000000000000647572616c65787365646c6578",
    "nonce": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "timestamp": "0x00"
}
```

