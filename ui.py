import sqlite3

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.widgets import Static

class PyChronicle(App):

    CSS_PATH = "app.css"

    def load_execution(self):
     connection = sqlite3.connect("trace.db")
     cursor = connection.cursor()

     cursor.execute("""
SELECT line_number,variable_name, serialized_value
FROM variable_history

""")

     self.rows = cursor.fetchall()
     connection.close()


    def load_code(self):
       with open("sample.py", "r") as file:
         lines = file.readlines()

       code = ""
       for i, line in enumerate(lines, start=1):
        code += f"{i:>2}  {line}"

       return code

    def compose(self) -> ComposeResult:

        # Read data from SQLite
      

        self.load_execution()
        print("kkkkk")
       
        CodeView = self.load_code()
        # Create text
        variable_text = "Execution.....................\n\n"

        for line_number, name, value in self.rows:
            variable_text += f"Line {line_number}: {name} = {value}\n"

        yield Header()

        yield Static(
    "Code View\n\n" + CodeView,
    id="code"
)

        yield Static(variable_text, id="Execution")

        yield Footer()


if __name__ == "__main__":
    PyChronicle().run()
