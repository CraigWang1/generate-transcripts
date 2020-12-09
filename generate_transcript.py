import time
from youtube_transcript_api import YouTubeTranscriptApi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def generate_transcript(url):
    # Get the transcript
    video_id = extract_video_id(url)
    print("Getting transcript")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_string = ""
    for line in transcript:
        transcript_string += line['text'] + " "

    # Add punctuation to transcript"""
    transcript_string = punctuate(transcript_string)

    f = open("transcript.txt", "w+")
    f.write(transcript_string)
    f.close()

    print("Transcript saved at ./transcript.txt")

def extract_video_id(url):
    """ Get video id from url"""
    print("Extracting video url")
    return url[32:]

def punctuate(text):
    # Split string in half because punctuate website can't handle too many words
    split_idx = int(len(text) / 2)
    if text[split_idx] != " ":
        while True:
            split_idx += 1
            if text[split_idx] == " ":
                is_whitespace = True
                break
    chunks = []
    chunks.append(text[:split_idx])
    chunks.append(text[split_idx:])

    punctuated_text = ""

    # Access the punctuate website to add punctuation
    print("Opening browser")
    opts = Options()
    opts.require_window_focus = True
    opts.headless = True
    driver = webdriver.Firefox(executable_path="./geckodriver", options=opts)
    driver.get("http://bark.phon.ioc.ee/punctuator")

    for i in range(len(chunks)):
        print("Inputting raw chunk {}".format(i))
        driver.execute_script('document.getElementById("input-text").value="' + chunks[i] + '"')

        print("Submitting raw text {}".format(i))
        submit_button = driver.find_element_by_id("punctuate-btn")
        submit_button.click()
        time.sleep(5)

        print("Extracting punctuated text {}".format(i))
        complete = False
        prev = 0
        while complete == False:
            output = driver.find_element_by_id("output-text")
            now = len(output.text)
            if output.text == None or now > prev:
                time.sleep(1)
                prev = now
            else:
                complete = True
                punctuated_text += output.text
    driver.close()
    return punctuated_text
  
if __name__ == '__main__': 
            
    url = input('Enter the youtube url: ') 

    print('')  
    
    generate_transcript(url) 
