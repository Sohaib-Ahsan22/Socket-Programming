# Socket-Programming
Socket Programming Project
Objective
Implement a socket-based system in Python that:

Transfers files from client to server

Optionally streams real-time audio from server to client (bonus)

Technologies Used
  Python 3
  Socket module
  pyaudio for real-time audio

📁 File Structure
project/
│
├── server.py       # Server to receive files and broadcast audio
├── client.py       # Client to send files or receive audio
└── README.md       # How to run + explanation
🔧 Setup Instructions
Step 1: Install Required Packages
pip install pyaudio
If on Windows, install using .whl if pip install fails.

How to Run"
  Start the Server
  python server.py
  Start the Client
  python client.py
Then choose one of the modes:

📂 File Transfer Mode
Type file when prompted.

Enter full path of the file you want to send.

🔊 Audio Streaming Mode
Type audio when prompted.

You will start hearing the live audio from the server’s microphone.

📦 Features
Feature	Description
File Transfer	Send large files reliably to server
Real-time Audio	Bonus: Live mic audio from server
Error Handling	Handles missing files, bad input
Multi-threaded Server	Handles multiple clients in parallel
