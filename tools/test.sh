#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build/tests
clang++ -std=c++17 -Wall -Wextra -Werror tests/tweeter-mirror.cpp -o build/tests/tweeter-mirror
build/tests/tweeter-mirror
clang++ -std=c++17 -include initializer_list src/CirrusAudioFixup/Tests/output-policy.cpp -o build/tests/output-policy
build/tests/output-policy
python3 src/CirrusAudioFixup/Tests/check_stop_backport.py
