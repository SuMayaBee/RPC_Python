"""
RPC Server implementation
"""

import socket
import threading
import msgpack
import json
import inspect
from typing import Dict, Callable, Any, Optional
import traceback


class Server:
    """
    RPC Server that can bind functions and handle remote procedure calls.
    
    Similar to the C++ rpclib server, this allows you to:
    - Bind functions to names for remote calling
    - Handle multiple concurrent connections
    - Automatically capture function signatures
    """
    
    def __init__(self, port: int, host: str = "0.0.0.0"):
        """
        Initialize the RPC server.
        
        Args:
            port: Port number to listen on
            host: Host address to bind to (default: localhost)
        """
        self.host = host
        self.port = port
        self.functions: Dict[str, Callable] = {}
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        
    def bind(self, name: str, func: Callable) -> None:
        """
        Bind a function to a name for RPC calls.
        
        Args:
            name: The name to bind the function to
            func: The function to bind (can be a regular function, lambda, or method)
        """
        self.functions[name] = func
        print(f"Bound function '{name}' with signature: {inspect.signature(func)}")
    
    def _handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        Handle a client connection in a separate thread.
        
        Args:
            client_socket: The client socket
            address: Client address tuple
        """
        print(f"Client connected from {address}")
        
        try:
            while self.running:
                # Receive data
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    # Unpack the request
                    request = msgpack.unpackb(data, raw=False)
                    
                    # Process the request
                    response = self._process_request(request)
                    
                    # Send response
                    response_data = msgpack.packb(response)
                    client_socket.send(response_data)
                    
                except Exception as e:
                    # Send error response
                    error_response = {
                        "error": str(e),
                        "traceback": traceback.format_exc()
                    }
                    error_data = msgpack.packb(error_response)
                    client_socket.send(error_data)
                    
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Client {address} disconnected")
    
    def _process_request(self, request: dict) -> dict:
        """
        Process an RPC request and return the response.
        
        Args:
            request: The request dictionary containing method name and parameters
            
        Returns:
            Response dictionary with result or error
        """
        try:
            method_name = request.get("method")
            params = request.get("params", [])
            
            if method_name not in self.functions:
                return {"error": f"Method '{method_name}' not found"}
            
            func = self.functions[method_name]
            
            # Call the function with parameters
            if isinstance(params, list):
                result = func(*params)
            elif isinstance(params, dict):
                result = func(**params)
            else:
                result = func(params)
            
            return {"result": result}
            
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
    
    def run(self) -> None:
        """
        Start the server and run the main loop (blocking).
        This is similar to srv.run() in the C++ version.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"RPC Server listening on {self.host}:{self.port}")
            print(f"Available methods: {list(self.functions.keys())}")
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()
    
    def async_run(self) -> threading.Thread:
        """
        Start the server in a separate thread (non-blocking).
        Similar to srv.async_run() in the C++ version.
        
        Returns:
            The thread object running the server
        """
        server_thread = threading.Thread(target=self.run, daemon=True)
        server_thread.start()
        return server_thread
    
    def stop(self) -> None:
        """
        Stop the server.
        """
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Server stopped") 