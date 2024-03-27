import vertexai
from vertexai.language_models import CodeGenerationModel
import sys
from pathlib import Path


def write_function(function, file):
    Path(file).parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'w') as f:
        f.write(function
                .replace("```hcl", "")
                .replace("```python", "")
                .replace("```", "")
                .strip())


def prompt_generate_code(prompt, request):
    prompt = f"""
    {prompt}.
    input: ${request}.
    output:
    """
    return prompt


def generate_code(project_gcp, input_text, request, temperature):
    vertexai.init(project=project_gcp, location="europe-west1")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 2048,
        "temperature": temperature
    }

    model = CodeGenerationModel.from_pretrained('code-bison@002')
    response = model.predict(
        prefix=prompt_generate_code(input_text, request),
        **parameters
    )
    return response.text


if __name__ == "__main__":

    example_arg = sys.argv[1]
    project_gcp = sys.argv[2]
    examples = {
        "players": f"""
        The data will come from a table 'players_goals' in the new dataset 'myligue' with the schema 'player', 'team', 'goal_date' and 'minute'. This table stores all the goals scored by all the players in a season.
        We need to create and read this table, and make a ranking with the five players who have scored the most goals from minute 60 onwards and store this transformation in a new 'players_ranking' table within the 'myligue' dataset with schema 'player' and 'goals_scored' as the total number of goals. This request is under the project '{project_gcp}'.
    """,
        "customers":  f"""
        I am embarking on the establishment of a new dataset named 'raw_sales_data' within the expansive framework of BigQuery, nestled under the project '{project_gcp}' and region 'europe-southwest1'. This dataset is poised to become the home for two distinctive tables: 'customer_table' and 'sales_table'. On the other hand, we are going to need to create another dataset named 'master_sales_data,' which will have a single table called 'bigtable_info'
        In the realm of 'customer_table,' my objective is the seamless integration of pivotal fields such as 'customer_id', 'name', and 'email'. These components promise to furnish crucial insights into the essence of our valued customer base.
        Conversely, when delving into the nuances of 'sales_table,' the envisioned tapestry includes essential elements like 'order_id' 'product' 'price', 'amount' and 'customer_id'. Theseattributes, meticulously curated, will play a pivotal role in the nuanced exploration and analysis of sales-related data.
        The 'bigtable_info' table will have all the fields resulting from the union of the two tables, 'customer_table' and 'sales_table.' Here, the outcome of joining the two tables by the 'customer_id' numeric field will be stored.
        Furthermore, as part of our meticulous data collection strategy, I plan to inaugurate a dedicated Google Cloud Storage bucket christened 'sales-etl-bucket.' This repository is strategically designed to serve as a robust container for collating data, particularly hailing from CSV files. This endeavor is set to enhance the efficiency and organizational prowess of our data management processes.
        To enhance the structure, two distinct subfolders, 'input/sales' and 'input/customers' have been ingeniously incorporated within the 'sales-etl-bucket,' ensuring a refined organization of the incoming data streams.
        You will need to read the CSV files within the 'input/sales' folder to write the data into the 'sales_table'. Additionally, you should perform the same operation with the files from the 'input/customers' folder to write the data into the 'customer_table'. Finally, you are required to perform a join between the sales and customers information based on the 'customer_id' number field and write the merged information into the 'bigtable_info'.
    """
    }

    prompt_tf = open("prompt/prompt_tf.txt", "r")
    prompt_py = open("prompt/prompt_py.txt", "r")

    write_function(
        generate_code(
            project_gcp,
            prompt_tf.read(),
            examples[example_arg].strip(),
            0),
        f"generated/{example_arg}/terraform/main.tf"
    )

    write_function(
        generate_code(
            project_gcp,
            prompt_py.read(),
            examples[example_arg].strip(),
            0.2),
        f"generated/{example_arg}/python/etl.py"
    )
