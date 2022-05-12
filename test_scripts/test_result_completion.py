import openai
import os
import json
import sys

# for generating test outputs called by finetune.sh
# Command to execute this file :
# python test_result_completion.py ${OPENAI_API_KEY} testData.json output_curie_10.txt [fine-tune-model-name] 0 200
# python test_result_completion.py ${OPENAI_API_KEY} testData.json output_curie_20.txt [fine-tune-model-name] 0 200
# python test_result_completion.py ${OPENAI_API_KEY} testData.json output_curie_50.txt [fine-tune-model-name] 0.5 200
# python test_result_completion.py ${OPENAI_API_KEY} testData.json output_curie_100.txt [fine-tune-model-name] 0 200
# python test_result_completion.py ${OPENAI_API_KEY} testData.json output_curie_200.txt [fine-tune-model-name] 0 200

#Generate output for davinci
# python test_result_completion.py ${OPENAI_API_KEY} testData.json output_davinci_50.txt [fine-tune-model-name] 0 200
# python test_result_completion.py ${OPENAI_API_KEY} testData.json output_davinci_100.txt [fine-tune-model-name] 0 200

def prepare_test(test_json):
    clean_test_data = dict()
    with open(test_json) as json_file:
        test_data = json.load(json_file)
    for k, v in test_data.items():
        k = repr(k.replace("\u2019", "'"))
        k = k.strip()
        v = repr(v.replace("\u2019", "'"))
        v = v.strip()
        clean_test_data[k] = v
    return clean_test_data

def train_chatbox(APIKEY, test_file, out_file, finetune_model, temperature = 0, max_tokens = 200):
    # using parameter
    openai.api_key =APIKEY

    # prepare test questions
    test_data = prepare_test(test_file)
    test_questions = list(test_data.keys())

    outfile = open(out_file, "a")

    # query answers
    for question in test_questions:
      answer = openai.Completion.create(
            model=finetune_model,
            prompt= question,
            temperature= temperature,
            max_tokens= max_tokens,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n", "<|endoftext|>"]
        )
      outfile.write(question+": ")
      outfile.write("\n")
      outfile.write(answer+" ")
      outfile.write("\n")


if __name__ == '__main__':

    MAX_RERANK = 20
    MAX_TOKENS = 200

    s = f"""
    {'-' * 40}
    # Example to use test_result_completion.py
    # python test_result_completion [OPENAI_APIKEY] [TEST_FILE_PATH] [OUTPUT_FILE_PATH] [FINETUNE_MODEL_ID] [TEMPERATURE]* [MAX_TOKENS]*
    {'-' * 40}
    """
    #if len(sys.argv) < 5:
        #sys.exit(s)
    #if len(sys.argv) >= 7:
        #MAX_RERANK = sys.argv[6]
    #if len(sys.argv) >= 8:
        #MAX_TOKENS = sys.argv[7]


    train_chatbox(APIKEY = sys.argv[1],
                  test_file = sys.argv[2],
                  out_file= sys.argv[3],
                  finetune_model = sys.argv[4],
                  temperature = sys.argv[5],
                  max_tokens = sys.argv[6])
