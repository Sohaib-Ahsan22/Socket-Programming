import socket
import threading
import pyaudio

def handle_file_transfer(client_socket):
    try:
       
        filename = client_socket.recv(1024).decode()  #Receive the filename
        print(f"Receiving file: {filename}")
        
     
        with open(filename, 'wb') as f:   #  Receive file content in chunks
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)

        print(f"File '{filename}' received successfully.")
        client_socket.send(b"File received successfully.")
    except Exception as e:
        print(f"Error: {e}")
        client_socket.send(b"File transfer failed.")
    finally:
        client_socket.close()


def audio_broadcast(client_socket):   # audio broadcaster 
    try:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("Broadcasting audio...")

        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            client_socket.sendall(data)

    except Exception as e:
        print(f"Audio error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        client_socket.close()

def start_server():
    server_socket = socket.socket()
    host = 'localhost'
    port = 9999
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"📡 Server started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"🔗 Connected with {addr}")

        option = client_socket.recv(1024).decode()
        if option == 'file':
            threading.Thread(target=handle_file_transfer, args=(client_socket,)).start()
        elif option == 'audio':
            threading.Thread(target=audio_broadcast, args=(client_socket,)).start()
        else:
            print("Unknown option. Closing connection.")
            client_socket.close()

start_server()
