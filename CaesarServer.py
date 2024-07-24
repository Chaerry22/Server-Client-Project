
import socket
import sys
import threading

#keep track of connected clients to terminate server when all clients quit
active_connections = 0

def main():
    PORT = int(sys.argv[1])
    try:
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the specified port
        s.bind(("", PORT))
        # Listen for incoming connections, 10 at a time (?)
        s.listen(10)
        print(f"Server listening on port {PORT}")

        # Main loop to accept incoming connections
        while True:
            # Accept a new connection
            conn, addr = s.accept()
            # active connections to close server when active_server == 0
            global active_connections
            #add for each client that connects 
            active_connections += 1
            # Create new thread 
            thread = threading.Thread(target=client_handling, args=(conn, addr, s))
            thread.start()
    
    except ConnectionAbortedError:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the server socket
        s.close()

def client_handling(conn, addr, s):
    try:
        print(f"Connected by {addr}")

        # Receive rotation value from client
        rotation = conn.recv(1024)
        
        rotationInt = int(rotation.decode())

        # Validate rotation value
        if isinstance(rotationInt, int):
            print("Rotation value received")
        else:
            raise Exception("Error: Rotation not integer. Exiting")
            
        if(rotationInt > 25 or rotationInt < 1):
            raise Exception("Rotation out of bounds. Exiting")
        else:
            print(("Rotation value valid. Continuing"))
        
        # Send confirmation back to client
        conn.send(str(rotationInt).encode())

        # Receive data from client and send encrypted data back
        while True:

            data = conn.recv(1024).decode()
            if not data:
                break

            print("Data received from client:", data)

            cipher_data = caesarCipher(data, rotationInt)

            print("Data encrypted:", cipher_data)

            conn.sendall(cipher_data.encode())

        conn.close()
        print(f"Connection with {addr} closed")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        global active_connections
        active_connections -= 1
        #whenever client quits, minus 1
        if active_connections == 0:
            print("No connections. Closing Server...")
            s.close()




#function to encrypt the string
def caesarCipher(data, rotation):

    cipher_message = ""
    if(data == ""):
        return ""

    for char in data:
        if char.isalpha():
            cipher_message += chr(ord(char) + rotation)
            
        else:
            #if not char, leave as be
            cipher_message += char

    return cipher_message


if __name__ == "__main__":
    main()
