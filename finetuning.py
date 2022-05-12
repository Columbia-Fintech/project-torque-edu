#Fine tuning - file setup commands
#openai tools fine_tunes.prepare_data -f <LOCAL_FILE>
#openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL>

import openai
openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt="How to Apply for SNAP Benefits")