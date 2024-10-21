from keras.api.models import load_model
from keras.api.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import csv


def log_conversation(user_input, ai_response):
    with open('conversation_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_input, ai_response])


# Load the model and tokenizer
try:
    model = load_model('Allister_AI.h5')
    print(model.summary())
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

try:
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
except Exception as e:
    print(f"Error loading tokenizer: {e}")
    exit()


# Format the output by converting the model predictions to readable text
def format_output(model_output):
    print(f"Model Output Shape: {model_output.shape}")
    print(f"Model Output Values: {model_output}")

    # Convert the model output to a sequence of indices
    output_sequence = np.argmax(model_output, axis=-1)
    print(f"Generated Indices: {output_sequence}")

    # Convert indices to words using the tokenizer's index_word dictionary
    response_text = ' '.join([tokenizer.index_word.get(index, '') for index in output_sequence.flatten()])
    print(f"Formatted Response Text: {response_text}")

    # Return the first word in the formatted response or a fallback if empty
    predicted_word = response_text.split()[0] if response_text else ""
    return predicted_word


# Generate a response based on user input and the AI's last response
def generate_response(user_input, ai_last_response, max_words=20):
    max_sequence_len = 17  # Adjust this as needed
    conversation_history = ai_last_response + " " + user_input

    for _ in range(max_words):
        # Tokenize and pad the conversation history to fit the model's input requirements
        token_list = tokenizer.texts_to_sequences([conversation_history])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')

        # Predict the next word using the model
        predicted_prob = model.predict(token_list, verbose=0)

        # Use format_output to convert model predictions into readable text
        predicted_word = format_output(predicted_prob)

        # Check if the predicted word is valid
        if not predicted_word:
            break

        # Append the predicted word to the conversation history
        conversation_history += " " + predicted_word

        # End condition: stop at punctuation
        if predicted_word in ['.', '!', '?']:
            break

    # Extract the last part of the conversation history as the AI's new response
    ai_new_response = " ".join(conversation_history.split()[-max_words:])
    return ai_new_response


# Main loop to interact with the AI
ai_last_response = ""
while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("Chat ended.")
        break
    ai_new_response = generate_response(user_input, ai_last_response)
    log_conversation(user_input, ai_new_response)
    print("AI: ", ai_new_response)
    ai_last_response = ai_new_response
