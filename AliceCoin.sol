pragma solidity ^0.5.0;

contract ERC20Interface {
    function totalSupply() public view returns (uint);
    function balanceOf(address tokenOwner) public view returns (uint balance);
    function allowance(address tokenOwner, address spender) public view returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);

    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}

contract SafeMath {
    function safeAdd(uint a, uint b) public pure returns (uint c) {
        c = a + b;
        require(c >= a, "safeAdd condition failed.");
    }
    function safeSub(uint a, uint b) public pure returns (uint c) {
        require(b <= a, "safeSub condition failed.");
        c = a - b;
    }
    function safeMul(uint a, uint b) public pure returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b, "safeMul condition failed.");
    }
    function safeDiv(uint a, uint b) public pure returns (uint c) {
        require(b > 0, "safeDiv condition failed.");
        c = a / b;
    }
}

contract AliceCoin is ERC20Interface, SafeMath{
    
    uint supply;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;

    uint8 public constant decimals = 18;

    constructor (uint256 _initialSupply) public {
        balances[msg.sender] = _initialSupply;
        supply = _initialSupply;
    }
    
    function totalSupply() public view returns (uint){
        return supply;
    }
    
    function balanceOf(address tokenOwner) public view returns (uint balance){
        return balances[tokenOwner];
    }
    
    function allowance(address tokenOwner, address spender) public view returns (uint remaining){
        return allowed[tokenOwner][spender];
    }
    
    function transfer(address to, uint tokens) public returns (bool success){
        balances[msg.sender] = safeSub(balances[msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        emit Transfer(msg.sender, to, tokens);
        return true;
    }
    
    function approve(address spender, uint tokens) public returns (bool success){
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        return true;
    }
    
    function transferFrom(address from, address to, uint tokens) public returns (bool success){
        balances[from] = safeSub(balances[from], tokens);
        allowed[from][msg.sender] = safeSub(allowed[from][msg.sender], tokens);
        balances[to] = safeAdd(balances[to], tokens);
        emit Transfer(from, to, tokens);
        return true;
    }
    
    function mintNewTokens(address to, uint tokens) public{
        supply += tokens;
        balances[to] += tokens;
    }
    
    function () external payable {
        revert("Payment of ETH not allowed.");
    }
}
