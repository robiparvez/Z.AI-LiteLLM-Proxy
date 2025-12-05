"""Example usage of Z.AI with LiteLLM.

Based on: https://docs.litellm.ai/docs/providers/zai

Note: When using via proxy, models are configured in z_ai_config.yaml.
For direct usage with LiteLLM library, use the zai/ prefix.

To run this example:
1. Set ZAI_API_KEY environment variable or create .env file
2. Run: uv run python main.py
"""

import os
from litellm import completion


def main():
    """Example of calling Z.AI GLM models via LiteLLM.

    These examples use the direct zai/ prefix for SDK usage.
    When using the proxy, models are accessed without the zai/ prefix
    (e.g., just 'glm-4.6' instead of 'zai/glm-4.6').
    """

    # Ensure API key is set
    if not os.environ.get('ZAI_API_KEY'):
        print("Error: ZAI_API_KEY environment variable not set")
        print("Get your API key from: https://z.ai/model-api")
        return

    print("Testing Z.AI GLM-4.6 model (via direct SDK)...\\n")

    try:
        # Example: Non-streaming request with zai/ prefix
        response = completion(
            model="zai/glm-4.6",
            messages=[{
                "role": "user",
                "content": "Hello from LiteLLM! Please respond briefly."
            }]
        )

        print("Response:")
        print(response.choices[0].message.content)
        print("\\n" + "="*50 + "\\n")
    except Exception as e:
        print(f"Error: {e}")
        print("\\nNote: For direct SDK usage, ensure you have the latest LiteLLM version.")
        print("For proxy usage, use the start_proxy.sh or start_proxy.bat scripts.")

    # Example: Streaming request
    print("Testing streaming response with glm-4.5-flash (FREE tier)...\\n")

    try:
        response = completion(
            model="zai/glm-4.5-flash",  # FREE tier model
            messages=[{
                "role": "user",
                "content": "Count from 1 to 5."
            }],
            stream=True
        )

        print("Streaming response:")
        for chunk in response:
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end='', flush=True)
        print("\\n")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()