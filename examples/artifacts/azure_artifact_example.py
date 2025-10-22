import asyncio
import os
import warnings
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk_extra_services.artifacts import AzureBlobArtifactService
from csv_agent import csv_agent


APP_NAME = "azure_artifact_example"
USER_ID = "example_user"
SESSION_ID = "session1"


def load_env():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(dotenv_path):
        warnings.warn(
            f'Missing .env file at {dotenv_path}. See .env.example for an example.'
        )
    else:
        load_dotenv(dotenv_path, override=True, verbose=True)

        
async def main():
    session_service = InMemorySessionService()

    # Option 1: Use connection string
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    # Option 2: Use account URL + credential (e.g., SAS or key)
    account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")  # e.g., https://<account>.blob.core.windows.net
    credential = os.getenv("AZURE_STORAGE_CREDENTIAL")  # e.g., SAS token or account key

    container_name = os.getenv("AZURE_CONTAINER", "artifacts")

    if connection_string:
        artifact_service = AzureBlobArtifactService(
            container_name=container_name,
            connection_string=connection_string,
        )
    elif account_url and credential:
        artifact_service = AzureBlobArtifactService(
            container_name=container_name,
            account_url=account_url,
            credential=credential,
        )
    else:
        raise RuntimeError(
            "Configure either AZURE_STORAGE_CONNECTION_STRING or (AZURE_STORAGE_ACCOUNT_URL and AZURE_STORAGE_CREDENTIAL) in .env"
        )

    runner = Runner(
        agent=csv_agent,
        app_name=APP_NAME,
        session_service=session_service,
        artifact_service=artifact_service
    )

    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    user_prompt = "Write a CSV row 'name,age,city' and save it as 'sample.csv'"
    print(f">>> Sending to agent: {user_prompt}")
    user_content = types.Content(role="user", parts=[types.Part(text=user_prompt)])
    final_response = None
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=user_content
    ):
        if event.is_final_response() and event.content:
            final_response = event.content.parts[0].text
    print("Agent response:", final_response)

    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("Session state:", session.state)


if __name__ == "__main__":
    load_env()
    asyncio.run(main())


