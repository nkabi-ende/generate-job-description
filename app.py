from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate-job-description', methods=['POST'])
def generate_job_description():
    try:
        # Parse JSON request data
        data = request.json
        location = data.get("location")
        position = data.get("position")
        engagement_type = data.get("engagementType")
        hours = data.get("hours")
        time_zone = data.get("timeZone")
        pay_rate = data.get("payRate")
        responsibilities = data.get("responsibilities")
        requirements = data.get("requirements")
        benefits = data.get("benefits")
        company_overview = data.get("companyOverview")

        # Validate required fields
        if not all([location, position, engagement_type, hours, time_zone, pay_rate, responsibilities, requirements, benefits, company_overview]):
            return jsonify({"error": "Missing required fields"}), 400

        # Generate prompt for OpenAI API
        prompt = (
            f"This {engagement_type} role is open in {location}.\n"
            f"Position: {position}\n"
            f"Hours: {hours}, {time_zone}\n"
            f"Rate: {pay_rate}\n\n"
            "Role Overview: Generate a description based on the responsibilities provided.\n"
            f"About the client: {company_overview}\n\n"
            f"Key Responsibilities:\n{responsibilities}\n\n"
            f"Requirements:\n{requirements}\n\n"
            f"Benefits:\n{benefits}\n"
        )

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )

        # Extract the generated job description
        job_description = response['choices'][0]['message']['content'].strip()

        # Return response
        return jsonify({"jobDescription": job_description}), 200

    except openai.error.OpenAIError as e:
        return jsonify({"error": "Failed to generate job description", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
