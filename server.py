from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import answer

app = Flask(__name__)
query = True

history = [
    {
        'question':"Test Question",
        'answer': "Sample answer"
    },
    {
        'question': "This is a very long question that should span more than one line",
        'answer': "This should be a long response, explaining over a finance term in a great level of detail, but within the max-tokens (200/300) as specified."
    },
]
dummy_q_a = {
    "What day is today?": "Friday",
    "Q2": "a2",
}
# ROUTES

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/chat/<string:endpoint>')
def chat(endpoint):
    return render_template('chat.html', data={"history":history, "endpoint":endpoint})

# AJAX FUNCTIONS

@app.route('/ask', methods=['GET', 'POST'])
def ask_question():

    json_data = request.get_json()   
    q = json_data["question"]
    end = json_data["endpoint"]
    if end == "answer":
        max_rerank = int(json_data['max_rerank'])
    if end == "completion":
        temperature = float(json_data['temperature'])
    max_tokens = int(json_data['max_tokens'])

    if query:
        if end == "answer":
            a = answer.generate_answer_simple(q, max_rerank = max_rerank, max_tokens = max_tokens)
        if end == "completion":
            a = answer.generate_completion_simple(q,max_tokens = max_tokens, temperature = temperature)
    elif q in dummy_q_a:
        a = dummy_q_a[q]
    else:
        a = "I am not sure I understood your question."
    out = {
        'question':q,
        'answer':a
    }
    history.append(out)
    #send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data = history)



if __name__ == '__main__':
    app.run(debug = True)




