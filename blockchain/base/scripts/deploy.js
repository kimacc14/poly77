// Deployment script for SentimentOracle contract on Base
const hre = require("hardhat");

async function main() {
    console.log("Deploying SentimentOracle to Base...");

    // Get deployer account
    const [deployer] = await hre.ethers.getSigners();
    console.log("Deploying with account:", deployer.address);

    // Get account balance
    const balance = await deployer.getBalance();
    console.log("Account balance:", hre.ethers.utils.formatEther(balance), "ETH");

    // Deploy contract
    const SentimentOracle = await hre.ethers.getContractFactory("SentimentOracle");
    const sentimentOracle = await SentimentOracle.deploy();

    await sentimentOracle.deployed();

    console.log("SentimentOracle deployed to:", sentimentOracle.address);

    // Verify contract on Basescan (if on mainnet)
    if (hre.network.name === "base" || hre.network.name === "base-mainnet") {
        console.log("Waiting for block confirmations...");
        await sentimentOracle.deployTransaction.wait(6);

        console.log("Verifying contract on Basescan...");
        try {
            await hre.run("verify:verify", {
                address: sentimentOracle.address,
                constructorArguments: [],
            });
            console.log("Contract verified successfully");
        } catch (error) {
            console.log("Error verifying contract:", error.message);
        }
    }

    // Save deployment info
    const fs = require("fs");
    const deploymentInfo = {
        network: hre.network.name,
        address: sentimentOracle.address,
        deployer: deployer.address,
        timestamp: new Date().toISOString(),
        txHash: sentimentOracle.deployTransaction.hash
    };

    fs.writeFileSync(
        "./deployment-info.json",
        JSON.stringify(deploymentInfo, null, 2)
    );

    console.log("\nDeployment info saved to deployment-info.json");
    console.log("\nNext steps:");
    console.log("1. Update backend .env with contract address:");
    console.log(`   BASE_CONTRACT_ADDRESS=${sentimentOracle.address}`);
    console.log("2. Authorize submitter addresses using authorizeSubmitter()");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
