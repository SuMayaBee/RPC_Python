#!/usr/bin/env python3
"""
Demo script showing Python RPC library usage
Similar to the C++ rpclib examples
"""

import time
import threading
from rpc import Server, Client


def demo_server_client():
    """Demonstrate server and client functionality"""
    print("=== Python RPC Library Demo ===")
    print("Similar to C++ rpclib functionality\n")
    
    # Create server (equivalent to: rpc::server srv(8080))
    print("1. Creating server...")
    srv = Server(8080)
    
    # Define a function to bind
    def foo():
        print("foo was called!")
        return "foo executed successfully"
    
    # Bind functions (equivalent to: srv.bind("foo", &foo))
    print("2. Binding functions...")
    srv.bind("foo", foo)
    srv.bind("add", lambda a, b: a + b)
    srv.bind("multiply", lambda x, y: x * y)
    srv.bind("greet", lambda name: f"Hello, {name}!")
    
    # Start server asynchronously (equivalent to: srv.async_run())
    print("3. Starting server asynchronously...")
    server_thread = srv.async_run()
    time.sleep(1)  # Give server time to start
    
    try:
        # Create client (equivalent to: rpc::client client("127.0.0.1", 8080))
        print("4. Creating client and connecting...")
        client = Client("127.0.0.1", 8080)
        
        print("\n5. Making RPC calls...")
        
        # Call add function (equivalent to: client.call("add", 2, 3).as<int>())
        result = client.call("add", 2, 3).as_int()
        print(f"   add(2, 3) = {result}")
        
        # Call multiply function
        result = client.call("multiply", 4, 5).as_int()
        print(f"   multiply(4, 5) = {result}")
        
        # Call foo function
        result = client.call("foo").as_str()
        print(f"   foo() = '{result}'")
        
        # Call greet function
        result = client.call("greet", "World").as_str()
        print(f"   greet('World') = '{result}'")
        
        print("\n6. Demonstrating error handling...")
        try:
            client.call("nonexistent_method")
        except RuntimeError as e:
            print(f"   Expected error: {str(e).split(':')[0]}...")
        
        # Close client connection
        client.close()
        print("\n7. Demo completed successfully!")
        
    finally:
        # Stop server
        srv.stop()
        server_thread.join(timeout=1)
        print("8. Server stopped.")


if __name__ == "__main__":
    demo_server_client() 