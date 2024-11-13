#!/usr/bin/env python3

""" transposer.py at 

git commit -m"v001 new :transposer.py"

Before running this program:
pip install pyqt6
chmod +x transposer.py
./transposer.py

Based on perplexity.ai to write a python program with qt to transcribe different instrument keys to other keys
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

class KeyTranscriber(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Instrument Key Transcriber')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Input section
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('Input Notes:'))
        self.input_notes = QLineEdit()
        input_layout.addWidget(self.input_notes)
        layout.addLayout(input_layout)

        # Key selection
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel('From Key:'))
        self.from_key = QComboBox()
        key_layout.addWidget(self.from_key)
        key_layout.addWidget(QLabel('To Key:'))
        self.to_key = QComboBox()
        key_layout.addWidget(self.to_key)
        layout.addLayout(key_layout)

        # Populate key options
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.from_key.addItems(keys)
        self.to_key.addItems(keys)

        # Transcribe button
        self.transcribe_btn = QPushButton('Transcribe')
        self.transcribe_btn.clicked.connect(self.transcribe)
        layout.addWidget(self.transcribe_btn)

        # Output section
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel('Transcribed Notes:'))
        self.output_notes = QLineEdit()
        self.output_notes.setReadOnly(True)
        output_layout.addWidget(self.output_notes)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def transcribe(self):
        input_notes = self.input_notes.text().upper().split()
        from_key = self.from_key.currentText()
        to_key = self.to_key.currentText()

        # Define the chromatic scale
        chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        # Calculate the interval between keys
        from_index = chromatic_scale.index(from_key)
        to_index = chromatic_scale.index(to_key)
        interval = (to_index - from_index) % 12

        # Transcribe notes
        transcribed_notes = []
        for note in input_notes:
            if note in chromatic_scale:
                new_index = (chromatic_scale.index(note) + interval) % 12
                transcribed_notes.append(chromatic_scale[new_index])
            else:
                transcribed_notes.append(note)

        self.output_notes.setText(' '.join(transcribed_notes))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KeyTranscriber()
    ex.show()
    sys.exit(app.exec_())