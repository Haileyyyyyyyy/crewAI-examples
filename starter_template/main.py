import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from decouple import config

from textwrap import dedent
from agents import ScriptAgents
from tasks import ScriptTasks
import json

# os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
# os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID")

# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py


# Main class to run the agents and tasks cooperatively
class ScriptCrew:
    def __init__(self, backgrounds, characters):
        self.backgrounds = backgrounds
        self.characters = characters

    def run(self):
        # Initialize agents and tasks
        agents = ScriptAgents()
        tasks = ScriptTasks()

        # Create instances of each agent
        background_selector_agent = agents.background_selector()
        character_selector_agent = agents.character_selector()
        storyline_writer_agent = agents.storyline_writer()
        dialogue_writer_agent = agents.dialogue_writer()
        director_agent = agents.director()

        # Define the cooperative tasks
        background_task = tasks.select_background(background_selector_agent, self.backgrounds)
        character_task = tasks.select_characters(character_selector_agent, self.characters)
        storyline_task = tasks.create_storyline(storyline_writer_agent, character_task())
        dialogue_task = tasks.write_dialogue(dialogue_writer_agent, storyline_task(), character_task(), background_task())
        oversee_task = tasks.oversee_script(director_agent, storyline_task(), dialogue_task())

        # Create and run the Crew with agents and tasks
        crew = Crew(
            agents=[
                background_selector_agent,
                character_selector_agent,
                storyline_writer_agent,
                dialogue_writer_agent,
                director_agent
            ],
            tasks=[
                background_task,
                character_task,
                storyline_task,
                dialogue_task,
                oversee_task
            ],
            verbose=True  # Optional: Enables detailed output
        )

        # Run the crew and return the result
        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Crew AI Template")
    print("-------------------------------")
    
    ## EXTRACT CHARACTERS INFO
    with open('starter_template/data_table/s2m_char_data.json', 'r') as file:
        data = json.load(file)

    extracted_data = []
    for character in data['character_presets']:
        extracted_info = {
            'char_id': character['char_id'],
            'char_default_desc': character['char_default_desc'],
            'gender': character['gender']
        }
        extracted_data.append(extracted_info)

    # Store the extracted data in a variable
    characters = extracted_data
    # print("characters : ", characters)


    ## EXTRACT BACKGROUNDS INFO
    with open('starter_template/data_table/s2m_map_data.json', 'r') as file:
        data = json.load(file)

    extracted_data = []
    for background in data['maps']:
        extracted_info = {
            'stage_id': background.get('stages')[0].get('stage_id'),
            'stage_desc': background.get('stages')[0].get('stage_desc'),
            'stage_name': background.get('stages')[0].get('stage_name')
        }
        extracted_data.append(extracted_info)


    # Store the extracted data in a variable
    backgrounds = extracted_data
    # print("Backgrounds : ",backgrounds)




    custom_crew = ScriptCrew(backgrounds, characters)
    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)
