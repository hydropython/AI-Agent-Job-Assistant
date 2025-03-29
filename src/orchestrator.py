# src/orchestrator.py
from crewai import Task, Crew
from job_scraper import scraper_agent
from cover_letter_generator import writer_agent
from google_sheets_integration import tracker_agent

# Define tasks
scrape_task = Task(
    description="Scrape 5 job listings for 'Data Scientist' in 'London'",
    agent=scraper_agent,
    expected_output="List of job dictionaries"
)

write_task = Task(
    description="Generate cover letters for scraped jobs using CV at 'uploads/cv.pdf'",
    agent=writer_agent,
    expected_output="List of cover letters"
)

track_task = Task(
    description="Log scraped jobs and their status in Google Sheets",
    agent=tracker_agent,
    expected_output="Confirmation message"
)

# Create crew
crew = Crew(
    agents=[scraper_agent, writer_agent, tracker_agent],
    tasks=[scrape_task, write_task, track_task],
    verbose=2
)
def run_automation():
    crew = Crew(
        agents=[scraper_agent, writer_agent, tracker_agent],
        tasks=[scrape_task, write_task, track_task],
        verbose=2
    )
    result = crew.kickoff()
    # MODIFIED: Extract jobs from the scrape task output
    # crewAI returns task outputs in a specific format; adjust based on actual output
    jobs = result.tasks_output[0].raw if result.tasks_output else []  # Access the first task's output
    return jobs
# # Function to run the crew
# def run_automation():
#     return crew.kickoff()

if __name__ == "__main__":
    result = run_automation()
    print(result)