FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: run the pipeline in brand mode with the Ghost Tequila prompt
ENTRYPOINT ["python", "scripts/run_report_workflow.py"]
CMD [ \
    "--mode", "brand", \
    "--research-prompt-file", "ghost_tequila/ghost_tequila_research_prompt.md", \
    "--research-output", "ghost_tequila/report.txt", \
    "--report-source", "ghost_tequila/report.txt", \
    "--verbose" \
]
