from ragger.navigator import Navigator
from ragger.firmware import Firmware
from ragger_bitcoin import RaggerClient
from ragger_bitcoin.ragger_instructions import Instructions
from ragger.navigator import NavInsID


def pubkey_instruction_approve(model: Firmware) -> Instructions:
    instructions = Instructions(model)

    if model.is_nano:
        instructions.new_request("Approve")
    else:
        instructions.address_confirm()
        instructions.same_request("Address", NavInsID.USE_CASE_REVIEW_TAP,
                                  NavInsID.USE_CASE_STATUS_DISMISS)
    return instructions


def pubkey_instruction_warning_approve(model: Firmware) -> Instructions:
    instructions = Instructions(model)

    if model.is_nano:
        instructions.new_request("Approve")
        instructions.same_request("Approve")
    else:
        instructions.new_request("Unusual", NavInsID.USE_CASE_CHOICE_CONFIRM,
                                 NavInsID.USE_CASE_CHOICE_CONFIRM)
        instructions.same_request("Confirm",
                                  NavInsID.SWIPE_CENTER_TO_LEFT,
                                  NavInsID.USE_CASE_ADDRESS_CONFIRMATION_CONFIRM)
        instructions.same_request("Address", NavInsID.USE_CASE_REVIEW_TAP,
                                  NavInsID.USE_CASE_STATUS_DISMISS)
    return instructions


def test_get_public_key(navigator: Navigator, firmware: Firmware,
                        client: RaggerClient, test_name: str):
    # Regular BIP paths (44, 49, 84) - no warning needed
    regular_testcases = {
        "m/84'/57'/0'/0/0": "xpub6FmWA2PWkNDPmEfKBQzKaL9mqu4TfV3VLsm2GiCtqwN8uB73WWBdw7RYGusrtg6vZ8a8RrNAoP9xR4oRSUM5RZcVLjXvhJcUiaLsp9vXwLR",
        "m/44'/57'/0'/0/0": "xpub6FR3N26LdwUQCLb8jdr6oFbJJ4coHRMNvLGY4nyr455XBpDkGU1GuCz8GVsHohRTqTx3Pyij9sgX4jEZmbSAFMonvVQ55dkhLd2NyzpLJEi",
        "m/49'/57'/0'/0/0": "xpub6GTihEYUBWz5PX8SsHXY7AViGtpozWo1aaTXtkCkU7mQXWV81GTRqXTuyXFesmxoHwH2tL7zfbwA2jbq5e5KF5Rmx4ncLXJTHUgd5hx6agg",
    }
    
    # Test regular paths
    for path, pubkey in regular_testcases.items():
        assert pubkey == client.get_extended_pubkey(
            path=path,
            display=True,
            navigator=navigator,
            instructions=pubkey_instruction_approve(firmware),
            testname=f"{test_name}_{path}"
        )
    
    # Unusual/Warning BIP paths for Syscoin - require user confirmation
    warning_testcases = {
        "m/86'/57'/0'/0/0": "xpub6GMM1KKAPuS364DhU9v6puzQ4R2WRagG2WH45ojFC6LVZM1M4pgHEfMcWycyq9YQMStm7kJyZgM9k4ZrphbiMK5BXheTx59ukUWgEvA77KW",
        "m/44'/57'/0'": "xpub6DDDtq9CSMYEHemBTmQB5DpwQyCkAg7m8EN8mPgzM4ReJG9v25QxXkaJbRPdipjWRaHR2FpCuXmS6yYpZ2VYR3MhdC8YEh3MezYoHbNzUJh",
        "m/44'/57'/2'/1/42": "xpub6FsDJvL1h133xkt4fThSKYPqbNtGDjKNWEhirHrWTqmJy16H3A83LqL2MiLMBxGb4nXLukTyjR7R1SgNTuMWJSHViDXrsrs5LcKPF9gFt3N", 
        "m/48'/57'/0'/1'/0/7": "xpub6HUmhgfb9jdsS4yaNhBjCwsD1DW2NHRm34wZHVcDEs5UD93TvTPKPtD1kSDWvL5ZFqc6bsYjaEwz7wLBW52HXURzRY8314BwnAjZifh9fb5",
        "m/49'/57'/1'/1/3": "xpub6HER3yZ1LFxi2U7RqdrtzNYhYxoijACAqtLPt3xbZp9qip96eUnSYS4JCT9HtS23tXJ7MWBDdTZhYjJKsz4jvBC4AhneVKkFdk2nnVs3vEZ",
        "m/84'/57'/0'/1/50": "xpub6Fgh8wcjZDYsuGEzMbmcQN8q7SftLMsczxgefvCSAW2f7yPdauJ5Vm6JiaWZ6DCc37tNyqLuNCrhUMCoCXbosN83HRTucgWmxAfyEf44dAk",
    }

    # Test warning paths
    for path, pubkey in warning_testcases.items():

        assert pubkey == client.get_extended_pubkey(
            path=path,
            display=True,
            navigator=navigator,
            instructions=pubkey_instruction_warning_approve(firmware),
            testname=f"{test_name}_{path}"
            )
