rm -rf eth_data/*

geth --datadir './eth_data' init genesis.json

geth \
--networkid 1024 --identity "trace" --rpc --rpcaddr "0.0.0.0" --rpcport "8545" \
--datadir './eth_data' --port "30303" --rpcapi "db,eth,net,web3,personal,miner,admin,txpool,gasprice,shh,version" \
--rpccorsdomain "*" console

admin.nodeInfo
admin.addPeer
admin.peers


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

mkdir -p qdata/logs
mkdir -p qdata/node1/keystore
mkdir -p qdata/node1/geth
mkdir -p qdata/node1/keys

cd qdata/node1/keystore
geth account new --keystore .