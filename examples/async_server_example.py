#!/usr/bin/env python3
"""
Python RPC Async Server Example

This example demonstrates how to run an RPC server asynchronously (non-blocking).
Similar to srv.async_run() in the C++ version.
"""

import sys
import os
import time

# Add the parent directory to the path so we can import our rpc module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rpc import Server


def heavy_computation(n):
    """A function that simulates heavy computation"""
    print(f"Starting heavy computation with n={n}")
    time.sleep(2)  # Simulate work
    result = sum(i * i for i in range(n))
    print(f"Heavy computation completed: {result}")
    return result


def main():
    # Creating a server that listens on port 8080
    srv = Server(8080)
    
    # Bind some functions
    srv.bind("add", lambda a, b: a + b)
    srv.bind("heavy_computation", heavy_computation)
    srv.bind("ping", lambda: "pong")
    
    print("Starting RPC server asynchronously...")
    
    # Start the server in a separate thread (non-blocking)
    server_thread = srv.async_run()
    
    print("Server started! You can now connect clients.")
    print("This main thread is free to do other work...")
    
    # The main thread can continue doing other work
    for i in range(10):
        print(f"Main thread working... {i}")
        time.sleep(1)
    
    print("Main thread work completed.")
    print("Server is still running in the background.")
    print("Press Ctrl+C to stop everything.")
    
    try:
        # Keep the main thread alive
        server_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        srv.stop()


if __name__ == "__main__":
    main() 