from pathlib import Path
from pydub import AudioSegment
from whispercpp import Whisper

def convert_mp3_to_wav(mp3_path: Path, wav_path: Path) -> Path:
    """
    Converts an MP3 file to WAV format.
    
    Args:
        mp3_path (Path): Path to the input MP3 file.
        wav_path (Path): Path to save the output WAV file.
    
    Returns:
        Path: Path to the converted WAV file.
    """
    print(f"Converting {mp3_path} to WAV format")
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")
        print(f"Conversion successful: {wav_path}")
        return wav_path
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise

def transcribe_audio(wav_path: Path, model_type: str = 'tiny') -> str:
    """
    Transcribes a WAV audio file using Whisper.
    
    Args:
        wav_path (Path): Path to the WAV file.
        model_type (str): Whisper model type (default: 'tiny').
    
    Returns:
        str: Transcribed text.
    """
    print(f"Transcribing {wav_path}")
    try:
        w = Whisper(model_type)
        result = w.transcribe(str(wav_path))  # Ensure path is passed as a string
        text = w.extract_text(result)
        podcast_transcript = ''.join(text)
        print("Transcription completed successfully")
        return podcast_transcript
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise

def transcribe_podcast_episode(episode_path: Path, model_type: str = 'tiny') -> str:
    """
    Transcribes a podcast episode from MP3 to text.
    
    Args:
        episode_path (Path): Path to the MP3 file.
        model_type (str): Whisper model type (default: 'tiny').
    
    Returns:
        str: Transcribed text.
    """
    # Convert MP3 to WAV
    wav_path = episode_path.with_suffix('.wav')
    convert_mp3_to_wav(episode_path, wav_path)
    
    # Transcribe the WAV file
    transcript = transcribe_audio(wav_path, model_type)
    return transcript
