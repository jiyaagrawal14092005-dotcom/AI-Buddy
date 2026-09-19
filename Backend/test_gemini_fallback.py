from app.tools.search_tool import SearchTool


def main():
    print("=" * 60)
    print("GEMINI FALLBACK VERIFICATION")
    print("=" * 60)

    search_tool = SearchTool()

    print("\nTesting AI answer generation...")
    print("Query: Explain Python in simple words.")

    result = search_tool.execute({
        "query": "Explain Python in simple words."
    })

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)

    print(result)

    print("\n" + "=" * 60)
    print("STATUS")
    print("=" * 60)

    if result.get("success"):
        print("✅ Gemini/Fallback answer generation is working.")
        print("Model used:", result.get("model_used"))
        print("Status:", result.get("status"))
    else:
        print("❌ Gemini/Fallback answer generation failed.")
        print("Message:", result.get("message"))
        print("Error:", result.get("error"))

    print("\nTest finished.")


if __name__ == "__main__":
    main()