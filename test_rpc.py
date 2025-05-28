#!/usr/bin/env python3
"""
Test script for the Python RPC library
"""

import threading
import time
import sys
from rpc import Server, Client


def test_basic_functionality():
    """Test basic RPC functionality"""
    print("Testing basic RPC functionality...")
    
    # Create and start server
    srv = Server(8081)  # Use different port to avoid conflicts
    srv.bind("add", lambda a, b: a + b)
    srv.bind("multiply", lambda x, y: x * y)
    srv.bind("greet", lambda name: f"Hello, {name}!")
    
    # Start server in background
    server_thread = srv.async_run()
    time.sleep(1)  # Give server time to start
    
    try:
        # Test client
        client = Client("127.0.0.1", 8081)
        
        # Test add function
        result = client.call("add", 5, 3).as_int()
        assert result == 8, f"Expected 8, got {result}"
        print("✓ add(5, 3) = 8")
        
        # Test multiply function
        result = client.call("multiply", 4, 6).as_int()
        assert result == 24, f"Expected 24, got {result}"
        print("✓ multiply(4, 6) = 24")
        
        # Test greet function
        result = client.call("greet", "Python").as_str()
        assert result == "Hello, Python!", f"Expected 'Hello, Python!', got {result}"
        print("✓ greet('Python') = 'Hello, Python!'")
        
        # Test error handling
        try:
            client.call("nonexistent")
            assert False, "Should have raised an exception"
        except RuntimeError:
            print("✓ Error handling works correctly")
        
        client.close()
        print("✓ All tests passed!")
        
    finally:
        srv.stop()
        server_thread.join(timeout=1)


if __name__ == "__main__":
    test_basic_functionality() 