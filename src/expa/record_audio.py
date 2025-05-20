import audioop
import pyaudio
import wave
import os

output_dir = '.'

def record_audio_vad(filename="request.wav", silence_threshold=1000, silence_duration=3, max_record_time=30):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Full path for output file
    filepath = os.path.join(output_dir, filename)

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    input=True,
                    frames_per_buffer=chunk)

    print("Listening... (speak now)")

    frames = []
    silent_chunks = 0
    silence_chunk_limit = int(fs / chunk * silence_duration)
    max_chunks = int(fs / chunk * max_record_time)

    for i in range(max_chunks):
        data = stream.read(chunk)
        frames.append(data)
        
        rms = audioop.rms(data, 2)  # Calculate volume (root mean square)
        if rms < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > silence_chunk_limit:
            print("Silence detected, stopping...")
            break

    print("Recording complete.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename
