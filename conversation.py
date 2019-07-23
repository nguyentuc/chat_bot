#!/usr/bin/python3
import os
import aiml

BRAIN_FILE = "brain.dump"
k = aiml.Kernel()
if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    k.bootstrap(learnFiles="learningFileList.aiml", commands="LEARN AIML")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)
while True:
    input_text = raw_input("USER > ")
    response = k.respond(input_text)
    print(response)

# conversation.py : code for loading and running the bot
# learningFilesList.aiml : code load files to train
# folder data: contains all the AIML files and each aiml file contains the conversation patterns which kernel will load for chatting
# Kernel object is the public interface to the AIML interpreter.
# learn method loads the contents of an AIML file into the kernel.
# respond method is used to get the response from the learned AIML file.
# And "LEARN AIML" is the pattern that k.respond from conversation.py calls. The tag loads the AIML file to respond
