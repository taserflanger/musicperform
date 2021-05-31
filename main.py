#%%
from structurer_utils import find_structures
from music21 import converter,note # or import *
file = converter.parse('beethoven_fur_elise.mid')
midi_notes = []
notes = []
duration = []
notes_with_duration = []
for element in file.recurse():
    if isinstance(element, note.Note):
        midi_notes.append(element)
        notes.append(element.nameWithOctave)
        duration.append(element.duration)
        notes_with_duration.append(element.nameWithOctave + str(element.duration))


note_patterns, note_indices = find_structures(notes, threshold=6)
duration_patterns, duration_indices = find_structures(duration, threshold=20)
notes_with_duration_patterns, notes_with_duration_indices = find_structures(notes_with_duration)


#%%
import numpy as np
def cov(x1: np.ndarray, x2:np.ndarray):
    # pour calculer si les notes de 2 séquences rythmiques évoluent ensemble ou de manière opposée
    # entrée: 2 listes de notes sous forme de fréquence (de même longueur)
    # sortie: covariance des variables discrètes normalisées dont la distribution est cette liste
    x1 = (x1 - x1.mean())/x1.std()
    x2 = (x2 - x2.mean())/x2.std()
    return np.cov(x1, x2)[0][1]



