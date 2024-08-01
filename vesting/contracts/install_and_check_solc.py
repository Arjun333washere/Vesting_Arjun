import solcx

# Install Solidity compiler version 0.8.18
solcx.install_solc('0.8.18')

# Print installed Solidity compiler versions
print("Installed Solidity compiler versions:", solcx.get_installed_solc_versions())