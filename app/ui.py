from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.data import EMAIL_DATA
import sys
import os

# Ensure the parent directory is in the path to allow direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_dashboard():
    emails_html = ""
    for difficulty, emails in EMAIL_DATA.items():
        emails_html += f"<h3>{difficulty.capitalize()} Task Inbox</h3><div class='inbox'>"
        for e in emails:
            emails_html += f"""
            <div class='email'>
                <strong>{e.subject}</strong><br/>
                <p>{e.body}</p>
                <em>From: {e.sender}</em>
            </div>
            """
        emails_html += "</div>"
        
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Triage AI Dashboard</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
                body {{ 
                    font-family: 'Inter', sans-serif; 
                    background-color: #0f172a; 
                    color: #f8fafc; 
                    padding: 40px; 
                    margin: 0;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                }}
                h1 {{ 
                    color: #38bdf8; 
                    text-align: center; 
                    font-size: 3rem; 
                    margin-bottom: 1rem; 
                    letter-spacing: -1px;
                }}
                .subtitle {{
                    text-align:center; 
                    max-width:600px; 
                    margin: 0 auto 40px; 
                    color:#94a3b8;
                    line-height: 1.6;
                }}
                h3 {{ 
                    color: #c084fc; 
                    border-bottom: 2px solid #1e293b; 
                    padding-bottom: 10px; 
                    margin-top: 40px;
                    font-size: 1.5rem;
                }}
                .inbox {{ 
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 20px; 
                    margin-bottom: 20px; 
                }}
                .email {{ 
                    background: linear-gradient(145deg, #1e293b, #0f172a); 
                    padding: 24px; 
                    border-radius: 16px; 
                    border-left: 4px solid #3b82f6; 
                    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); 
                    transition: all 0.3s ease; 
                }}
                .email:hover {{ 
                    transform: translateY(-8px); 
                    border-left-color: #ec4899; 
                    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);
                }}
                .email strong {{ 
                    font-size: 1.25rem; 
                    color: #e2e8f0; 
                    margin-bottom: 10px;
                    display: box;
                }}
                .email p {{
                    color: #cbd5e1;
                    line-height: 1.5;
                }}
                .email em {{ 
                    color: #64748b; 
                    font-size: 0.85rem; 
                    display: block; 
                    margin-top: 20px; 
                    font-style: normal;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .header-badge {{
                    background: #1e3a8a;
                    color: #bfdbfe;
                    padding: 6px 12px;
                    border-radius: 9999px;
                    font-size: 0.8rem;
                    font-weight: bold;
                    display: inline-block;
                    margin-bottom: 10px;
                    text-transform: uppercase;
                }}
                .top-bar {{
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="top-bar">
                    <span class="header-badge">OpenEnv v1.0</span>
                </div>
                <h1>📧 Email Triage Simulation</h1>
                <p class="subtitle">A visual representation of the datasets your AI agents will face during the simulation. These are the inbound messages ready for classification, replies, and escalations!</p>
                {emails_html}
            </div>
        </body>
    </html>
    """
    return html_content
