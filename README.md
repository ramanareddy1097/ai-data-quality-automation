\# AI-Powered Data Quality \& Incident Automation Platform



An automated data quality monitoring platform that detects data issues in incoming CSV files, calculates a data quality score, uses a locally hosted LLM to analyze the problems, generates an incident report, stores quality history in SQLite, and exposes the results through a FastAPI service.



This project demonstrates an end-to-end \*\*AI + Data Engineering + Automation\*\* workflow using entirely local and free technologies.



\---



\## 🚀 Project Overview



Data quality problems can cause inaccurate reports, failed downstream processes, and unreliable business decisions.



This platform automates the initial data-quality investigation process.



When a new CSV file arrives in the monitored folder:



1\. The system automatically detects the file.

2\. Data quality checks are executed.

3\. Data quality issues are identified.

4\. A quality score is calculated.

5\. The quality report is sent to a locally hosted LLM.

6\. The LLM analyzes possible root causes and business impact.

7\. Remediation recommendations are generated.

8\. An incident report is saved as JSON.

9\. The quality run is stored in SQLite.

10\. FastAPI provides access to quality-history data.



\---



\## 🏗️ Architecture



```text

&#x20;                 ┌──────────────────────┐

&#x20;                 │   Incoming CSV File  │

&#x20;                 └──────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌──────────────────────┐

&#x20;                 │  File Monitor        │

&#x20;                 │  Watchdog            │

&#x20;                 └──────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌──────────────────────┐

&#x20;                 │ Data Quality Engine  │

&#x20;                 │ Python + Pandas      │

&#x20;                 └──────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌──────────────────────┐

&#x20;                 │ Quality Score        │

&#x20;                 │ \& Issue Detection    │

&#x20;                 └──────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌──────────────────────┐

&#x20;                 │ Local LLM Analysis   │

&#x20;                 │ Ollama + Llama 3.2   │

&#x20;                 └──────────┬───────────┘

&#x20;                            │

&#x20;                ┌───────────┴───────────┐

&#x20;                ▼                       ▼

&#x20;      ┌──────────────────┐    ┌────────────────────┐

&#x20;      │ Incident Report  │    │ SQLite Quality DB  │

&#x20;      │ JSON             │    │                    │

&#x20;      └──────────────────┘    └─────────┬──────────┘

&#x20;                                        │

&#x20;                                        ▼

&#x20;                               ┌──────────────────┐

&#x20;                               │ FastAPI REST API │

&#x20;                               └──────────────────┘

```



\---



\## 🛠️ Technologies



\### Data Engineering



\* Python

\* Pandas

\* SQLite

\* CSV

\* ETL / data-quality processing



\### AI / LLM



\* Ollama

\* Llama 3.2

\* Prompt engineering

\* Automated root-cause analysis

\* AI-generated remediation recommendations



\### Automation



\* Watchdog

\* Automated file monitoring

\* Automated quality checks

\* Automated incident generation



\### API



\* FastAPI

\* Uvicorn

\* REST endpoints

\* Swagger/OpenAPI documentation



\### Development



\* Git

\* GitHub

\* Pytest

\* Python virtual environment



\---



\## 🔍 Data Quality Checks



The platform currently detects:



| Data Quality Check           | Severity |

| ---------------------------- | -------- |

| Missing customer IDs         | HIGH     |

| Invalid email addresses      | MEDIUM   |

| Negative transaction amounts | HIGH     |

| Invalid transaction statuses | MEDIUM   |

| Duplicate transactions       | HIGH     |



The system calculates a quality score based on the detected data-quality issues.



\---



\## 🤖 AI Analysis



When quality problems are detected, the structured quality report is sent to a locally running Llama 3.2 model through Ollama.



The AI is instructed to provide:



\* Summary of data-quality problems

\* Possible root cause for each issue

\* Business impact

\* Recommended remediation actions

\* Overall assessment



The prompt also instructs the model to preserve the original issue counts rather than recalculating or changing the numbers.



\---



\## 📊 Example Result



Example test dataset:



```text

DATA QUALITY REPORT

==================================================



Records: 10010

Quality Score: 99.5%



Issues:



\- Missing customer\_id

&#x20; Records: 10

&#x20; Severity: HIGH



\- Invalid email address

&#x20; Records: 10

&#x20; Severity: MEDIUM



\- Negative transaction amount

&#x20; Records: 10

&#x20; Severity: HIGH



\- Invalid transaction status

&#x20; Records: 10

&#x20; Severity: MEDIUM



\- Duplicate transaction

&#x20; Records: 10

&#x20; Severity: HIGH

```



The platform then sends this structured information to the local LLM for automated analysis.



\---



