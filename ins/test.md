---
# - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Default Configuration
# - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# !!!
#
# DO NOT DELETE
# INTEGRAL TO THE SOFTWARE

# SFZ file formatting
sfz:
  name: SFZ Instrument
  use linebreak: true
  curve: None
  
  symbols:
    space: " "
    linebreak: "\n"
    comment:
      line: "- - - - - - - - - - - - - - - - - - - - -"
      subline: "* * * * * * * * * * * * * * * * *"

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Insert Text
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

insert:
  pre:
  post:

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Control Section
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# * * * * * * * * * * * * * * *
# Default Controls
control:
  # ::: Listed :::
  Velocity:
    cc: 131
    default: 0
    hide: true
  Release Velocity:
    cc: 132
    default: 0
    hide: true
  Channel AT:
    cc: 129
    default: 0
  Volume:
    cc: 7
    default: 127
  Pan:
    cc: 10
    default: 64
  Pitchbend:
    cc: 128
    default: 0
  # ::: Unlisted (SFZ2) :::
  Poly AT:
    cc: 130
    default: 0
    hide: True
  Note:
    cc: 133
    hide: true
  Gate:
    cc: 134
    hide: true
  Random Unipolar:
    cc: 135
    hide: true
  Random Bipolar:
    cc: 136
    hide: true
  Alternate:
    cc: 137
    hide: true
  # ::: Unlisted (ARIA) :::
  Keydelta:
    cc: 140
    hide: True
  Keydelta ABS:
    cc: 141
    hide: True
  Host BPM:
    cc: 142
    hide: True
  Host Transport:
    cc: 143
    hide: True
  Host Samplerate:
    cc: 144
    hide: True
  Time Engine:
    cc: 145
    hide: True
  Timesig A:
    cc: 146
    hide: True
  Timesig B:
    cc: 147
    hide: True
  QN Position ABS:
    cc: 148
    hide: True
  QN Position:
    cc: 149
    hide: True
  Time Instrument:
    cc: 150
    hide: True
  Time LastKeyOn:
    cc: 151
    hide: True
  Time LastKeyOff:
    cc: 152
    hide: True
  Keycount:
    cc: 153
    hide: True
  Voicecount:
    cc: 154
    hide: True
  Offset:
    cc: 155
    hide: True

# * * * * * * * * * * * * * * *
# Control Element

control element:
  cc: 0
  default: 0
  hide: false

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Equalizers
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# * * * * * * * * * * * * * * *
# Equalizer Section

equalizers:
  3Band:
    dynamic: true
    bands:
      - [0, 1, 2]
      - [200, 20, 2]
  

# * * * * * * * * * * * * * * *
# Equalizer Element

equalizer element:
  dynamic: false
  bands:

# * * * * * * * * * * * * * * *
# Part Equalizer Element

part equalizer element:
  modulation:
    band 1:
      frequency:
        cc:
        variables:
      bandwidth:
        cc:
        variables:
      gain:
        cc:
        variables:
    band 2:
      frequency:
        cc:
        variables:
      bandwidth:
        cc:
        variables:
      gain:
        cc:
        variables:
    band 3:
      frequency:
        cc:
        variables:
      bandwidth:
        cc:
        variables:
      gain:
        cc:
        variables:
        

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Filters
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# * * * * * * * * * * * * * * *
# Filter Section

filters:
  Lowpass:
    type: lowpass
    poles: 2
    frequency: 100
  Highpass:
    type: highpass
    poles: 2
    frequency: 500

# * * * * * * * * * * * * * * *
# Filter Element

filter element:
  type: lowpass
  poles: 1
  frequency: 9600
  resonance: 0
  gain: 0
  key tracking: 0
  key tracking center: 64
  velocity tracking: 0

# * * * * * * * * * * * * * * *
# Part Filter Element

part filter element:
  modulation:
    frequency:
      cc:
      variables:
    resonance:
      cc:
      variables:
    gain:
      cc:
      variables:

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Release Envelopes
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# * * * * * * * * * * * * * * *
# Envelopes

release envelopes:
  Normal:
    points:
      - [0, 1]

# * * * * * * * * * * * * * * *
# Release Envelope Element

release envelope element:
  points:

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Modulation
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# * * * * * * * * * * * * * * *
# Modulation Element

modulation element:
  depth: 0
  curve:
  compensate: 0

# * * * * * * * * * * * * * * *
# Modulation Envelope Element

modulation envelope element:
  levels:
  times:

# * * * * * * * * * * * * * * *
# Adsr Modulation Element

modulation adsr element:
  depth: 0
  curve:
  compensate: 0

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Variables
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

variables:
  modulation:
  type: mult

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Amp EG
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

amp eg:
  dynamic: false
  delay:
    level: 0
    modulation:
      cc:
  attack:
    level: 0.01
    shape: 0
    modulation:
      cc:
  hold:
    level: 0
    modulation:
      cc:
  decay:
    level: 0.01
    shape: 0
    modulation:
      cc:
  sustain:
    level: 1
  release:
    level: 0.01
    shape: 0
    modulation:
      cc:

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Envelopes
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

envelopes:
  sustain:
  points: None

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Curves
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

curve element:
  resolution: 1
  points: None # [level, position, exponent]

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Choke
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

choke:
  group:
  off by:
  time:
  shape:

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Attributes
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

attributes:
  level: 0
  modulation:
    velocity:
      depth: 0
    cc:
      1:
        depth: 0
    envelopes:
    variables:

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Range Element
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

range element:
  low: 0
  high: 127

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Keyswitch Element
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

keyswitch element:
  label: Keyswitch
  program: 
  note: 


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# SFZ Structure
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# * * * * * * * * * * * * * * *
# Instruments

instruments:
  control:
  envelopes:
  variables:
  release envelopes:
  filters:
  equalizers:
  velocity tracking: 0
  choke:
  

# * * * * * * * * * * * * * * *
# Parts

parts:
  trigger: Normal
  playmode: Normal
  keyswitch:
  zones:
  splits:
  samples:
  sounds:
  choke:
  filters:
  amp eg:
  equalizer:
  hide: false
  roundrobin: sequence # random, hybrid
  
  cc range:
  program range:
    
  keyrange:
    low: 0
    high: 127
    force note:
    extend:
      low: 0
      high: 0

# * * * * * * * * * * * * * * *
# Zones

zones:
  note detection: 
    type: array # direct
    pattern: classic-b-sharp
  
  crossfade:
    depth: 1
    type: power

# * * * * * * * * * * * * * * *
# Splits

splits:
  pattern: null
  curve: 1.0
  crossfade:
    depth: 1.0
    type: power
    control:
      type: velocity
      index: 0

# * * * * * * * * * * * * * * *
# Samples

samples:
  location: Samples
  include: "*"
  exclude: ""
  split: _
  pattern: [name, note, level, roundrobin]
  note: None
  mapping:
    type: tonal # atonal
    note:
      step: 12
      start: 36

# * * * * * * * * * * * * * * *
# Sounds

sounds:
  pitch tracking: 100
