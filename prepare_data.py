import openai
import os
import json
import random

APIKey = ""
FineTuneModelID = ""

training_data_ex = {
    "prompt":"Question\n\n###\n\n",
    "completion":"Answer\n"
} #stoppers needed, one for prompt, one for completion

def clean(q,a):
    q = repr(q.replace("\u2019", "'"))
    a = repr(a.replace("\u2019", "'"))
    q = q.strip()
    a = a.strip()
    return q, a

def data_clean():
    with open('./output.jsonl', 'r') as json_file:
        json_list = list(json_file)

    for json_str in json_list:
        result = json.loads(json_str)
        first_pair = next(iter(result.items()))
        question = first_pair[0].replace("https://www.saverlife.org/money-101/", "")
        question = question.replace("-", " ")
        jsonDict = {}
        textInfo = repr(first_pair[1].replace("\n", ""))
        textInfo = repr(textInfo.replace("\u2019", "'"))
        textInfo = textInfo.replace("\"'", "")
        jsonDict["text"] = textInfo
        jsonString = json.dumps(jsonDict)
        with open('./trainData.jsonl', 'a') as f:
            f.write(jsonString + "\n")

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


def train_chatbox(APIKEY, train_file, test_questions, FINE_TUNED_MODEL = None, PROMPT = None, max_rerank = 20, max_tokens = 200):
    # using parameter
    openai.api_key =APIKEY
    # or get from env variable
    #openai.api_key = os.getenv("OPENAI_API_KEY")

    # retrieve existing files
    files = openai.File.list()["data"]
    # clear existing files
    # for f in files:
    #     openai.File.delete(f["id"])

    # uploading scrapped document
    # openai.File.create(file=open(train_file), purpose='answers')
    print(openai.File.list())
    new_file = openai.File.list()["data"][-1]
    FILE_ID = new_file["id"]  # how to get this id?

    # randomly select two examples to query (2 - 3 recommended)
    # or should we use a fixed example-example_context pair
    # example_dicts = random.choices(data, k=2)
    # for e in example_dicts:
    #     #     examples.append([e["prompt"],e["completion"]])

    # Manually chosen examples
    examples = [
       ["Should I defer payments on my bills?" ,"Some companies are offering to let people delay their payments for a little while because of the COVID-19 crisis. This can be a good idea if you really can't pay right now, but you should be careful before you agree to anything. "
    ],
        ["If I receive unemployment insurance, are my benefits taxable?","Unemployment benefits are money that you get from the government when you are not working. They are taxable, which means that the government takes some of the money away. You can choose to have taxes taken out of your unemployment benefits by completing a form called a W-4V. Some states also take taxes out of unemployment benefits. You can also make an estimated tax payment to the IRS quarterly."]
    ]
    example_context = "The pros and cons of deferring payments during the COVID-19 crisis  As you look for help to make ends meet, you may be looking at the increasing amount of creditors offering the ability to delay payments. It's great companies are taking quick action to help with the financial impact of COVID-19. But proceed with caution and consider the following three things before making a decision:   Your financial situation now  Your possible financial situation in the future What happens after the deferral period ends  Your financial situation now  Understandably, if you can't cover your expenses, the only option may be to delay payments. One of the biggest mistakes I saw people making during the last recession was not quickly reducing their spending. Start cutting non-essential expenses: cable, your cellphone package, etc.  The other mistake I saw people making was not calling creditors before the first missed payment. Creditors are far more likely to work with you if you call them  before  you miss a payment. Explain to your creditors how you are impacted by COVID-19 and ask for COVID-19 hardships programs. Most creditors and lenders have hardship programs, but programs specific to COVID-19 may be better. Ask about:  The effects on your credit score (ideally none) when you delay payments How long you can defer (creditors may extend deferrals if COVID-19 continues to spread) What happens once your start repayment  Your financial situation in the future   Even if you can pay your expenses, it may make sense to defer your payments. If you are paying expenses through savings and are facing a layoff or have little in savings, carefully consider accepting options to delay payments. Delaying payments frees up cash so you can save money. As mentioned before, ask about programs specifically for those impacted by COVID-19.  Is it worth it?  All payment deferrals will impact you. The key is understanding the impact and deciding if it's worth it.  The ability to miss payments is not free money. You will have to pay it back. How you pay it back depends on your creditors. Contact your creditors and ask what happens after the missed payment period ends. The COVID-19 crisis changes the rules, but in general, there are typically four possibilities that can occur once your deferral period is over:  Your creditors add your missed payments to the end of your payment period. So if you missed three payments, your total payment period would be three months longer. Your loan is modified. This can mean a higher interest rate or an extended payment period. You temporarily pay a higher amount. This higher amount is your regular payment plus a portion of the payments you missed until you have “paid off” your missed payments.  Your creditor may ask for the total missed payments to be paid in full once your deferral period ends.  The last thing you want is to find yourself in a worse financial position because you accepted an offer to defer payments without knowing the consequences after your deferral period ends. Get all the facts so you can make an informed decision.  "

    outfile = open("output_full_"+str(max_rerank)+"_"+str(max_tokens)+".txt", "a")
    # query answers
    for question in test_questions:
        print(question)
        answer = openai.Answer.create(
            search_model="ada",
            model="curie",
            question= question,
            file=FILE_ID,
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
        # first_answer = answer["answers"][0]
        # print(first_answer)
        # outfile.write(question+": "+first_answer+"\n")


if __name__ == '__main__':
    # q,a = clean("If I receive unemployment insurance, are my benefits taxable?", "Unemployment benefits are taxable income. They are subject to federal and state taxes (if your state taxes income). You can choose to withhold 10% in federal taxes from your benefits by completing a  W-4V  and giving the form to your unemployment office. Some states automatically withhold taxes; some states do not. Go to your state\u2019s unemployment website to learn how they handle state taxes. You can also make an  estimated tax payment  to the IRS quarterly. Your state agency will give you a  1099-G  that will report unemployment income and taxes paid on your unemployment income.   Everyone\u2019s tax situation is different. But the rule of thumb is to have taxes withheld now, so it\u2019s taken out in small chunks. Otherwise, you may have to make a large tax payment next year. ")
    # print(q)
    # print(a)

    test_data = prepare_test('testData.json')
    test_questions = list(test_data.keys())
    #print(len(test_questions), test_questions[0])
    #for rerank in range(10, 35, 5):
    train_chatbox(APIKEY = APIKey, train_file = "trainData.jsonl",test_questions = test_questions, max_rerank = 20, max_tokens = 200)
