from app.tools.file_tool import FileTool


file_tool = FileTool()


print("=== FILE TOOL INFO ===")

print(
    file_tool.get_info()
)


print("\n=== CREATE FILE OPERATION ===")

print(
    file_tool.execute({
        "operation": "create",
        "file_path": "test.txt",
        "content": "Hello from AI Buddy."
    })
)


print("\n=== READ FILE OPERATION ===")

print(
    file_tool.execute({
        "operation": "read",
        "path": "test.txt"
    })
)


print("\n=== UPDATE FILE OPERATION ===")

print(
    file_tool.execute({
        "operation": "update",
        "file_path": "test.txt",
        "content": "Updated content."
    })
)


print("\n=== DELETE FILE OPERATION ===")

print(
    file_tool.execute({
        "operation": "delete",
        "file_path": "test.txt"
    })
)


print("\n=== INVALID OPERATION ===")

print(
    file_tool.execute({
        "operation": "rename",
        "file_path": "test.txt"
    })
)


print("\n=== EMPTY PATH ===")

print(
    file_tool.execute({
        "operation": "read",
        "file_path": ""
    })
)


print("\n=== FILE TOOL AVAILABILITY ===")

print(
    file_tool.is_available()
)