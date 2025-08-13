# 🚀 AI Resume Optimizer


## ✨ Key Features

  * **AI-Powered Tailoring**: Leverages Google's Gemini AI to analyze job descriptions and rewrite your resume to match.
  * **Keyword Optimization**: Intelligently integrates essential keywords and skills to pass through Applicant Tracking Systems (ATS).
  * **Impactful Language**: Replaces passive phrases with strong, action-oriented verbs to highlight your accomplishments.
  * **Instant Feedback**: Provides a clear, bulleted list of all changes made so you know what was improved.
  * **Simple & Fast**: A clean, intuitive interface that gets the job done in seconds.

-----

## 🛠️ Tech Stack

This project is a full-stack application built with a modern, decoupled architecture.

| **Component** | **Technology** |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| **Frontend** |    **React.js** |
| **Backend** |    **Python** |
| **API** |    **FastAPI** |
| **AI Model** |    **Gemini 1.5 Flash** |
| **Deployment**|    **Vercel** |

-----

## ⚙️ Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

  * **Python 3.9+** & **Node.js v14+**
  * A **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

### 1\. Backend Setup

```bash
# Clone the repository and navigate into the project
git clone https://github.com/your-username/AI-Resume-Optimizer.git
cd AI-Resume-Optimizer/api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate # On macOS/Linux
# .\venv\Scripts\activate # On Windows

# Install dependencies
pip install -r requirements.txt

# Create a .env file and add your API key:
echo "GEMINI_API_KEY=YOUR_API_KEY_HERE" > .env

# Start the server (from the 'api' directory)
uvicorn main:app --reload
```

### 2\. Frontend Setup

```bash
# Open a NEW terminal window
# Navigate into the frontend directory from the root
cd AI-Resume-Optimizer/resume-ai-frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

Your application should now be running locally, with the frontend at `http://localhost:3000` and the backend at `http://localhost:8000`.

-----

## 📄 License

This project is open-source and available under the **MIT License**. See the `LICENSE` file for more details.
