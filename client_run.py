#!/usr/bin/env python3
"""
Python RPC Client Example

This example demonstrates how to create an RPC client similar to the C++ rpclib example.
It shows how to:
- Connect to an RPC server
- Call remote functions with parameters
- Convert results to specific types
"""

import sys
import os

# Add the parent directory to the path so we can import our rpc module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rpc import Client


def main():
    try:
        # Creating a client that connects to localhost on port 8080
        client = Client("192.168.1.102", 8080)
        
        print("Connected to RPC server!")
        print("Testing various RPC calls...\n")
        
        # Calling a function with parameters and converting the result to int
        # This is similar to: client.call("add", 2, 3).as<int>() in C++
        result = client.call("add", 2, 3).as_int()
        print(f"add(2, 3) = {result}")
        
        # Test other functions
        multiply_result = client.call("multiply", 4, 5).as_int()
        print(f"multiply(4, 5) = {multiply_result}")
        
        # Call function with no parameters
        foo_result = client.call("foo").as_str()
        print(f"foo() = {foo_result}")
        
        # Call function with string parameter
        greet_result = client.call("greet", "World").as_str()
        print(f"greet('World') = {greet_result}")
        
        # Call function that returns a dictionary
        info_result = client.call("get_info").as_dict()
        print(f"get_info() = {info_result}")
        
        # Demonstrate error handling
        try:
            # This should fail because the method doesn't exist
            client.call("nonexistent_method")
        except RuntimeError as e:
            print(f"\nExpected error for nonexistent method: {e}")
        
        # Close the connection
        client.close()
        
    except ConnectionError as e:
        print(f"Failed to connect to server: {e}")
        #print("Make sure the server is running (python examples/server_example.py)")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 