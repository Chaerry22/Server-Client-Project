## By Daniel Chae
## 4/18/2024
## CS 232
## Caesar Client
############################################

import socket 
import sys

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((HOST, PORT))
        print("Connected")
        print("Welcome to Caesar Client Server!")
        
        rotations = (input("How many rotations would you like? (1-25): "))

        #this check will be implemented on server side as well
        if(int(rotations) > 25 or int(rotations) < 1):
            s.close()
            raise Exception("Rotation out of bounds. Exiting")
            

        s.send(rotations.encode())

        print((s.recv(1024)).decode())

        while(True):
            string_input = input("Enter String to send: ")
            #to check for all versions of string quit
            check_for_quit = string_input.lower()
            if(check_for_quit == "quit"):
                print("Exiting... goodbye")
                s.close()
                break
            s.sendall(string_input.encode())
            print("Data sent!: ", string_input )
            string_received = s.recv(1024).decode()
            print("Data received!: ", string_received)


    except Exception as e:
        print(f"Error:", e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
