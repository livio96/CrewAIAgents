# Different AI Agents Built with CrewAI framework

## Project Structure


### Files and Directories

- **.env**: Contains environment variables for API keys.
- **requirement.txt**: Contains a list of libraries to install
- **README.md**: This file, contains project information and instructions.
- **main.py**: Entry point for the streamlit project, loading environment variables, and kicking off the Agent system.


## Setup

### Prerequisites

- Python 3.12 or higher
- `pip` (Python package installer)

### Virtual Python Environment Creation 
```bash
- pip install virtualenv
- python -m venv customer_support_agent
- customer_support_agent\Scripts\activate
```

### Install Dependencies

Install the required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

Add your API keys in .env file:
```bash
OPENAI_API_KEY=your_openai_api_key
```

### Run the Project
Run the main.py script:


Run the Streamlit application:
```
streamlit run app.py
```

Once the server is running, it will open a web browser
