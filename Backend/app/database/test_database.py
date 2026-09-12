from sqlalchemy import inspect

from app.database.connection import engine


def test_database():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    expected_tables = [
        "users",
        "tasks",
        "notifications",
        "conversations",
        "workflows",
        "scheduled_jobs",
        "memories"
    ]

    print("\nAI Buddy Database Test")
    print("-" * 30)

    for table in expected_tables:

        if table in tables:
            print(f"[PASS] {table}")
        else:
            print(f"[FAIL] {table}")

    print("-" * 30)

    if all(
        table in tables
        for table in expected_tables
    ):
        print("Database test passed successfully.")
        return True

    print("Database test failed.")
    return False


if __name__ == "__main__":

    test_database()