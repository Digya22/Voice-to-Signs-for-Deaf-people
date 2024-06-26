import json

from fastapi.responses import StreamingResponse
from moviepy.editor import VideoFileClip, concatenate_videoclips
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from os import path

videos = path.join("videos")
final = path.join("final.mp4")
data = path.join("data1.json")

with open(data, "r") as file:
    predefined_tokens = json.load(file)


def english_to_tokens(text, predefined_tokens=predefined_tokens):
    # Tokenize the input English text
    words = word_tokenize(text.lower())
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    print(stemmed_words)

    # Map each word to its corresponding token
    tokens = []
    words = []
    for word in stemmed_words:
        if word in predefined_tokens:
            tokens.append(predefined_tokens[word])
            words.append(word)
        else:
            continue

    print(stemmed_words, tokens)

    return {"tokens": tokens}


def get_video_path(tokens):
    if not isinstance(tokens, list):
        return path.join(videos, str(tokens[0])+".mp4")
    return [path.join(videos, str(token)+".mp4")for token in tokens]


def stream_video(paths):
    path: str
    if not isinstance(paths, list):
        path = paths[0]
    else:
        concatenate_videos(paths)
        path = final
    try:

        def iterfile():
            with open(path, "rb") as f:
                yield from f

        return StreamingResponse(iterfile(), media_type="video/mp4")
    except:
        return {"message": "File not found"}


def concatenate_videos(paths):
    clips = [VideoFileClip(path) for path in paths]

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(final)
