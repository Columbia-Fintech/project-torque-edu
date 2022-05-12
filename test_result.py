import openai
import os
import json
import sys

# for generating test outputs called by finetune.sh

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

def train_chatbox(APIKEY, train_file_id, test_file, out_file, finetune_model, max_rerank = 20, max_tokens = 200):
    # using parameter
    openai.api_key =APIKEY

    # retrieve existing files
    files = openai.File.list()["data"]

    ## if trainData.json is not uploaded yet, uncomment line 28-31
    # upload trainData.json
    # openai.File.create(file=open('trainData.jsonl'), purpose='answers')
    # print(openai.File.list())
    # sys.exit("waiting for file to process")
    ## if the file is ready
    # new_file = openai.File.list()["data"][-1]
    # file_id = new_file["id"]


    # Manually chosen examples
    examples = [
       ["Should I defer payments on my bills?" ,"Some companies are offering to let people delay their payments for a little while because of the COVID-19 crisis. This can be a good idea if you really can't pay right now, but you should be careful before you agree to anything. "
    ],
        ["If I receive unemployment insurance, are my benefits taxable?","Unemployment benefits are money that you get from the government when you are not working. They are taxable, which means that the government takes some of the money away. You can choose to have taxes taken out of your unemployment benefits by completing a form called a W-4V. Some states also take taxes out of unemployment benefits. You can also make an estimated tax payment to the IRS quarterly."]
    ]
    example_context = "The pros and cons of deferring payments during the COVID-19 crisis  As you look for help to make ends meet, you may be looking at the increasing amount of creditors offering the ability to delay payments. It's great companies are taking quick action to help with the financial impact of COVID-19. But proceed with caution and consider the following three things before making a decision:   Your financial situation now  Your possible financial situation in the future What happens after the deferral period ends  Your financial situation now  Understandably, if you can't cover your expenses, the only option may be to delay payments. One of the biggest mistakes I saw people making during the last recession was not quickly reducing their spending. Start cutting non-essential expenses: cable, your cellphone package, etc.  The other mistake I saw people making was not calling creditors before the first missed payment. Creditors are far more likely to work with you if you call them  before  you miss a payment. Explain to your creditors how you are impacted by COVID-19 and ask for COVID-19 hardships programs. Most creditors and lenders have hardship programs, but programs specific to COVID-19 may be better. Ask about:  The effects on your credit score (ideally none) when you delay payments How long you can defer (creditors may extend deferrals if COVID-19 continues to spread) What happens once your start repayment  Your financial situation in the future   Even if you can pay your expenses, it may make sense to defer your payments. If you are paying expenses through savings and are facing a layoff or have little in savings, carefully consider accepting options to delay payments. Delaying payments frees up cash so you can save money. As mentioned before, ask about programs specifically for those impacted by COVID-19.  Is it worth it?  All payment deferrals will impact you. The key is understanding the impact and deciding if it's worth it.  The ability to miss payments is not free money. You will have to pay it back. How you pay it back depends on your creditors. Contact your creditors and ask what happens after the missed payment period ends. The COVID-19 crisis changes the rules, but in general, there are typically four possibilities that can occur once your deferral period is over:  Your creditors add your missed payments to the end of your payment period. So if you missed three payments, your total payment period would be three months longer. Your loan is modified. This can mean a higher interest rate or an extended payment period. You temporarily pay a higher amount. This higher amount is your regular payment plus a portion of the payments you missed until you have “paid off” your missed payments.  Your creditor may ask for the total missed payments to be paid in full once your deferral period ends.  The last thing you want is to find yourself in a worse financial position because you accepted an offer to defer payments without knowing the consequences after your deferral period ends. Get all the facts so you can make an informed decision.  "

    # prepare test questions
    test_data = prepare_test(test_file)
    test_questions = list(test_data.keys())

    outfile = open(out_file, "a")

    # query answers
    for question in test_questions:
        answer = openai.Answer.create(
            model=finetune_model,
            question= question,
            file=train_file_id,
            examples_context=example_context,
            examples=examples,
            max_rerank=max_rerank,
            max_tokens=max_tokens,
            stop=["\n", "<|endoftext|>"]
        )
        outfile.write(question+": ")
        for a in answer["answers"]:
            outfile.write(a+" ")
        outfile.write("\n")


if __name__ == '__main__':

    MAX_RERANK = 20
    MAX_TOKENS = 200

    s = f"""
    {'-' * 40}
    # Example to use test_result.py
    # python test_result.py [OPENAI_APIKEY] [TRAIN_FILE_PATH] [TEST_FILE_PATH] [OUTPUT_FILE_PATH] [FINETUNE_MODEL_ID] [MAX_RERANK]* [MAX_TOKENS]*
    {'-' * 40}
    """
    if len(sys.argv) < 6:
        sys.exit(s)
    if len(sys.argv) >= 7:
        MAX_RERANK = sys.argv[6]
    if len(sys.argv) >= 8:
        MAX_TOKENS = sys.argv[7]


    train_chatbox(APIKEY = sys.argv[1],
                  train_file = sys.argv[2],
                  test_file = sys.argv[3],
                  out_file= sys.argv[4],
                  finetune_model = sys.argv[5],
                  max_rerank = MAX_RERANK,
                  max_tokens = MAX_TOKENS)
