# The MIT License (MIT)

# Copyright (c) 2021-2022 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#!/bin/bash

device=$1
locale=$2

rm -rf screenshots && mkdir -p screenshots
rm -rf sd && mkdir -p sd && rm -f sd/settings.json
echo "{\"settings\": {\"i18n\": {\"locale\": \"$locale\"}}}" > sd/settings.json

poetry run python simulator.py --sequence sequences/about.txt  --device $device
poetry run python simulator.py --sequence sequences/bitcoin-options.txt  --device $device
poetry run python simulator.py --sequence sequences/logging-options.txt  --device $device
poetry run python simulator.py --sequence sequences/extended-public-key-wpkh.txt  --device $device
poetry run python simulator.py --sequence sequences/extended-public-key-wsh.txt  --device $device
poetry run python simulator.py --sequence sequences/home-options.txt  --device $device
poetry run python simulator.py --sequence sequences/load-mnemonic-options.txt  --device $device
poetry run python simulator.py --sequence sequences/load-mnemonic-via-numbers.txt  --device $device
poetry run python simulator.py --sequence sequences/load-mnemonic-via-qr.txt  --device $device
poetry run python simulator.py --sequence sequences/load-mnemonic-via-stackbit.txt  --device $device
poetry run python simulator.py --sequence sequences/load-mnemonic-via-text.txt  --device $device
poetry run python simulator.py --sequence sequences/load-mnemonic-via-tinyseed.txt  --device $device
poetry run python simulator.py --sequence sequences/language-options.txt  --device $device
poetry run python simulator.py --sequence sequences/login-options.txt  --device $device
poetry run python simulator.py --sequence sequences/logo.txt  --device $device
poetry run python simulator.py --sequence sequences/new-mnemonic-options.txt  --device $device
poetry run python simulator.py --sequence sequences/new-mnemonic-via-d6.txt  --device $device
poetry run python simulator.py --sequence sequences/new-mnemonic-via-d20.txt  --device $device
poetry run python simulator.py --sequence sequences/new-mnemonic-via-snapshot.txt  --device $device
poetry run python simulator.py --sequence sequences/print-qr.txt --sd --printer --device $device
poetry run python simulator.py --sequence sequences/printer-options.txt  --device $device
poetry run python simulator.py --sequence sequences/scan-address.txt --device $device
poetry run python simulator.py --sequence sequences/settings-options.txt  --device $device
poetry run python simulator.py --sequence sequences/shutdown.txt  --device $device
poetry run python simulator.py --sequence sequences/sign-message.txt  --device $device
poetry run python simulator.py --sequence sequences/sign-options.txt  --device $device
poetry run python simulator.py --sequence sequences/sign-psbt.txt  --device $device
poetry run python simulator.py --sequence sequences/thermal-options.txt  --device $device
poetry run python simulator.py --sequence sequences/wallet-type-options.txt  --device $device
poetry run python simulator.py --sequence sequences/wallet-wpkh.txt  --device $device
poetry run python simulator.py --sequence sequences/wallet-wsh.txt  --device $device
