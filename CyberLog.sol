// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CyberLog {
    struct Alert {
        string sessionId;
        bool detected;
        uint256 timestamp;
    }

    Alert[] private alerts;
    event AlertLogged(string sessionId, bool detected, uint256 timestamp);

    function logAlert(string memory sessionId, bool detected) public {
        alerts.push(Alert(sessionId, detected, block.timestamp));
        emit AlertLogged(sessionId, detected, block.timestamp);
    }

    function getAlertCount() public view returns (uint256) {
        return alerts.length;
    }

    function getAlert(uint256 index)
        public
        view
        returns (string memory, bool, uint256)
    {
        require(index < alerts.length, "Invalid alert index");
        Alert memory alert = alerts[index];
        return (alert.sessionId, alert.detected, alert.timestamp);
    }
}
