import asyncio
import websockets

# Set of connected WebSocket clients
connected_clients = set()

# Handler for WebSocket connections
async def chat_handler(websocket, path):
    # Add the new client to the set of connected clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast received message to all connected clients
            await asyncio.wait([client.send(message) for client in connected_clients])
    except websockets.ConnectionClosed:
        print(f"Client {websocket.remote_address} disconnected")
    finally:
        # Remove client from the set of connected clients when it disconnects
        connected_clients.remove(websocket)

# Start the WebSocket server
async def start_server():
    server = await websockets.serve(chat_handler, "localhost", 8765)
    print("Chat server started on ws://localhost:8765")
    await server.wait_closed()

# Entry point of the program
if __name__ == "__main__":
    asyncio.run(start_server())
