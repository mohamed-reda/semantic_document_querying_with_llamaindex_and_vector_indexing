from llama_index.core import Settings
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

from common_llm_models import setup_models

setup_models()


# --------

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return eval(str(a)) * eval(str(b))


def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return eval(str(a)) + eval(str(b))


def subtract(a: float, b: float) -> float:
    """Subtract two numbers and returns the difference"""
    return eval(str(a)) - eval(str(b))


def divide(a: float, b: float) -> float:
    """Divide two numbers and returns the quotient"""
    return eval(str(a)) / eval(str(b))


multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
sub_tool = FunctionTool.from_defaults(fn=subtract)
divide_tool = FunctionTool.from_defaults(fn=divide)

agent = ReActAgent.from_tools([multiply_tool, add_tool, sub_tool, divide_tool], llm=Settings.llm, verbose=True)

response = agent.chat("Use a tool to calculate every step of: 20 + ( 2 * 4 ) / ( 5 - 1 )")
print(response)

"""
project name is:3 Math Expression Evaluator using ReAct Agent and LLM

> Running step 19797d84-b255-4347-95c4-06480340ee4f. Step input: None
Thought: I have enough information to calculate the final result without using any more tools. I'll use the user's language to answer
Answer: The calculation is 20 + (2 * 4) / (5 - 1). First, we do multiplication and division from left to right, so it becomes 20 + 8 / 4 = 20 + 2 = 22.
The calculation is 20 + (2 * 4) / (5 - 1). First, we do multiplication and division from left to right, so it becomes 20 + 8 / 4 = 20 + 2 = 22.
"""
