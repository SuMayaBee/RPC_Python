#!/usr/bin/env python3
"""
Python RPC Server Example

This example demonstrates how to create an RPC server similar to the C++ rpclib example.
It shows how to:
- Create a server that listens on port 8080
- Bind functions (both regular functions and lambdas)
- Run the server loop
"""

import sys
import os

# Add the parent directory to the path so we can import our rpc module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rpc import Server


def foo():
    """A simple function that prints a message"""
    print("foo was called!")
    return "foo executed successfully"


def main():
    # Creating a server that listens on port 8080
    srv = Server(8080)
    
    # Binding the name "foo" to the free function foo.
    # Note: the signature is automatically captured
    srv.bind("foo", foo)
    
    # Binding a lambda function to the name "add".
    srv.bind("add", lambda a, b: a + b)
    
    # You can also bind more complex functions
    srv.bind("multiply", lambda x, y: x * y)
    srv.bind("greet", lambda name: f"Hello, {name}!")
    
    # Bind a function that returns a dictionary
    srv.bind("get_info", lambda: {
        "server": "Python RPC Server",
        "version": "1.0.0",
        "status": "running"
    })
    
    print("Starting RPC server...")
    print("Available methods: foo, add, multiply, greet, get_info")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Run the server loop (this will block)
        srv.run()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        srv.stop()


if __name__ == "__main__":
    main() 