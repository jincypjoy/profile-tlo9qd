import sys
import sqlite3
from datetime import datetime


connection = sqlite3.connect("trace.db")
cursor = connection.cursor()

cursor.execute("DELETE FROM variable_history")

def trace_calls(frame, event, arg):

    if event == "line":

        line = frame.f_lineno

        allowed = {"x", "y", "z", "name"}

        for name, value in frame.f_locals.items():

            if name not in allowed:
                continue

            cursor.execute("""
            INSERT INTO variable_history
            (timestamp,line_number,variable_name,serialized_value)
            VALUES(?,?,?,?)
            """,(
                datetime.now().isoformat(),
                line,
                name,
                str(value)
            ))

    return trace_calls


def run_script(filename):
    print("Running script...")
    sys.settrace(trace_calls)

    with open(filename) as file:
        code = file.read()

    exec(code, {})

    sys.settrace(None)

    connection.commit()
    connection.close()