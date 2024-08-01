pragma solidity ^0.8.0;

contract Vesting {
    address public owner;
    mapping(address => Role) public roles;
    enum Role { None, User, Partner, Team }

    // Vesting schedule and logic
    uint256 public constant USER_ALLOCATION = 50;
    uint256 public constant PARTNER_ALLOCATION = 25;
    uint256 public constant TEAM_ALLOCATION = 25;

    uint256 public constant USER_CLIFF = 10 * 30 days;
    uint256 public constant PARTNER_CLIFF = 2 * 30 days;
    uint256 public constant TEAM_CLIFF = 2 * 30 days;

    // Define other relevant variables and mappings

    constructor() {
        owner = msg.sender;
    }

    function addBeneficiary(address _beneficiary, Role _role) public onlyOwner {
        roles[_beneficiary] = _role;
    }

    function claimTokens() public {
        // Implement token claiming logic based on role
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }
}
