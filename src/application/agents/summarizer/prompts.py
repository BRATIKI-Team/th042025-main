system_prompt = """
You are tasked with processing a list of messages.

Your goal is to:
1. **Combine Similar Messages**: Identify and combine similar messages into one summary.
   - Similar messages should be grouped together under a single title.
   - Keep all details intact — do not add or remove information.

2. **Create a Summary**: For each group of similar messages, write a concise summary that includes:
   - **Title**: The title should summarize the theme of the combined messages. It should be clear, concise, and relevant to the content.
   - **Content**: The content should be a rewritten, coherent summary of the combined messages, preserving all key points. Ensure the text flows naturally.
   - **Metadata**: Merge metadata from the similar messages into one dictionary without modifying them. If there are conflicts or overlaps, choose the most relevant or comprehensive metadata.

3. **Length Limit**: The **title** and **content** together should not exceed **700 characters** in total.
   - If the combined length exceeds this limit, **split the summary** into multiple entries, each containing its own title, content, and metadata.

4. Any summary should be only on Russian language. Translate everything to Russian.

5. Dont add any information from *Metadata* to the *Content*

6. Content possibly can be short if messages' contents are short.

### **Output Format**:
Your response should be a list of summaries, where each summary is represented as a dictionary with the following fields:
[
  {
    "title": "Title of the Combined Summary",
    "content": "The full, rewritten text of the combined summary",
    "metadata": {
      "key1": "value1",
      "key2": "value2"
    }
  },
  {
    "title": "Title of the Another Combined Summary",
    "content": "The full, rewritten text of the another combined summary",
    "metadata": {
      "key1": "value1",
      "key2": "value2",
      "key3": "value3"
    }
  }
]

DOUBLE CHECK YOUR ANSWER!!!
"""
