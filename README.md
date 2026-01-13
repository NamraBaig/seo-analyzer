SEO Analyzer (Woorank-Inspired Project)

A simplified SEO analysis web app inspired by [Woorank.com](https://www.woorank.com), built completely from scratch using Python (Flask), BeautifulSoup, and Requests.  

This project replicates the core backend logic of an SEO auditing tool. it analyzes a website’s content, metadata, structure, and technical factors, then generates a weighted SEO score (out of 100).

Live Demo
👉 [https://seo-analyzer-peach.vercel.app/](#)


About the Project
Objective
To develop a backend system that replicates Woorank’s SEO audit features - without using any of its APIs - by manually crawling and analyzing websites.

Features
Analyze any website for:
- SEO meta data (Title, Description, Headings)
- Content quality (word count, keywords)
- Image optimization (alt tags)
- Link structure (internal & external)
- Technical SEO (HTTPS, Sitemap, Robots.txt)
- Social metadata (Open Graph, Twitter tags)
- Generates an SEO Score / 100

✅ User-friendly web interface  
✅ Optional API endpoint for JSON results  
✅ Lightweight & easily deployable (Flask + Vercel)



Tech Stack

| Layer | Technology Used |
|-------|------------------|
| Backend | Python (Flask) |
| Web Scraping | BeautifulSoup, Requests |
| Frontend | HTML, CSS (via Flask templates) |
| Hosting | Vercel / Render |
| Version Control | Git + GitHub |



Scoring Formula

| Category | Weight | Description |
|-----------|---------|-------------|
| Technical SEO | 25% | HTTPS, Robots.txt, Sitemap |
| On-page SEO | 25% | Title, Meta Description, Headings, Image Alt |
| Content Quality | 20% | Word count, Keyword presence |
| Links | 15% | Internal & External Links |
| Social Metadata | 15% | Open Graph & Twitter Tags |

Each section contributes to the final score (0–100), based on the number and quality of successful checks.

System Architecture
User Input: 
The user enters a website URL through the frontend form.  

Backend Processing: 
Flask receives the URL → fetches page content using Requests → parses HTML with BeautifulSoup → runs multiple SEO checks.  

Scoring:
Each check contributes to a weighted SEO score (technical + on-page + content + links + social).  

Output:
Results are displayed on a clean HTML results page and can also be fetched via a JSON API endpoint.



How to Run Locally
Prerequisites
- Python 3.x
- pip installed

Steps
```bash
# 1. Clone this repository
git clone https://github.com/<your-username>/seo-analyzer.git
cd seo-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Now open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser 🌐


Screenshots

Home Page  
<img width="1365" height="661" alt="image" src="https://github.com/user-attachments/assets/856ab209-2c76-4c60-9ac5-c41492f38b1a" />

SEO Report Page 
<img width="1365" height="668" alt="image" src="https://github.com/user-attachments/assets/c67e5155-64a1-4f87-97e1-d249829b1d00" />


Documentation Summary

- Built using Flask (backend) and BeautifulSoup (HTML parser)
- Performs SEO checks without using third-party APIs
- Uses a custom weighted scoring algorithm
- Deployed on Vercel with serverless Python runtime

Author
Namra Baig 
B.Tech in Cybersecurity | Tech Enthusiast  
[LinkedIn](https://linkedin.com/in/namrabaig15) | [GitHub](https://github.com/NamraBaig)
