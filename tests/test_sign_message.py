
import pytest
from ragger.navigator import Navigator
from ragger.firmware import Firmware
from ragger_bitcoin import RaggerClient
from ragger_bitcoin.ragger_instructions import Instructions
from ragger.navigator import NavInsID

from utils.validations_sign_message import validate_syscoin_message_signature


def message_instruction_approve(model: Firmware) -> Instructions:
    instructions = Instructions(model)
    if model.is_nano:
        instructions.new_request("Approve")
        instructions.nano_skip_screen("Message")
        instructions.same_request("Sign")
    else:
        instructions.address_confirm()
        instructions.same_request("Address", NavInsID.SWIPE_CENTER_TO_LEFT,
                                  NavInsID.USE_CASE_STATUS_DISMISS)
        instructions.confirm_message()
    return instructions


def test_sign_message(navigator: Navigator, firmware: Firmware,
                      client: RaggerClient, test_name: str):
    """Test message signing with different BIP32 paths and message content."""
    
    # Test with the original known case first
    message = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks."
    bip32_path = "m/44'/57'/0'/0/0"
    
    result = client.sign_message(message=message, bip32_path=bip32_path, navigator=navigator,
                                 instructions=message_instruction_approve(firmware),
                                 testname=test_name)

    expected_signature = "MEQCIHx0pcPt48grh8BXyr+6EJo2MjI29PVDoxDD34m/xgsGAiAGoh/dWQFbdbxK7fu4O935GyqSP2XzOSgOiSQKRTKvgQ=="
    
    validate_syscoin_message_signature(
        signature=result,
        expected=expected_signature,
        client=client,
        path=bip32_path,
        message=message
    )
    
    # Test different BIP32 paths with the same message
    path_testcases = {
        "m/44'/57'/1'/0/0": "MUQCIHXgynd6BiGmFNKeehUkwXCH2CHZvAFFLsykJiKCScAQAiBbSIYUwC2AiZ7iXt8q6ZSxqSAt3pQX7iysAhfU+1Q+kw==",
        "m/84'/57'/0'/0/0": "MEUCIQDCr5jbfcykjQVy1E4BvSZ7f8z+2CVdQAxIDmJSmJJOygIgbNzWa1L7JIgb7Yi/DnlNCRbbXPycyNA7jTmgvWPDXFg=",
    }
    
    # Test each path with the same message
    for path, expected_sig in path_testcases.items():
        result = client.sign_message(
            message=message,
            bip32_path=path,
            navigator=navigator,
            instructions=message_instruction_approve(firmware),
            testname=f"{test_name}_{path}"
        )
        
        validate_syscoin_message_signature(
            signature=result,
            expected=expected_sig,
            client=client,
            path=path,
            message=message
        )
    
    # Test different messages with the same path
    message_testcases = {
        "Hello": "MUQCIC57J5P3IwotVAdY1/eaEcJNzZ/aHA82h9iW/KeHbxY5AiAxOrSY3l3N/1ZPZpxIQ7adv4mRpAJjWTYkXieUQqqp5Q==",
        "Test": "MEUCIQC9ysFMFWMrOjoOnmbHCT+MHcHMsw7y/7YMPgdTqzeH1QIgdjp1Sw6xdg1qJRHERsgDWUy2f+YrBhZ1AGHuX2T/Bcw=",
    }
    
    # Test each message with the same path
    base_path = "m/44'/57'/0'/0/0"
    for msg, expected_sig in message_testcases.items():
        result = client.sign_message(
            message=msg,
            bip32_path=base_path,
            navigator=navigator,
            instructions=message_instruction_approve(firmware),
            testname=f"{test_name}_{msg}"
        )
        
        validate_syscoin_message_signature(
            signature=result,
            expected=expected_sig,
            client=client,
            path=base_path,
            message=msg
        )
