
import socket
import os
import pyaudio


def receive_audio(client_socket):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True, frames_per_buffer=CHUNK)

    print("Receiving audio. Press Ctrl+C to stop.")

    try:
        while True:
            data = client_socket.recv(CHUNK)
            stream.write(data)
    except KeyboardInterrupt:
        print("Audio stream stopped by user.")
    except Exception as e:
        print(f"Audio error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        client_socket.close()


def send_file(client_socket):
    file_path = input("Enter full path of file to send: ")
    if not os.path.isfile(file_path):
        print("File not found.")
        client_socket.close()
        return

    filename = os.path.basename(file_path)
    client_socket.send(filename.encode())

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            client_socket.send(data)
    client_socket.shutdown(socket.SHUT_WR)  # Tells server we're done sending


    print("File sent. Waiting for server response...")
    print(client_socket.recv(1024).decode())
    client_socket.close()


def start_client():
    client_socket = socket.socket()
    host = 'localhost'
    port = 9999

    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f" Connection failed: {e}")
        return

    mode = input("Enter mode ('file' or 'audio'): ").strip().lower()
    client_socket.send(mode.encode())

    if mode == 'file':
        send_file(client_socket)
    elif mode == 'audio':
        receive_audio(client_socket)
    else:
        print("Invalid mode.")
        client_socket.close()

start_client()
