from app.tools.search_tool import SearchTool


search_tool = SearchTool()


print("=== SEARCH TOOL INFO ===")

print(
    search_tool.get_info()
)


print("\n=== VALID SEARCH ===")

print(
    search_tool.execute({
        "query": "Python programming for beginners"
    })
)


print("\n=== SEARCH URL ===")

print(
    search_tool.build_search_url(
        "AI agent automation"
    )
)


print("\n=== QUERY WITH SPACES ===")

print(
    search_tool.execute({
        "query": "AI Buddy project"
    })
)


print("\n=== EMPTY QUERY ===")

print(
    search_tool.execute({
        "query": ""
    })
)


print("\n=== INVALID QUERY TYPE ===")

print(
    search_tool.execute({
        "query": 12345
    })
)


print("\n=== SEARCH TOOL AVAILABILITY ===")

print(
    search_tool.is_available()
)