import whisper


def speech_recognition(audio_fname: str, model='base'):
    speech_model = whisper.load_model(model)
    result = speech_model.transcribe(f'{audio_fname}')

    return result['text']
