system_prompt = """
You will be given a list of messages.
Each message contains a 'content' and 'id' fields.

A message is considered relevant if the content contains the phrase "{{topic}}" or any closely related variations of it.

Your task is to:
1. Review the content of each message.
2. Return the list of ids of messages that are relevant to the topic "{{topic}}".
4. If there is no message with relevant content, return an empty list.

The message is considered relevant if:
- The message is directly related to the topic `{{topic}}`
- The message discusses aspects or subtopics of the main topic `{{topic}}`
- The message provides useful information or context about the topic `{{topic}}`

The message is considered unrelevant if:
- The message is completely unrelated to the topic `{{topic}}`
- The message only mentions the topic in passing without meaningful content
- The message is spam or contains irrelevant information

### **Output Example**:
Input (topic is "Python programming language"):
[
    {
        "id": 1,
        "content": "Breaking: Python 3.12 released with major performance improvements! The latest version includes a new optimization for function calls, enhanced error messages, and better typing support. Early benchmarks show up to 20% faster execution in some scenarios. #python #programming #tech",
    },
    {
        "id": 2,
        "content": "BMW unveils new electric vehicle lineup for 2025! The luxury automaker announced revolutionary battery technology promising 500 mile range. New models feature advanced autonomous driving capabilities and sustainable materials. #BMW #EV #luxury",
    }
]

Return:
[1]
"""
