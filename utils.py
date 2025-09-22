import numpy as np
import platform

try:
    import simpleaudio as sa
    SIMPLEAUDIO_AVAILABLE = True
except Exception:
    SIMPLEAUDIO_AVAILABLE = False

def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def eye_aspect_ratio(landmarks, idxs):
    p1, p2, p3, p4, p5, p6 = [np.array(landmarks[i]) for i in idxs]
    A = np.linalg.norm(p2 - p6)
    B = np.linalg.norm(p3 - p5)
    C = np.linalg.norm(p1 - p4)
    return 0.0 if C == 0 else (A + B) / (2.0 * C)

def mouth_aspect_ratio(landmarks, top_idx, bottom_idx, left_idx, right_idx):
    top = np.array(landmarks[top_idx])
    bottom = np.array(landmarks[bottom_idx])
    left = np.array(landmarks[left_idx])
    right = np.array(landmarks[right_idx])
    vertical = np.linalg.norm(top - bottom)
    horizontal = np.linalg.norm(left - right)
    return 0.0 if horizontal == 0 else vertical / horizontal

def drowsiness_probability(ear, mar):
    ear_prob = np.clip((0.35 - ear) / 0.2, 0.0, 1.0)
    mar_prob = np.clip((mar - 0.4) / 0.6, 0.0, 1.0)
    combined = 0.75 * ear_prob + 0.25 * mar_prob
    return float(np.clip(combined, 0.0, 1.0))

def play_beep():
    if platform.system() == "Windows":
        try:
            import winsound
            winsound.Beep(1000, 400)
            return
        except:
            pass
    if SIMPLEAUDIO_AVAILABLE:
        fs = 44100
        duration = 0.2
        t = np.linspace(0, duration, int(fs*duration), False)
        tone = np.sin(440 * 2*np.pi * t)
        audio = (tone * (2**15 - 1) / np.max(np.abs(tone))).astype(np.int16)
        sa.play_buffer(audio, 1, 2, fs)
