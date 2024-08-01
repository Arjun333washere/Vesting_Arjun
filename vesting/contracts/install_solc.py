import solcx

# Install Solidity compiler version 0.8.18
solcx.install_solc('0.8.18')

# Verify installation
print(solcx.get_installed_solc_versions())
