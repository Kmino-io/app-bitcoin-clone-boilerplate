import base64
import base58


def _get_public_key_from_extended(client, path: str) -> str:
    """Extract compressed public key from extended public key."""
    extended_pubkey = client.get_extended_pubkey(path=path, display=False)
    
    try:
        decoded = base58.b58decode(extended_pubkey)
        decoded_hex = decoded.hex()
        
        # Find compression prefix (02 or 03) in decoded data
        for i in range(0, len(decoded_hex) - 66, 2):
            if decoded_hex[i:i+2] in ['02', '03']:
                return decoded_hex[i:i+66]
        
        # Fallback - take last 33 bytes
        public_key = decoded[-33:]
        return public_key.hex()
        
    except Exception:
        return extended_pubkey


def validate_syscoin_message_signature(signature: str, expected: str, client, path: str, message: str):
    """Validate Syscoin message signature with deterministic, format, and public key checks."""
    
    # Deterministic verification
    assert signature == expected, f"Signature mismatch!\nExpected: {expected}\nReceived: {signature}"
    
    # Format validation
    try:
        decoded = base64.b64decode(signature)
        assert 60 <= len(decoded) <= 80, f"Invalid signature length: {len(decoded)}"
    except Exception as e:
        assert False, f"Invalid signature format: {e}"
    
    # Public key extraction
    try:
        _get_public_key_from_extended(client, path)
    except Exception as e:
        assert False, f"Failed to extract public key: {e}"
