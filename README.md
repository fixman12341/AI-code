Hello this is my quick draw ai that I made for my nvdia camp.
It is a classification ai that looks at what you draw and tells what it is
I use the quick draw data from google quick draw to train my ai.
The data making turns the ndjson file that are strokes into a jpg so I can train the ai with it.
The data link is: https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/simplified;tab=objects?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false
The game itself uses a two point line system to make it look smoother.
The controls are space to move on and hold down to start drawing
When the time hits 0 or you press space it moves and then it sends to the ai code and predicts it
If the random image and what the ai thinks you drew you're score goes up and time gets halfed, if not it resets and time gets set back to a minute.
