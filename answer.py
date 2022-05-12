import openai
import os
import json

# for single answer called by server.py

APIKey = ""

def truncate_answer(answer):
    last_period = answer.rfind('.')
    if last_period >= 0:
        # not none
        return answer[:last_period+1]

def generate_completion_simple(query, max_tokens, temperature):
    openai.api_key = APIKey
    outstr = ""
    res = openai.Completion.create(
        model="curie",
        prompt=query,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=["\n", "<|endoftext|>"],
    )
    outstr = res['choices'][0]['text']
    return truncate_answer(outstr)


def generate_answer_simple(question, max_rerank=25, max_tokens=300):
    openai.api_key = APIKey

    new_file = openai.File.list()["data"][-1]
    FILE_ID = new_file["id"]

    outstr=""

    examples = [
        ["Should I defer payments on my bills?",
         "Some companies are offering to let people delay their payments for a little while because of the COVID-19 crisis. This can be a good idea if you really can't pay right now, but you should be careful before you agree to anything. "
         ],
        ["If I receive unemployment insurance, are my benefits taxable?",
         "Unemployment benefits are money that you get from the government when you are not working. They are taxable, which means that the government takes some of the money away. You can choose to have taxes taken out of your unemployment benefits by completing a form called a W-4V. Some states also take taxes out of unemployment benefits. You can also make an estimated tax payment to the IRS quarterly."]
    ]
    example_context = "The pros and cons of deferring payments during the COVID-19 crisis  As you look for help to make ends meet, you may be looking at the increasing amount of creditors offering the ability to delay payments. It's great companies are taking quick action to help with the financial impact of COVID-19. But proceed with caution and consider the following three things before making a decision:   Your financial situation now  Your possible financial situation in the future What happens after the deferral period ends  Your financial situation now  Understandably, if you can't cover your expenses, the only option may be to delay payments. One of the biggest mistakes I saw people making during the last recession was not quickly reducing their spending. Start cutting non-essential expenses: cable, your cellphone package, etc.  The other mistake I saw people making was not calling creditors before the first missed payment. Creditors are far more likely to work with you if you call them  before  you miss a payment. Explain to your creditors how you are impacted by COVID-19 and ask for COVID-19 hardships programs. Most creditors and lenders have hardship programs, but programs specific to COVID-19 may be better. Ask about:  The effects on your credit score (ideally none) when you delay payments How long you can defer (creditors may extend deferrals if COVID-19 continues to spread) What happens once your start repayment  Your financial situation in the future   Even if you can pay your expenses, it may make sense to defer your payments. If you are paying expenses through savings and are facing a layoff or have little in savings, carefully consider accepting options to delay payments. Delaying payments frees up cash so you can save money. As mentioned before, ask about programs specifically for those impacted by COVID-19.  Is it worth it?  All payment deferrals will impact you. The key is understanding the impact and deciding if it's worth it.  The ability to miss payments is not free money. You will have to pay it back. How you pay it back depends on your creditors. Contact your creditors and ask what happens after the missed payment period ends. The COVID-19 crisis changes the rules, but in general, there are typically four possibilities that can occur once your deferral period is over:  Your creditors add your missed payments to the end of your payment period. So if you missed three payments, your total payment period would be three months longer. Your loan is modified. This can mean a higher interest rate or an extended payment period. You temporarily pay a higher amount. This higher amount is your regular payment plus a portion of the payments you missed until you have “paid off” your missed payments.  Your creditor may ask for the total missed payments to be paid in full once your deferral period ends.  The last thing you want is to find yourself in a worse financial position because you accepted an offer to defer payments without knowing the consequences after your deferral period ends. Get all the facts so you can make an informed decision.  "

    answer = openai.Answer.create(
        search_model="ada",
        model="curie",
        question=question,
        file=FILE_ID,
        examples_context=example_context,
        examples=examples,
        max_rerank=max_rerank,
        max_tokens=max_tokens,
        stop=["\n", "<|endoftext|>"]
    )
    for a in answer['answers']:
        outstr += a + " "

    return truncate_answer(outstr)

