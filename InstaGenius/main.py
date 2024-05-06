from flask import Flask, render_template, request, redirect, url_for
from agents import MarketingAnalysisAgents
from tasks import MarketingAnalysisTasks
from crewai import Crew
from dotenv import load_dotenv
import time
import groq  # Import the groq module
import logging

load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()

MAX_REQUESTS_PER_MINUTE = 3000
TIME_WINDOW = 60
INITIAL_RETRY_DELAY = 10

retry_delay = INITIAL_RETRY_DELAY

def handle_rate_limit_error():
    logger.error("Rate limit reached. Waiting for retry...")
    time.sleep(retry_delay)
    return retry_delay * 2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_model', methods=['POST'])
def update_model():
    selected_model = request.form['model']
    agents.update_model(selected_model)
    return redirect(url_for('index'))

@app.route('/result', methods=['POST'])
def result():
    product_website = request.form['website']
    product_details = request.form['details']

    # Add the "wait processing your request!" message
    processing_message = "Processing your request..."

    product_competitor_agent = agents.product_competitor_agent()
    strategy_planner_agent = agents.strategy_planner_agent()
    creative_agent = agents.creative_content_creator_agent()

    try:
        website_analysis = tasks.product_analysis(
            product_competitor_agent, product_website, product_details)
        market_analysis = tasks.competitor_analysis(
            product_competitor_agent, product_website, product_details)
        campaign_development = tasks.campaign_development(
            strategy_planner_agent, product_website, product_details)
        write_copy = tasks.instagram_ad_copy(creative_agent)
    except groq.RateLimitError as e:
        retry_delay = handle_rate_limit_error()
        website_analysis = tasks.product_analysis(
            product_competitor_agent, product_website, product_details)
        market_analysis = tasks.competitor_analysis(
            product_competitor_agent, product_website, product_details)
        campaign_development = tasks.campaign_development(
            strategy_planner_agent, product_website, product_details)
        write_copy = tasks.instagram_ad_copy(creative_agent)

    copy_crew = Crew(
        agents=[
            product_competitor_agent,
            strategy_planner_agent,
            creative_agent
        ],
        tasks=[
            website_analysis,
            market_analysis,
            campaign_development,
            write_copy
        ],
        verbose=True,
        max_rpm=50
    )

    ad_copy = copy_crew.kickoff()

    senior_photographer = agents.senior_photographer_agent()
    chief_creative_director = agents.chief_creative_director_agent()

    try:
        take_photo = tasks.take_photograph_task(
            senior_photographer, ad_copy, product_website, product_details)
        approve_photo = tasks.review_photo(
            chief_creative_director, product_website, product_details)
    except groq.RateLimitError as e:
        retry_delay = handle_rate_limit_error()
        take_photo = tasks.take_photograph_task(
            senior_photographer, ad_copy, product_website, product_details)
        approve_photo = tasks.review_photo(
            chief_creative_director, product_website, product_details)

    image_crew = Crew(
        agents=[
            senior_photographer,
            chief_creative_director
        ],
        tasks=[
            take_photo,
            approve_photo
        ],
        verbose=True,
    )

    image = image_crew.kickoff()

    # Return the processing message along with the ad copy and image
    return render_template('result.html', processing_message=processing_message, ad_copy=ad_copy, image=image)

if __name__ == '__main__':
    app.run(debug=True)
