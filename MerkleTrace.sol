pragma solidity >=0.4.7 <0.6.0;

contract MerkleTrace {

    struct itemDetail{
        string name;
        string trace_path;
    }
    uint item_id;
    mapping(string => itemDetail) item;



    function concat(string _base, string _value) internal returns (string) {
        bytes memory _baseBytes = bytes(_base);
        bytes memory _valueBytes = bytes(_value);
        string memory tmp = new string(_baseBytes.length + _valueBytes.length);
        bytes memory _newValue = bytes(tmp);

        uint i;
        uint j = 0;

        for(i=0; i<_baseBytes.length; i++) {
            _newValue[j++] = _baseBytes[i];
        }

        for(i=0; i<_valueBytes.length; i++) {
            _newValue[j++] = _valueBytes[i];
        }

        return string(_newValue);
    }

    function test() public returns(string ){
        string memory _name = item['123'].name;
        string memory _trace_path = item['123'].trace_path;
        return concat(_name, _trace_path);
    }
    function query(string  addr) public returns(string ){
        string memory _name = item[addr].name;
        string memory _trace_path = item[addr].trace_path;
        return concat(_name, _trace_path);
    }
    function add_item(string addr, string _name) public returns(bool){
        item[addr].name = _name;
        return true;
    }
    function add_path(string addr, string memory input) public returns(bool){
        string memory tmp = item[addr].trace_path;
        item[addr].trace_path = concat(tmp, input);
        return true;
    }

}