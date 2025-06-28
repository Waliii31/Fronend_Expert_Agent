import os
from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

@st.cache_resource
def get_agent_config():
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    agent = Agent(
        name="Frontend Expert",
        instructions="You are a frontend expert",
    )

    return agent, config

import asyncio

async def run_agent_async(agent_input: str):
    agent, config = get_agent_config()
    result = await Runner.run(agent, input=agent_input, run_config=config)
    return result.final_output

def get_frontend_answer(agent_input: str) -> str:
    try:
        return asyncio.run(run_agent_async(agent_input))
    except RuntimeError:
        return asyncio.get_event_loop().run_until_complete(run_agent_async(agent_input))