def generate_answer(question, api_key = None, fine_tune_model = None, train_file_id = None, max_rerank = 25, max_tokens = 300):
    outstr = ""
    if fine_tune_model is None:
        fine_tune_model = 'curie'
    if api_key is None:
        api_key = APIKey
    if train_file_id is None:
        new_file = openai.File.list()["data"][-1]
        train_file_id = new_file['id']
    examples = [
        ["Should I defer payments on my bills?",
         "Some companies are offering to let people delay their payments for a little while because of the COVID-19 crisis. This can be a good idea if you really can't pay right now, but you should be careful before you agree to anything. "
         ],
        ["If I receive unemployment insurance, are my benefits taxable?",
         "Unemployment benefits are money that you get from the government when you are not working. They are taxable, which means that the government takes some of the money away. You can choose to have taxes taken out of your unemployment benefits by completing a form called a W-4V. Some states also take taxes out of unemployment benefits. You can also make an estimated tax payment to the IRS quarterly."]
    ]
    example_context = "The pros and cons of deferring payments during the COVID-19 crisis  As you look for help to make ends meet, you may be looking at the increasing amount of creditors offering the ability to delay payments. It's great companies are taking quick action to help with the financial impact of COVID-19. But proceed with caution and consider the following three things before making a decision:   Your financial situation now  Your possible financial situation in the future What happens after the deferral period ends  Your financial situation now  Understandably, if you can't cover your expenses, the only option may be to delay payments. One of the biggest mistakes I saw people making during the last recession was not quickly reducing their spending. Start cutting non-essential expenses: cable, your cellphone package, etc.  The other mistake I saw people making was not calling creditors before the first missed payment. Creditors are far more likely to work with you if you call them  before  you miss a payment. Explain to your creditors how you are impacted by COVID-19 and ask for COVID-19 hardships programs. Most creditors and lenders have hardship programs, but programs specific to COVID-19 may be better. Ask about:  The effects on your credit score (ideally none) when you delay payments How long you can defer (creditors may extend deferrals if COVID-19 continues to spread) What happens once your start repayment  Your financial situation in the future   Even if you can pay your expenses, it may make sense to defer your payments. If you are paying expenses through savings and are facing a layoff or have little in savings, carefully consider accepting options to delay payments. Delaying payments frees up cash so you can save money. As mentioned before, ask about programs specifically for those impacted by COVID-19.  Is it worth it?  All payment deferrals will impact you. The key is understanding the impact and deciding if it's worth it.  The ability to miss payments is not free money. You will have to pay it back. How you pay it back depends on your creditors. Contact your creditors and ask what happens after the missed payment period ends. The COVID-19 crisis changes the rules, but in general, there are typically four possibilities that can occur once your deferral period is over:  Your creditors add your missed payments to the end of your payment period. So if you missed three payments, your total payment period would be three months longer. Your loan is modified. This can mean a higher interest rate or an extended payment period. You temporarily pay a higher amount. This higher amount is your regular payment plus a portion of the payments you missed until you have “paid off” your missed payments.  Your creditor may ask for the total missed payments to be paid in full once your deferral period ends.  The last thing you want is to find yourself in a worse financial position because you accepted an offer to defer payments without knowing the consequences after your deferral period ends. Get all the facts so you can make an informed decision.  "

    answer = openai.Answer.create(
        search_model="ada",
        model=fine_tune_model,
        question=question,
        file=train_file_id,
        examples_context=example_context,
        examples=examples,
        max_rerank=max_rerank,
        max_tokens=max_tokens,
        stop=["\n", "<|endoftext|>"]
    )
    for a in answer['answers']:
        outstr+=a+" "
    return outstr

def generate_completion(question, api_key = None, fine_tune_model = None, temperature=0.7, max_tokens = 200):
    outstr = ""
    if fine_tune_model is None:
        fine_tune_model = 'curie'
    if api_key is None:
        api_key = APIKey

    res = openai.Completion.create(
        model=fine_tune_model,
        prompt=question,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=["\n", "<|endoftext|>"],

    )
    outstr = res['choices'][0]['text']
    return outstr

if __name__ == '__main__':
    test_question = "How to Apply for SNAP Benefits"
    print(generate_completion_simple(test_question, 200, 0.7))
