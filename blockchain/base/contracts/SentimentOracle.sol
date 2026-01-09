// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SentimentOracle
 * @dev On-chain oracle for verified sentiment analysis results on Base (Ethereum L2)
 */
contract SentimentOracle {

    struct SentimentRecord {
        bytes32 dataHash;          // Hash of input social data
        int256 sentimentScore;     // Sentiment score (-100 to +100)
        uint256 mentionCount;      // Number of mentions
        uint256 timestamp;         // Record timestamp
        address submitter;         // Address that submitted the record
        bool verified;             // Verification status
        string topic;              // Topic/market identifier
    }

    // Mapping from record ID to sentiment record
    mapping(bytes32 => SentimentRecord) public records;

    // Array of all record IDs for enumeration
    bytes32[] public recordIds;

    // Mapping from topic to array of record IDs
    mapping(string => bytes32[]) public topicRecords;

    // Owner address (for access control)
    address public owner;

    // Authorized submitters
    mapping(address => bool) public authorizedSubmitters;

    // Events
    event SentimentSubmitted(
        bytes32 indexed recordId,
        string indexed topic,
        int256 sentimentScore,
        uint256 mentionCount,
        uint256 timestamp
    );

    event SubmitterAuthorized(address indexed submitter);
    event SubmitterRevoked(address indexed submitter);

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyAuthorized() {
        require(
            authorizedSubmitters[msg.sender] || msg.sender == owner,
            "Not authorized to submit"
        );
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedSubmitters[msg.sender] = true;
    }

    /**
     * @dev Submit a sentiment analysis record to the blockchain
     * @param recordId Unique identifier for this record
     * @param dataHash Hash of the input data (for verification)
     * @param sentimentScore Sentiment score (-100 to +100)
     * @param mentionCount Number of social media mentions
     * @param topic Topic or market identifier
     */
    function submitSentiment(
        bytes32 recordId,
        bytes32 dataHash,
        int256 sentimentScore,
        uint256 mentionCount,
        string calldata topic
    ) external onlyAuthorized {
        require(records[recordId].timestamp == 0, "Record already exists");
        require(sentimentScore >= -100 && sentimentScore <= 100, "Invalid sentiment score");

        records[recordId] = SentimentRecord({
            dataHash: dataHash,
            sentimentScore: sentimentScore,
            mentionCount: mentionCount,
            timestamp: block.timestamp,
            submitter: msg.sender,
            verified: true,
            topic: topic
        });

        recordIds.push(recordId);
        topicRecords[topic].push(recordId);

        emit SentimentSubmitted(
            recordId,
            topic,
            sentimentScore,
            mentionCount,
            block.timestamp
        );
    }

    /**
     * @dev Batch submit multiple sentiment records
     * @param _recordIds Array of record IDs
     * @param _dataHashes Array of data hashes
     * @param _sentimentScores Array of sentiment scores
     * @param _mentionCounts Array of mention counts
     * @param _topics Array of topics
     */
    function batchSubmitSentiment(
        bytes32[] calldata _recordIds,
        bytes32[] calldata _dataHashes,
        int256[] calldata _sentimentScores,
        uint256[] calldata _mentionCounts,
        string[] calldata _topics
    ) external onlyAuthorized {
        require(
            _recordIds.length == _dataHashes.length &&
            _recordIds.length == _sentimentScores.length &&
            _recordIds.length == _mentionCounts.length &&
            _recordIds.length == _topics.length,
            "Array length mismatch"
        );

        for (uint256 i = 0; i < _recordIds.length; i++) {
            require(records[_recordIds[i]].timestamp == 0, "Record already exists");
            require(
                _sentimentScores[i] >= -100 && _sentimentScores[i] <= 100,
                "Invalid sentiment score"
            );

            records[_recordIds[i]] = SentimentRecord({
                dataHash: _dataHashes[i],
                sentimentScore: _sentimentScores[i],
                mentionCount: _mentionCounts[i],
                timestamp: block.timestamp,
                submitter: msg.sender,
                verified: true,
                topic: _topics[i]
            });

            recordIds.push(_recordIds[i]);
            topicRecords[_topics[i]].push(_recordIds[i]);

            emit SentimentSubmitted(
                _recordIds[i],
                _topics[i],
                _sentimentScores[i],
                _mentionCounts[i],
                block.timestamp
            );
        }
    }

    /**
     * @dev Get sentiment record by ID
     * @param recordId Record identifier
     */
    function getRecord(bytes32 recordId) external view returns (SentimentRecord memory) {
        return records[recordId];
    }

    /**
     * @dev Get all records for a topic
     * @param topic Topic identifier
     */
    function getTopicRecords(string calldata topic) external view returns (bytes32[] memory) {
        return topicRecords[topic];
    }

    /**
     * @dev Get total number of records
     */
    function getRecordCount() external view returns (uint256) {
        return recordIds.length;
    }

    /**
     * @dev Get latest record for a topic
     * @param topic Topic identifier
     */
    function getLatestTopicRecord(string calldata topic) external view returns (SentimentRecord memory) {
        bytes32[] memory topicRecordIds = topicRecords[topic];
        require(topicRecordIds.length > 0, "No records for topic");

        bytes32 latestId = topicRecordIds[topicRecordIds.length - 1];
        return records[latestId];
    }

    /**
     * @dev Authorize an address to submit sentiment data
     * @param submitter Address to authorize
     */
    function authorizeSubmitter(address submitter) external onlyOwner {
        authorizedSubmitters[submitter] = true;
        emit SubmitterAuthorized(submitter);
    }

    /**
     * @dev Revoke authorization from an address
     * @param submitter Address to revoke
     */
    function revokeSubmitter(address submitter) external onlyOwner {
        authorizedSubmitters[submitter] = false;
        emit SubmitterRevoked(submitter);
    }

    /**
     * @dev Transfer ownership
     * @param newOwner New owner address
     */
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }
}
