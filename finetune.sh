export OPENAI_API_KEY="<OPENAI_API_KEY>"

#Fine-tuning the curie model
openai api fine_tunes.create -t finetuning_10.jsonl -m curie --suffix "finetuning-10"
openai api fine_tunes.create -t finetuning_20.jsonl -m curie --suffix "finetuning-20"
openai api fine_tunes.create -t finetuning_50.jsonl -m curie --suffix "finetuning-50"
openai api fine_tunes.create -t finetuning_100.jsonl -m curie --suffix "finetuning-100"
openai api fine_tunes.create -t finetuning_200.jsonl -m curie --suffix "finetuning-200"

#Fine-tuning the davinci model, expansive so doing two for now
openai api fine_tunes.create -t finetuning_50.jsonl -m davinci --suffix "finetuning-50"
openai api fine_tunes.create -t finetuning_100.jsonl -m davinci --suffix "finetuning-100"

#Retrieve your fine-tune jobs and analyze result
for fine_tune_file in $(openai api fine_tunes.list)['data']
do
  file_id=fine_tune_file['id']
  echo "${file_id}"
  openai api fine_tunes.results -i "${file_id}"
done

#See below for sample running script after fine-tune models are prepared
#Each run should be used associated with distinct model-name
#The five arguments corresponds to
#argv[1] : openai api key
#argv[2] : training data file path
#argv[3] : test data file path
#argv[4] : output file path
#argv[5] : fine tune model name uploaded in previous steps

#Generate output for curie
# python test_result.py ${OPENAI_API_KEY} [train_file_id] testData.json output_curie_10.txt [fine-tune-model-name]
# python test_result.py ${OPENAI_API_KEY} [train_file_id] testData.json output_curie_20.txt [fine-tune-model-name]
# python test_result.py ${OPENAI_API_KEY} [train_file_id] testData.json output_curie_50.txt [fine-tune-model-name]
# python test_result.py ${OPENAI_API_KEY} [train_file_id] testData.json output_curie_100.txt [fine-tune-model-name]
# python test_result.py ${OPENAI_API_KEY} [train_file_id] testData.json output_curie_200.txt [fine-tune-model-name]

#Generate output for davinci
# python test_result.py ${OPENAI_API_KEY} [train_file_id] testData.json output_davinci_50.txt [fine-tune-model-name]
# python test_result.py ${OPENAI_API_KEY} [train_file_id] testData.json output_davinci_100.txt [fine-tune-model-name]

