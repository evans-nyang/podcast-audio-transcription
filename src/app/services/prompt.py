model_instructions = """
Solve a podcast guest extraction task using interleaving Thought, Action, Observation steps.
Thought can reason about the current situation, Observation understands relevant information from an Action's output, and Action can be one of three types:
  
  (1) <search>entity</search>: Searches for the exact entity in a knowledge source and returns relevant details.
  (2) <lookup>keyword</lookup>: Finds the next sentence containing the keyword in the podcast transcript or summary.
  (3) <finish>guest names</finish>: Returns a list of extracted guest names and finishes the task.
"""

prompt1 = """Question
Who are the guests mentioned in the following podcast summary?

Summary:
"In this episode, host Jane Doe sits down with Dr. Emily Carter and tech entrepreneur Alex Reed to discuss the future of artificial intelligence. 
Emily, a professor at MIT, shares her insights on ethical AI, while Alex talks about how his startup is leveraging AI for medical breakthroughs."

Thought 1
The question asks for guest names in the podcast. I need to identify proper names from the summary.

Action 1
<lookup>Dr.</lookup>

Observation 1
Dr. Emily Carter is mentioned in the summary.

Thought 2
Emily Carter is a guest. Now, I need to check for any other names.

Action 2
<lookup>entrepreneur</lookup>

Observation 2
Tech entrepreneur Alex Reed is also mentioned.

Thought 3
Alex Reed is another guest. The full list of guests is: Dr. Emily Carter, Alex Reed.

Action 3
<finish>Dr. Emily Carter, Alex Reed</finish>
"""

prompt2 = """Question
Identify all guests from this podcast transcript.

Transcript:
"Welcome back to the AI Revolution Podcast! I'm your host, Mark Benson. Today, we have an amazing panel featuring Dr. Susan Wright, an AI researcher at Stanford, 
along with journalist Kevin Patel and CEO Linda Huang, who will share their insights on AI ethics and business applications."

Thought 1
I need to find names of people who are identified as guests.

Action 1
<lookup>Dr.</lookup>

Observation 1
Dr. Susan Wright is mentioned.

Thought 2
Susan Wright is a guest. Now, I need to check for more guests.

Action 2
<lookup>journalist</lookup>

Observation 2
Journalist Kevin Patel is mentioned.

Thought 3
Kevin Patel is a guest. I should check for any more guests.

Action 3
<lookup>CEO</lookup>

Observation 3
CEO Linda Huang is mentioned.

Thought 4
Linda Huang is also a guest. The full list of guests is: Dr. Susan Wright, Kevin Patel, Linda Huang.

Action 4
<finish>Dr. Susan Wright, Kevin Patel, Linda Huang</finish>
"""
