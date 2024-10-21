# AllisterAI

Allister AI is a conversational AI chatbot built using Keras, which takes user input and generates intelligent responses. It’s designed to interact in a continuous conversation, making predictions for next words based on context and conversation history. This project includes a trained deep learning model, capable of understanding and processing natural language.

---

## 🚀 Features

- **Interactive Conversation:** Generates responses dynamically based on user input and previous conversation history.
- **Conversation Logging:** Automatically logs user interactions and AI responses into a CSV file.
- **Custom Fine-Tuning:** Easily replace the model to adapt to specific conversational tasks or domains.
- **Real-Time Predictions:** Provides responses by predicting the next words based on probabilities from the trained model.
- **Error Handling:** Built-in mechanisms for graceful failure in case of model or tokenizer loading issues.

---

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- Keras (v2.x) and TensorFlow (v2.x)
- Numpy
- Pickle
- CSV module (standard Python library)

### Setup Instructions

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/allister-ai.git
    cd allister-ai
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have your AI model and tokenizer files:
    - Place your pre-trained model (`Allister_AI.h5`) and tokenizer (`tokenizer.pickle`) files in the root directory.

4. Run the chatbot:
    ```bash
    python allister_ai.py
    ```

---

## 🧠 Usage

1. After launching the chatbot, type any input to initiate a conversation.
2. The AI will respond to your input based on its learned conversation patterns.
3. To end the conversation, simply type `bye`.

```bash
You: Hello, how are you?
AI: I am doing well, thank you.
