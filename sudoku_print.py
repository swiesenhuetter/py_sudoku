

def generate_sudoku_html(sudoku_strings, output_file):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sudoku</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f9f9f9;
                margin: 0;
            }
            table {
                border-collapse: collapse;
                margin: 20px;
            }
            td {
                width: 40px;
                height: 40px;
                text-align: center;
                vertical-align: middle;
                font-size: 20px;
                font-family: Arial, sans-serif;
                border: 1px solid #000;
            }
            /* Edges of the entire Sudoku grid */
            .outer-right {
                border-right: 2px solid #000;
            }
            .outer-bottom {
                border-bottom: 2px solid #000;
            }
            .outer-left {
                border-left: 2px solid #000;
            }
            .outer-top {
                border-top: 2px solid #000;
            }
            /* Inner bold lines to separate 3x3 sections */
            .inner-right {
                border-right: 2px solid #000;
            }
            .inner-bottom {
                border-bottom: 2px solid #000;
            }
        </style>
    </head>
    <body>
        <table>
    """

    # Construct table rows and cells
    for row_index, row_values in enumerate(sudoku_strings):
        html_content += "<tr>"
        segments = row_values.replace("\"", "").split()

        for col_index, segment in enumerate(segments):
            for i, char in enumerate(segment):
                # Determine classes for borders
                border_class = ""

                # Add outer borders
                if row_index == 0:
                    border_class += "outer-top "
                if col_index == 0:
                    border_class += "outer-left "
                if row_index == 8:
                    border_class += "outer-bottom "
                if col_index == 8:
                    border_class += "outer-right "

                # Add inner bold lines to separate 3x3 blocks
                if col_index % 3 == 2:
                    border_class += "inner-right "
                if row_index % 3 == 2:
                    border_class += "inner-bottom "

                cell_value = char if char != '-' else '&nbsp;'
                html_content += f"<td class='{border_class.strip()}'>{cell_value}</td>"
        html_content += "</tr>"

    # Close the HTML
    html_content += """
        </table>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"Sudoku HTML generated: {output_file}")


if __name__ == "__main__":
    sudoku_strings = [
        "53- -7- ---",
        "6-- 195 ---",
        "-98 --- -6-",
        "8-- -6- --3",
        "4-- 8-3 --1",
        "7-- -2- --6",
        "-6- --- 28-",
        "--- 419 --5",
        "--- -8- -79"
    ]
    generate_sudoku_html(sudoku_strings, "sudoku.html")
