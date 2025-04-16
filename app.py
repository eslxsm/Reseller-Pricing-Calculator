from flask import Flask, render_template, request
import openai
import os

# Your OpenAI API key (replace this with your actual key)
openai.api_key = "YOUR API KEY"  # ← Replace with your key

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    advice = ""

    if request.method == "POST":
        try:
            # Safely get and convert inputs
            cost = float(request.form.get("cost", 0))
            shipping = float(request.form.get("shipping", 0))
            commission = float(request.form.get("commission", 0)) / 100
            gst = float(request.form.get("gst", 0)) / 100
            selling_price = float(request.form.get("selling_price", 0))
            competitor_price = float(request.form.get("competitor_price", 0))

            # Calculate profit
            total_cost = cost + shipping + (selling_price * commission) + (selling_price * gst)
            profit = selling_price - total_cost
            profit_percent = (profit / selling_price) * 100

            result = {
                "selling_price": selling_price,
                "profit": round(profit, 2),
                "profit_percent": round(profit_percent, 2),
                "total_cost": round(total_cost, 2)
            }

            # Get AI-powered advice
            advice = get_ai_advice(selling_price, profit, profit_percent, competitor_price)

        except Exception as e:
            result = None
            advice = f"⚠️ Error: {e}"

    return render_template("calculator.html", result=result, advice=advice)


def get_ai_advice(selling_price, profit, profit_percent, competitor_price):
    prompt = f"""
    I’m an online reseller. I sell a product for ₹{selling_price}. After fees, my profit is ₹{profit} which is {profit_percent}%.
    My competitor is selling the same product for ₹{competitor_price}.

    Give me business advice in simple words:
    - Should I raise or lower my price?
    - Is my margin healthy?
    - Any psychological pricing or strategy tips?
    - Should I consider bundling or upselling?

    Be friendly and helpful like a smart business coach.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or use "gpt-3.5-turbo" if needed
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    app.run(debug=True)
