# OrgChartWithMermaid
*Python code to turn a CSV file of employee details into an org chart that is human readable and editable.*

![Sample Org Chart Output](https://github.com/wrashi/OrgChartWithMermaid/blob/main/mermaid-diagram-2023-06-27-073747.png?raw=true)

Visualizing a fast changing organizational structure for investors, potential customers, and curious journalists 
	is common in the startup space.
Many other organizations also need a quick and easy way to create an org chart without learning Visio in detail or hiring an IT department.

The included Python script creates an org chart which can be exported to HTML and other formats. 
The output is easy to read and modify by people who consider themselves non-technical.

This script tries to hit the following requirements.

| Want                                              | MoSCoW Ranking |
| ------------------------------------------------- | -------------- |
| Multiple people maintain the list                 | Must           |
| Simple workflow for non-tech end user             | Must           |
| Straight lines between nodes                      | Must           |
| Employee IDs non-contiguous integers              | Must           |
| Update the employee list constantly               | Should         |
| Easy to embed in a department web page            | Should         |
| Easy to export to an image file                   | Should         |
| Use of identifying icons for rank                 | Should         |
| Use different shapes, colours for visual identity | Could          |

The sample CSV is tab-delineated and based on Peter Stark's Chinook sample database, which is used in the excellent [SQLite Tutorial](https://www.sqlitetutorial.net/) site. 

The Python script requires two modules: SQLAlchemy and Pandas.
Python throws errors if these are not available.
To install both, in the Terminal use `pip`:

```bash
pip install sqlalchemy pandas
```


###  Usage

1. Download the package.
2. Modify the CSV file (it should open in any spreadsheet program).
3. Save the modified CSV file (select tab-separated-values (TSV) format) into the same folder as the script.
4. Modify the Python script to output the desired information and format.
5. Run the script.
6. Copy the Markdown output into a program that handles Mermaid like Obsidian, Notion, Hackmd.io, etc. 
   For the latest features like Markdown strings and FontAwesome icons, use the [Mermaid live editor](https://mermaid.live) without the lines starting with 3 backtics `` ` ``.

A detailed review of Mermaid and the code's inner workings is available [in this blog post](https://wpenner.com/en/blog/building-an-org-chart-with-mermaid).