\## 📄 Incident Reports



Each processed file can generate an incident report containing:



```text

reports/

└── incident\_YYYYMMDD\_HHMMSS.json

```



The JSON report contains:



\* Processing timestamp

\* Source file

\* Total records

\* Quality score

\* Detected issues

\* Issue severity

\* AI-generated analysis



\---



\## 🗄️ Database



SQLite is used to maintain quality-run history.



Current table:



```text

quality\_runs

```



Fields include:



```text

id

file\_name

total\_records

quality\_score

issue\_count

created\_at

```



This allows previous quality runs to be queried through the API.



\---



\## 🔌 FastAPI



The project exposes a REST API for accessing quality information.



\### Root endpoint



```text

GET /

```



Returns application status.



\### Health endpoint



```text

GET /health

```



Returns service health status.



\### Quality history



```text

GET /quality-runs

```



Returns previous quality runs.



\### Individual quality run



```text

GET /quality-runs/{run\_id}

```



Returns information for a specific quality run.



\### API documentation



When the API is running, interactive Swagger documentation is available through:



```text

http://127.0.0.1:8000/docs

```



\---



\## ⚙️ Project Structure



```text

ai-data-quality-automation/

│

├── app/

│   ├── api/

│   │   └── main.py

│   │

│   ├── automation/

│   │   └── file\_monitor.py

│   │

│   ├── ai\_analyzer.py

│   ├── create\_bad\_data.py

│   ├── database.py

│   ├── generate\_data.py

│   └── quality\_checker.py

│

├── data/

│   ├── incoming/

│   ├── processed/

│   └── sample/

│

├── reports/

│

├── tests/

│   └── test\_quality\_checker.py

│

├── .gitignore

└── README.md

```



\---



\## 🧪 Testing



The project includes automated tests using Pytest.



Current tests validate:



\* Total record count

\* Quality score

\* Number of detected issue types

\* Specific data-quality issue detection



Run tests with:



```powershell

pytest

```



Expected result:



```text

2 passed

```



\---



\## 💻 Local Setup



\### 1. Clone the repository



```powershell

git clone <YOUR-GITHUB-REPOSITORY-URL>

cd ai-data-quality-automation

```



\### 2. Create a virtual environment



```powershell

python -m venv .venv

```



\### 3. Activate the environment



```powershell

.venv\\Scripts\\Activate.ps1

```



\### 4. Install Python dependencies



```powershell

pip install pandas faker requests watchdog fastapi uvicorn pytest

```



\### 5. Install Ollama



Install Ollama on your local machine and download the Llama 3.2 model:



```powershell

ollama pull llama3.2

```



\### 6. Generate sample data



```powershell

python app\\generate\_data.py

```



\### 7. Create a bad-data test file



```powershell

python app\\create\_bad\_data.py

```



\### 8. Run the quality checker



```powershell

python app\\quality\_checker.py

```



\### 9. Run the automation monitor



```powershell

python app\\automation\\file\_monitor.py

```



The application will monitor:



```text

data/incoming/

```



When a new CSV file is added, processing starts automatically.



\### 10. Start the API



From the project root:



```powershell

python -m uvicorn app.api.main:app --reload

```



Then open:



```text

http://127.0.0.1:8000/docs

```



\---



\## 💰 Cost



This project was designed to run locally without paid cloud services or paid APIs.



The LLM runs locally using Ollama and Llama 3.2.



No OpenAI API key or cloud AI API is required.



\---



\## 🎯 Skills Demonstrated



This project demonstrates practical experience with:



\* Python

\* Pandas

\* SQL

\* SQLite

\* Data quality engineering

\* ETL concepts

\* Data validation

\* Data profiling

\* Automation

\* File monitoring

\* LLM integration

\* Prompt engineering

\* Local AI

\* JSON processing

\* REST APIs

\* FastAPI

\* Pytest

\* Error handling

\* Git/GitHub

\* Software project structure



\---



\## 🔮 Future Improvements



Potential future enhancements include:



\* Data-quality dashboards

\* More validation rules

\* Data profiling and anomaly detection

\* Email or Slack incident notifications

\* Historical quality trends

\* Retry and failure handling

\* Data remediation pipelines

\* Docker containerization

\* Cloud deployment

\* Azure AI Search integration

\* Production database integration

\* Role-based API authentication



\---



\## 📌 Disclaimer



This is a portfolio project designed to demonstrate AI, data engineering, automation, and API development skills.



It is not presented as an enterprise production system.



\---



\## 👨‍💻 Author



Built as an AI + Data Engineering portfolio project demonstrating automated data-quality monitoring, local LLM analysis, incident generation, database persistence, and API development.



