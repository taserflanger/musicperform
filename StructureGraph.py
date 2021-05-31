# %%
from typing import List

from music21 import note
from music21.stream import Stream

from Style import Style
from structurer_utils import find_structures


class Graph(object):
    """
    The nodes are tuples indicating beginning and ending of a sequence
    """

    def __init__(self, file: Stream):
        self.midi_notes = []
        notes = []
        durations = []
        notes_with_duration = []
        for element in file.recurse():
            if isinstance(element, note.Note):
                self.midi_notes.append(element)
                notes.append(element.nameWithOctave)
                durations.append(element.duration)
                notes_with_duration.append(element.nameWithOctave + str(element.duration))

        self.note_patterns, self.note_indices = find_structures(notes, threshold=6)
        self.duration_patterns, self.duration_indices = find_structures(durations, threshold=20)
        self.notes_with_duration_patterns, self.notes_with_duration_indices = find_structures(notes_with_duration)

        frequencies = [n.pitch.frequency for n in self.midi_notes]
        self.nodes = [Node(0, len(self.midi_notes)-1)]
        self.root = self.nodes[0]


class Node(object):
    def __init__(self, beginning: int, end: int, styles: List[Style] = None, children=None, parents=None):
        if styles is None:
            styles = []
        if children is None:
            children = []
        if parents is None:
            parents = []
        self.styles = styles
        self.beginning = beginning
        self.end = end
        self.children = children
        self.parents = parents

    def add_parents(self, *parents):
        for p in parents:
            self.parents.append(p)

    def add_children(self, *children):
        for c in children:
            self.children.append(c)


