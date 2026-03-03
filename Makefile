# ****************************************************************************
#    Ledger App Bitcoin
#    (c) 2023 Ledger SAS.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ****************************************************************************

########################################
#        Mandatory configuration       #
########################################

# Application version
# To use Trusted Input for segwit, app version must be kept > 2.0.0
APPVERSION_M = 2
APPVERSION_N = 0
APPVERSION_P = 3

APPDEVELOPPER="Ledger"
APPCOPYRIGHT="(c) 2024 Ledger"

APPNAME ="Syscoin"

VARIANT_VALUES = syscoin

# Application source files
# There is no additional sources for bitcoin
#APP_SOURCE_PATH += src/

# simplify for tests
# Setting to allow building variant applications
VARIANT_PARAM = COIN
VARIANT_VALUES = syscoin_test syscoin

# Default to mainnet, but allow testnet builds
ifndef COIN
COIN=syscoin
endif

# Enabling DEBUG flag will enable PRINTF and disable optimizations
#DEBUG = 1

ifeq ($(COIN),syscoin_test)

# Syscoin testnet configuration
BIP44_COIN_TYPE=1
BIP44_COIN_TYPE_2=1
COIN_P2PKH_VERSION=111
COIN_P2SH_VERSION=196
COIN_NATIVE_SEGWIT_PREFIX=\"tb\"
COIN_COINID_SHORT=\"TEST\"
COIN_COINID=\"Syscoin\"

# Add to compiler defines
DEFINES   += BIP32_PUBKEY_VERSION=0x043587CF
DEFINES   += BIP44_COIN_TYPE=$(BIP44_COIN_TYPE)
DEFINES   += BIP44_COIN_TYPE_2=$(BIP44_COIN_TYPE_2)
DEFINES   += COIN_P2PKH_VERSION=$(COIN_P2PKH_VERSION)
DEFINES   += COIN_P2SH_VERSION=$(COIN_P2SH_VERSION)
DEFINES   += COIN_NATIVE_SEGWIT_PREFIX=$(COIN_NATIVE_SEGWIT_PREFIX)
DEFINES   += COIN_COINID_SHORT=$(COIN_COINID_SHORT)

# Name of the coin that will be used in the app display
COIN_COINID_NAME="Syscoin Test"

# Testnet derivation paths (more comprehensive for testing)
APP_LOAD_PARAMS += --path "0'/1'" --path "44'/1'" --path "45'/1'" --path "84'/1'" --path "86'/1'" --path "48'/1'" --path "49'/1'"

else ifeq ($(COIN),syscoin)

# Syscoin mainnet configuration (production)
BIP44_COIN_TYPE=57
BIP44_COIN_TYPE_2=57
COIN_P2PKH_VERSION=63
COIN_P2SH_VERSION=5
COIN_NATIVE_SEGWIT_PREFIX=\"sys\"
COIN_COINID_SHORT=\"SYS\"
COIN_COINID=\"Syscoin\"

# Add to compiler defines
DEFINES   += BIP32_PUBKEY_VERSION=0x0488B21E 
DEFINES   += BIP44_COIN_TYPE=$(BIP44_COIN_TYPE)
DEFINES   += BIP44_COIN_TYPE_2=$(BIP44_COIN_TYPE_2)
DEFINES   += COIN_P2PKH_VERSION=$(COIN_P2PKH_VERSION)
DEFINES   += COIN_P2SH_VERSION=$(COIN_P2SH_VERSION)
DEFINES   += COIN_NATIVE_SEGWIT_PREFIX=$(COIN_NATIVE_SEGWIT_PREFIX)
DEFINES   += COIN_COINID_SHORT=$(COIN_COINID_SHORT)

# Name of the coin that will be used in the app display
COIN_COINID_NAME="Syscoin"

# Mainnet derivation paths (standard Bitcoin-compatible)
APP_LOAD_PARAMS += --path "44'/57'" --path "45'/57'" --path "84'/57'" --path "86'/57'"

else
ifeq ($(filter clean,$(MAKECMDGOALS)),)
$(error Unsupported COIN - use $(VARIANT_VALUES))
endif
endif

# COIN_FAMILY can be set to FAMILY_BITCOIN, FAMILY_PEERCOIN, or FAMILY_STEALTH to handle 
# parsing of the timestamp in the transaction (see lib-app-bitcoin/transaction.c)
COIN_FAMILY=FAMILY_BITCOIN

# COIN_FLAGS can be set to FLAG_PEERCOIN_UNITS, FLAG_PEERCOIN_SUPPORT, or
# FLAG_SEGWIT_CHANGE_SUPPORT, (see lib-app-bitcoin/transaction.c and
# lib-app-bitcoin/hash_input_finalize_full.c)
COIN_FLAGS=FLAG_SEGWIT_CHANGE_SUPPORT

# COIN_FORKID can be set if needed
COIN_FORKID=0

include lib-app-bitcoin/Makefile
